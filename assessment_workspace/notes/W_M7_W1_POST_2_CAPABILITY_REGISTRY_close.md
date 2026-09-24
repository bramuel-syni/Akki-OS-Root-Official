READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-M7-W1-POST-2 · Capability Registry · Wave close · 2026-09-16T~06:00Z

**Wave:** W-M7-W1-POST-2 (M7 W1-family follow-up).
**Type:** VERIFICATION WALK · zero-delta close (revised from mechanism build after from-disk discovery of pre-existing W1b `services/capability_registry.py`).
**Verdict:** Path α · CLEAN VERIFICATION.
**Predecessor:** CP-M7-W1-POST-1 · Resource Registry SEALED · master `358ea3d4` · ratchet 4384.
**Track-a HEAD at close:** `2c7a8f0c6157d4103feeebad1171a3bdc92d952c` (unchanged from POST-1 · verification walks land no code).
**Master HEAD at close:** to be recorded post-Commit-B.
**Ratchet floor at close:** **4384** (unchanged).

---

## 1 · Progress made

**Attempted to author CP-M7-W1-POST-2 as a mechanism build**: drafted tests-first RED (`test_wm7_w1_post_2_capability_registry.py` · 27 invariants) + grounding brief + planned to land `services/capability_registry/{__init__, registry}.py`. The RED drill executed as expected — but with **22 failed + 5 unexpectedly passed**. The 5 passing tests included `test_capability_registry_module_importable` — which should have failed if the mechanism was unlanded.

**Investigation surfaced the discovery:** `services/capability_registry.py` **already exists** as a single-file module (not the package I proposed). It was landed **2026-09-13T06:59:30Z** by commit `53645935` in **W1b · Platform Primitives wave close** — 26 minutes after W1 close (commit `fe01e5e` at 06:33:22Z) and NOT covered by the M7 W1 verification receipt this shift.

The W1b `services/capability_registry.py` is:
- **Case-agnostic** — module docstring line 15-17 verbatim: *"this module carries NO category-specific tokens. It merely stores (category, name) -> import_path mappings and resolves them lazily."*
- **Compose-not-modify with `services/layer_b/factory.py`** — W1b invariant test `test_layer_b_factory_registries_re_expressible_in_capability_registry` freezes the compose-freeze property (generic registry is strict superset of layer_b.factory pattern; factory is NOT refactored).
- **Registry-surface-only** — public `__all__` names exactly `register_capability`, `get_capability`, `list_categories`, `list_capabilities_in`, `CapabilityNotRegistered`, `_reset_capabilities_for_tests`. No `enforce_/refuse_/kill_/terminate_` operations.
- **Frozen by 15 W1b CP4 invariants** at `tests/invariants/test_w1b_cp4_capability_registry.py` — all pass under file-scoped pytest (0.64 s).

**Under Audio-Plane §1.2 verbatim** (*"Anything ... that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build"*), authoring a NEW `services/capability_registry/` package alongside the pre-existing W1b module would be rule proliferation. The correct move is verification walk on the pre-existing module — analog of W0/W1 verification walks this shift.

**Draft POST-2 test file deleted** at 2026-09-16T~05:59Z (`rm test_wm7_w1_post_2_capability_registry.py`). Grounding brief revised in place to reflect verification-walk shape. Six from-disk checks executed:

- **C.1 · Primitive surface (clean).** `services/capability_registry.py` exports the exact expected 6-name set (`register_capability`, `get_capability`, `list_categories`, `list_capabilities_in`, `CapabilityNotRegistered`, `_reset_capabilities_for_tests`).
- **C.2 · Invariant tests (clean).** 15 W1b invariants pass under `python -m pytest -q` in 0.64 s.
- **C.3 · Case-agnostic doctrine (clean).** 0 domain tokens (asr/diarization/vision/audio/harvest) in module source — verified by `grep -c -i` across the 5 tokens.
- **C.4 · Module unchanged since W1b close (clean).** Last-touched at `2026-09-13T06:59:30Z` by commit `53645935` (W1b close). Zero drift.
- **C.5 · Compose-not-modify (clean).** W1b invariant `test_layer_b_factory_registries_re_expressible_in_capability_registry` passes; `services/layer_b/factory.py` is unchanged (3353 bytes at pre-CP size).
- **C.6 · Registry-only surface (clean).** No enforcement / refusal / termination tokens on public surface.

Machine-readable receipt: `phase0/m7_w1_post_2_verification/verification_receipt_20260916.json`.

**ROADMAP §A.12 W1 reconciliation refined** at `notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md`:
- Added W1b close as a delivery row (2026-09-13T06:59:30Z · `53645935` · +100 ratchet · capability_registry + retention_policy + SourceConnector Protocol + Synology FileStation interface + AttributeStreamBundle_v0 + L2/L4 shells).
- Marked capability_registry ratified at CP-M7-W1-POST-2 (this shift · verification walk · Path α clean · zero-delta).
- Marked remaining W1b deliverables (RetentionPolicy · SourceConnector Protocol · Synology FileStation · AttributeStreamBundle_v0 · L2/L4 shells) as candidate CP-M7-W1-POST-3-VERIFICATION.

## 2 · How much to go

- **CP-M7-W1-POST-2** — CLOSED this shift (Path α clean · zero-delta).
- **W2 · Mount + run vertical slice** — BLOCKED-ON-OWNER unchanged (NAS reach · HF token · 3-station selection · RetentionPolicy Path A/B/C ruling).
- **W-M7-UTILIZATION-72H** — LIVE · elapsed 1.88 h · remaining 70.12 h · 224+224 bench iterations banked · peak 100% GPU util.
- **NEW · candidate CP-M7-W1-POST-3-VERIFICATION** — verification walk for the remaining 5 W1b deliverables (RetentionPolicy + SourceConnector Protocol + Synology FileStation + AttributeStreamBundle_v0 + L2/L4 shells). Owner-desk P2 · authorable autonomously by same precedent as POST-2 verification walk (Audio-Plane §1.2 anti-proliferation + owner ruling 2026-09-16T~05:10Z "applying existing owner law is not speculation").

## 3 · Decisions taken

1. **POST-2 revised from mechanism build to verification walk** on from-disk discovery of pre-existing W1b `services/capability_registry.py`. Rationale: Audio-Plane §1.2 verbatim ("*Anything ... that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build*") + owner ruling 2026-09-16T~05:10Z INTENT was case-agnostic capability registry landed, which is satisfied.
2. **Draft mechanism-build test file deleted** (`test_wm7_w1_post_2_capability_registry.py`) prior to any track-a commit — the draft's 27 invariants tested a different-surface module (`services/capability_registry/{__init__, registry}` package with `CapabilityBinding` frozen dataclass) which does not exist and would collide with the pre-existing single-file module.
3. **ROADMAP §A.12 W1 reconciliation refined** to include W1b close as a first-class delivery row.
4. **New wave-honest limit D.1** (W1 verification scope hole) surfaced: M7 W1 verification receipt this shift covered only W1 close (`fe01e5e` at 06:33Z); missed W1b close (`53645935` at 06:59Z · 26 min later). Candidate CP-M7-W1-POST-3-VERIFICATION covers the remaining 5 W1b deliverables.
5. **POST-2 close matches W0/W1 verification-walk shape**: single-master-commit · no track-a Commit-A · no Commit-C fixup (no seal file references a master SHA).

## 4 · Discoveries not envisioned at planning

1. **The pre-existing W1b module was not surfaced by my earlier W1 verification walk this shift.** The W1 verification receipt (`phase0/m7_w1_verification/verification_receipt_20260916.json` · 2026-09-16T~04:15Z) enumerated the 5 W1 modules (runtime_supervisor + supervisor + governance + job_manifest + kind_registry) all last-touched by commit `fe01e5e` — but did NOT extend enumeration to modules landed by commit `53645935` 26 minutes later. This is a **verification-scope discipline lesson**: when verifying a wave's platform primitives, enumerate every commit within the wave-window, not just the canonically-named wave-close commit. Recorded as wave-honest limit D.1 with a candidate CP-M7-W1-POST-3-VERIFICATION to close the remaining W1b gap.
2. **The 5 unexpected passes in the POST-2 RED drill** (before the discovery) were not a discipline breach — they were the earliest signal from disk that a pre-existing module existed. `test_capability_registry_module_importable PASSED` at RED was the tell. Under strict tests-first discipline, all 27 draft tests should have failed if the mechanism truly did not exist. The 5 passes were the mechanism's ghost. Documenting so future compaction-restarts recognize this pattern.
3. **The owner's 2026-09-16T~05:10Z ruling INTENT** ("case-agnostic capability registry landed with compose-not-modify posture") was ratified by W1b close 3 days earlier. Under premature-invariant discipline this shift's initial approach ("author a new package") was speculative in exactly the sense the owner corrected: applying existing owner law (2026-09-13 case-agnostic correction + W1b already implementing it) is not speculation.

## 5 · Recommendations to make the experience better, in line with the mission

1. **Author CP-M7-W1-POST-3-VERIFICATION next** to close the wave-honest gap D.1. Enumerate + verify from-disk: `services/governance_plane/retention_policy.py` · `services/source_plane/connector.py` · `services/source_plane/synology_file_station.py` · `services/audio_plane_v1/attribute_stream_bundle.py` + L2/L4 contract shells. Same six-check schema as POST-2. Estimated single-shift walk. Ratchet delta 0 if Path α clean.
2. **Extend the M7 W1 verification receipt schema** to enumerate every commit within a wave-window, not just the canonically-named wave-close commit. Update the walk template for future M7 milestone-open verifications.
3. **Do NOT propagate the ratchet delta to POST-2** (per verdict-clean Path α zero-delta). Ratchet stays at 4384 from POST-1 seal.
4. **Continue GPU utilization interleave** at every CP boundary of POST-3-VERIFICATION.

---

## §G · GPU utilization check-in interleave (per grounding brief §G)

**Check-in fired at CP-seal:** `python3 tools/m7_util_72h_orchestrator.py check_in` @ 2026-09-16T~06:00Z.

**Rollup (as of check-in):**
- akki-vm: sampler_alive + workload_alive · telemetry_samples=52 · bench_iterations=224 (ok=224) · per-GPU peak 100% util · peak ~691 W · peak ~70°C.
- akki-vm-ii: sampler_alive + workload_alive · telemetry_samples=50 · bench_iterations=224 (ok=224) · per-GPU peak 100% util · peak ~693 W · peak ~71°C.
- Elapsed: 1.88 h · Remaining: 70.12 h.
- 448 total bench artefacts banked · zero synthetic burn · in-perimeter.
- Report served: `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.

---

## §H · Owner-desk items (carried per §H standing template)

**P1 blocked:** JUMP custody rotation · CD+Visitors admin binds (bramuel vs bramwel) · Amendment 8 · Watch-Learning R-15(b)/16(b)/17(b) · BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · S-24/S-27/S-28/S-29 build charters · D9 receipt-unify · SEC rotations · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine.

**P2 blocked:** SW-10 A.1-A.5 rulings (SW-10 DEFERRED-TO-CLOSE) · Audio-bytes-retention Path A/B/C · R-17(a) non-blocking · Cross-service binding enforcement ruling (§3.2 clause 5 hard-gate authorisation).

**NEW · P2 · Candidate CP-M7-W1-POST-3-VERIFICATION**: verification walk for the remaining 5 W1b deliverables (RetentionPolicy · SourceConnector Protocol · Synology FileStation · AttributeStreamBundle_v0 · L2/L4 shells). Autonomously authorable by same precedent as POST-2. Not blocking any current wave.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
