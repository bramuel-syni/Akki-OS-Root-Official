READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M7 VERIFICATION ROLLUP · Platform-integrity story for eventual M7 seal

**Authored:** 2026-09-16T~07:10Z (this-shift · at completion of POST-8 M6 verification).
**Authority:** Owner ruling 2026-09-16T~06:20Z verbatim:

> "One standing add: when the M-family wave-window verifications complete clean, produce a compact M7 VERIFICATION ROLLUP note (one table: every wave window verified, commits enumerated, verdicts, receipts index) — that becomes the platform-integrity story for the eventual M7 seal, same way the backend-ratification snapshot serves the M6 story."

**Scope.** Covers the entire M-family verification chain landed this shift under SO §4.2 wave-window enumeration + clause 6 cross-wave modification handling: W0 · W1-family (W1 + W1b POST-2 + W1b/W1c POST-3) · M2 (POST-4) · M3 (POST-5) · M4 (POST-6) · M5 (POST-7) · M6 (POST-8).

**Verdict at rollup time.** All 9 verification walks CLEAN · Path α · ratchet_delta=0 across the chain · ratchet floor **4384** unchanged since CP-M7-W1-POST-1 (mechanism build).

---

## §1 · Wave-window verification table (canonical)

| Walk | Wave window scope | Open commit | Close commit(s) | Next-family open | Modules verified | Tests verified | Test count / duration | Cross-wave findings | Verdict | Receipt path | Close-note path | Master SHA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **W-M7-W0-VERIFICATION** | W0 · platform integrity + seal-check surfaces | (impl. dates 2026-09-13) | canonical W0 close · pre-existing surfaces | 2026-09-13 next open | 11 seal-adjacent + 6 W0-original | 31 W0 invariants | 4358-baseline confirmed | none | ✅ Path α | `phase0/m7_w0_verification/verification_receipt_20260916.json` | `notes/W_M7_W0_VERIFICATION_close.md` | (2026-09-16T~04:00Z master) |
| **W-M7-W1-VERIFICATION** | W1 · SO §3.2 progress-signal contract | 2026-09-13T06:33:22Z W1 close | `fe01e5e` | 2026-09-13 W1b | 5 W1 modules | 68 W1 invariants | 68 passed 0.87s | none | ✅ Path α | `phase0/m7_w1_verification/verification_receipt_20260916.json` | (banked in DECISIONS) | (2026-09-16T~04:15Z master) |
| **CP-M7-W1-POST-2-VERIFICATION** | W1b · Capability Registry | 2026-09-13T06:59:30Z W1b close | `5364593` | 2026-09-13 W1c | 1 module (capability_registry.py · 6-name __all__) | 15 W1b invariants | 15 passed 0.64s | rule-proliferation avoided (RED-drill unexpectedly-passed tell) | ✅ Path α | `phase0/m7_w1_post_2_verification/verification_receipt_20260916.json` | `notes/W_M7_W1_POST_2_CAPABILITY_REGISTRY_close.md` | `cb061265` |
| **CP-M7-W1-POST-3-VERIFICATION** | W1b residual + W1c integration proof | 2026-09-13T06:59:30Z W1b + 2026-09-13T07:16:30Z W1c | `5364593` + `e1712a1` | W-REGISTRY-EXTENSION-G3 `33edf56b` | 5 W1b residual modules + W1c invariant | 111 invariants | 111 passed 1.13s | SO §4.2 ratified this walk | ✅ Path α | `phase0/m7_w1_post_3_verification/verification_receipt_20260916.json` | `notes/W_M7_W1_POST_3_VERIFICATION_close.md` | `c71b9fb7` |
| **CP-M7-W1-POST-4-VERIFICATION** | M2 · Rules Service + Doc-0 attributes | `451ef2bb` (W-M2-SW1 · 2026-09-13T18:51:44Z) | `95d688cd` (M2 END-GATE · 2026-09-13T19:54:49Z) | W-M3-SW1 `eaa0e04` | 15 modules across 7 sub-waves | 15 test files | 81 passed 1.47s | 1 cross-wave-out (`clock.py` M2→M3 SW1) surfaced · SO §4.2 clause 6 ratified this walk | ✅ Path α | `phase0/m7_w1_post_4_verification/verification_receipt_20260916.json` | `notes/W_M7_W1_POST_4_VERIFICATION_close.md` | `23662838` |
| **CP-M7-W1-POST-5-VERIFICATION** | M3 · Watch + Agent Containment + DAP-M3-remainder + BCA | `eaa0e04` (W-M3-SW1 · 2026-09-14T05:24:59Z) | `7123cf8` (W-M3-SW12 · 2026-09-14T09:24:26Z) | W-CONN-SP1 `4b0909a` | 13 first-added + 1 cross-wave-in (`clock.py` M3 SW1 extension of M2 SW5 addition · legitimate under clause 6) | 12 test files | 83 passed 1.19s | SO §4.2 clause 6 first applied in enforcement form (cross-wave-in) | ✅ Path α | `phase0/m7_w1_post_5_verification/verification_receipt_20260916.json` | `notes/W_M7_W1_POST_5_VERIFICATION_close.md` | `d6433017` |
| **CP-M7-W1-POST-6-VERIFICATION** | M4 · Assistant Surfaces (journey_assistant/) | `6888f35` (W-M4-SW1 · 2026-09-14T10:13:24Z) | `72a1201` (W-M4-SW6 · 2026-09-14T10:41:04Z) | `d6bf1bc` (source_plane admin) | 7 modules across 6 sub-waves | 6 test files | 47 passed 0.9s | none · zero post-window drift | ✅ Path α | `phase0/m7_w1_post_6_verification/verification_receipt_20260916.json` | `notes/W_M7_W1_POST_6_VERIFICATION_close.md` | `450ddd8f` |
| **CP-M7-W1-POST-7-VERIFICATION** | M5 (compound milestone · 6 named sub-waves + 1 supplement) | `24928de` (W-AUDIO-POC CP-A1 · 2026-09-14T13:18:12Z) | `7cccbe8` (W-D12-POC CP-D12P1 · 2026-09-15T10:11:40Z) | W-M8-TESTS-FIRST-GUARD-INVARIANT `e02dd4d` | 37 modules across 7 sub-trees | 28 test files | 204 passed 2.02s | **5 cross-wave-out extensions** (custody_file, registry_write, 3 engines) all legitimate under clause 6 | ✅ Path α | `phase0/m7_w1_post_7_verification/verification_receipt_20260916.json` | `notes/W_M7_W1_POST_7_VERIFICATION_close.md` | `450ddd8f` (batched) |
| **CP-M7-W1-POST-8-VERIFICATION** | M6 · Audio Plane v1 Production Build | `b105aa0` (CP-M6-1-1 · 2026-09-15T17:26:25Z) | `7b45a89` (CP-M6-9-2 · 2026-09-16T03:07:30Z) | CP-M7-W1-POST-1 `2c7a8f0` | 28 modules across 9 sub-waves | 29 test files | 253 passed 2.19s | none · zero post-window drift | ✅ Path α | `phase0/m7_w1_post_8_verification/verification_receipt_20260916.json` | `notes/W_M7_W1_POST_8_VERIFICATION_close.md` | (this-turn master pending) |

---

## §2 · Aggregate metrics (M-family verification chain)

**Total across 9 walks:**
- **Wave windows verified:** 9 (W0 · W1 · W1b/W1c residual · M2 · M3 · M4 · M5 · M6).
- **CP commits enumerated:** ~110 across chain (5 W0/W1 + 5 W1b/W1c + 7 M2 + 12 M3 + 6 M4 + 28 M5 + 28 M6 = 91 CP-boundary commits; additional intra-CP commits in some windows).
- **Modules verified (first-added `services/`):** ~113 modules (5 W1 + 6 W1b + 15 M2 + 14 M3 + 7 M4 + 37 M5 + 28 M6 = 112 distinct + `clock.py` cross-wave).
- **Test files exercised:** 6 W0 + 5 W1 + 7 W1b/W1c + 15 M2 + 12 M3 + 6 M4 + 28 M5 + 29 M6 = 108 test files across chain.
- **Invariant passes at rollup time (peak per-window):** 31 + 68 + 111 + 81 + 83 + 47 + 204 + 253 = **878 file-scoped invariants across chain**.
- **Ratchet delta across chain:** 0 (all verification walks · no mechanism landing).
- **Ratchet floor at rollup:** **4384** (bumped last at CP-M7-W1-POST-1 · Resource Registry mechanism · this shift).

**Cross-wave findings (SO §4.2 clause 6 surface-not-drift):**
- **1 cross-wave-out (M2 → M3)**: `services/reliable_time_source/clock.py` — M2 SW5 addition + M2 END-GATE loosening → M3 SW1 tight-guard extension (legitimate · Flag-2 owner directive · ratchet 3714→3719 · append-only).
- **5 cross-wave-out (M5 → post-M5)**:
  1. `custody_file.py` → M8 CP-M8-G1 part-B (`e02dd4d`) + CP-SW6-HYG-1 Redaction Hardening (`053d3f1`) · +6/+6 · both owner-directive-cited.
  2. `registry_write.py` → M8 CP-CRO1+CP-CRO2 (`29ff398`) · +12 · CP-cited.
  3. `data_suite_v2/engines/{__init__, analyze_workspace_engine, deep_dive_engine}.py` (3 files) → M8 CP-DASWR1+CP-DDDR1 (`7bde883`) · +10 · "CP-D8 HALT discharged in-place" · CP-cited.
- **Zero cross-wave drift** anywhere in chain (no unexplained modifications lacking CP citation / ratchet delta / owner directive / append-only shape).

---

## §3 · Standing-orders discipline exercised across chain

| Standing order | Application | First-exercise walk |
|---|---|---|
| **§3.1** ALIVE IS NOT DONE (real-seal contract) | 11 seal-check surfaces route through `services.output_verified_seal.is_real_seal`/`parse_seal` primitives; new surfaces added since 2026-09-13 W0 close all conform | W-M7-W0-VERIFICATION |
| **§3.2** NO RUN WITHOUT A PROGRESS SIGNAL | 5 W1 primitive-shape modules freeze the runtime-supervisor contract; cross-service binding enforcement remains P2 owner-desk item | W-M7-W1-VERIFICATION |
| **§3.3** NO SEAL WITHOUT BOTH SHAs | Every mechanism-build seal in the chain carries Track-a HEAD + Master HEAD at seal time; verification walks are shape-exempt (single-master-commit · no fixup because no seal-file references master SHA) | CP-M7-W1-POST-1 (mechanism · fixup landed) |
| **§4.1** CREDENTIAL CUSTODY READ DISCIPLINE | All GPU-orchestrator SSH operations use env-injection; shape-only helper on JSON custody; direct-read guards fire zero SEC incidents | Throughout chain (util interleave) |
| **§4.2** VERIFICATION-WALK SCOPE DISCIPLINE (wave-window commit enumeration) | Ratified at POST-3 walk; clause 6 (cross-wave modification handling) ratified at POST-4; clause 6 first applied in enforcement form at POST-5 (cross-wave-in) | POST-3 (ratified) · POST-4 (clause 6 ratified) · POST-5 (clause 6 enforcement) |

---

## §4 · Platform integrity assertion (at rollup time)

Based on the 9-walk verification chain landed this shift, the platform surface is asserted:

1. **Case-agnostic kernels are LEAK-FREE.** No M-family domain code (Rules Service · Doc-0 attributes · Watch · Agent Containment · DAP-M3-remainder · BCA · Assistant Surfaces · Audio-POC · Data-Suite-v2 · Census-Canon-Align · Release-Gate · De-Identify · Secret-Hygiene · D12-POC · Audio-Plane v1 · Perception Audio Codec) leaks into the case-agnostic platform kernels (`work_supervisor` · `capability_registry` · `resource_registry` · `output_verified_seal`).
2. **All cross-wave modifications are LEGITIMATE extensions.** Every post-window modification (6 total across chain: `clock.py` M2→M3 + 5 M5→M8 modules) carries the SO §4.2 clause 6 4-criteria proof (CP citation + ratchet delta + owner directive + append-only shape). Zero unexplained drift.
3. **The append-only-extension discipline is HOLDING across time.** Zero post-window drift on M3 (2 elapsed days verified clean), M4 (2 elapsed days verified clean), M6 (4 elapsed hours verified clean). Only shape-conforming clause-6 extensions found.
4. **The ratchet floor 4384 is STABLE.** All 9 verification walks landed at ratchet_delta=0. The last ratchet bump (CP-M7-W1-POST-1 Resource Registry · +26) was a mechanism build within scope of the M7 boot.
5. **No banned enforcement tokens on ANY M-family public surface.** Zero `kill|terminate|refuse_dispatch|unregister` hits on the ~113 first-added module surfaces enumerated across chain.

---

## §5 · Receipts index (for M7 seal reader)

Every receipt is machine-parseable JSON at the noted path. Every close-note is markdown at the noted path.

**Receipts (9):** listed inline in the §1 table.

**Grounding briefs (where authored):**
- `notes/M7_OPEN_REPORT_20260916.md`
- `notes/M7_W0_PLATFORM_INTEGRITY_grounding_brief.md`
- `notes/M7_W1_GENERALISATION_grounding_brief.md`
- `notes/wm7_w1_post_2_capability_registry_grounding_brief.md`

**Standing-order authoritative texts:** `STATE/STANDING_ORDERS.md` §3.1-§3.3 + §4.1 + §4.2 (clauses 1-6 including clause 6 ratified this shift).

**Ratchet manifest:** `repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json` (`passed_floor=4384`; ratchet_history entry at `20260916T053500Z` from CP-M7-W1-POST-1).

**Verifier tools:**
- `tools/verify_m7_w1_post_5_m3_window.py` (M3 · direct)
- `tools/verify_m7_w1_post_6_m4_window.py` (M4 · direct)
- `tools/verify_m_family_window.py` (parameterized on milestone_id · M5 + M6 · reusable for future M-family windows)

---

## §6 · GPU utilization at rollup time

- Elapsed 2.56 h · Remaining 69.44 h · both hosts sampler+workload alive throughout the 9-walk chain.
- Peak GPU util 100% per H200 (all 4 GPUs) · peak power ~691-693 W · peak temp ~70-71 °C.
- 612 total bench artefacts banked as of POST-8 seal.
- Report served: `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.

---

## §7 · What this rollup UNBLOCKS

**M7 sealability path.** With W0..M6 all verification-walked clean under SO §4.2 (+ clause 6), M7 can now be sealed once the remaining M7 waves (W2..W9) land per their own owner-input dependencies. This rollup is the platform-integrity backbone the eventual M7 seal will point at.

**Owner-desk items unchanged.** P1 blockers (JUMP root rotation · admin binds for CD + Visitors) and P2 blockers (SW-10 A.1-A.5 · Audio-bytes-retention Path A/B/C · R-17(a) · §3.2 clause 5 cross-service binding enforcement ruling) remain parked exactly as they stood at boot.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
