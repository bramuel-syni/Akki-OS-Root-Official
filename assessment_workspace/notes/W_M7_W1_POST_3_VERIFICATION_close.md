READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M7-W1-POST-3-VERIFICATION · Wave close · 2026-09-16T~06:20Z

**Wave:** W-M7-W1-POST-3-VERIFICATION (M7 W1-family wave-window residual verification walk).
**Type:** VERIFICATION WALK · zero-delta close · SO §4.2 wave-window commit enumeration discipline applied.
**Verdict:** Path α · CLEAN VERIFICATION.
**Predecessor:** CP-M7-W1-POST-2 · Capability Registry CLOSED · master `cb061265`.
**Track-a HEAD at close:** `2c7a8f0c6157d4103feeebad1171a3bdc92d952c` (unchanged · verification walk).
**Master HEAD at close:** to be recorded post-Commit-B.
**Ratchet floor at close:** **4384** (unchanged · verification walk).

---

## 1 · Progress made

Under the newly-ratified **SO §4.2 · Verification-walk scope discipline · wave-window commit enumeration** (banked same shift · same commit), computed the W1-family wave-window and enumerated every commit + first-added `services/` / `tests/invariants/` file.

**Wave-window (from `programme/track-a` git log):**
- Open anchor: **CP0.a + W0 close** · `44795f3f` · 2026-09-13T06:05:55Z.
- Close anchors: **W1 close** `fe01e5e` at 06:33:22Z (+110 · ratchet 3282 → 3392) · **W1b close** `53645935` at 06:59:30Z (+100 · ratchet 3392 → 3492) · **W1c close** `e1712a1` at 07:16:30Z (+11 · ratchet 3492 → 3503).
- Next-family open: **W-REGISTRY-EXTENSION-G3** `33edf56b` at 10:34:08Z (starts M2 · closes W1-family window).

**Enumerated files (from `git show --diff-filter=A`):**

- **W1 close (`fe01e5e`)** — 5 platform kernel modules: `runtime_supervisor` · `supervisor` · `governance` · `job_manifest` · `kind_registry`. **Verified at W-M7-W1-VERIFICATION** (2026-09-16T~04:15Z · Path α clean · master `997d8398`).
- **W1b close (`53645935`)** — 8 module additions: `attribute_stream_bundle/__init__.py` · **`capability_registry.py`** (verified at POST-2) · `contract_shells/__init__.py` · `governance_plane/__init__.py` · `governance_plane/retention_policy.py` · `source_plane/__init__.py` · `source_plane/connector.py` · `source_plane/synology_file_station.py` · plus 6 test files.
- **W1c close (`e1712a16`)** — 1 test file: `test_w1c_platform_integration_proof.py` (662 L · +11 invariants · end-to-end integration proof · no new services/ modules).

**This POST-3 walk covers the residual not covered by prior verifications:**
- `services/governance_plane/retention_policy.py` (+ `__init__.py`).
- `services/source_plane/connector.py` (SourceConnector Protocol + ReadOnlyGuard + SourceHandle + write-refusal semantics + `__init__.py`).
- `services/source_plane/synology_file_station.py` (interface-only connector).
- `services/attribute_stream_bundle/__init__.py` (AttributeStreamSchema + AttributeStreamBundle_v0 + registry).
- `services/contract_shells/__init__.py` (TargetOutcome_v0 · StratumAcceptance · CommissionSpec · Milestone · WorkerLane · WorkerJD frozen dataclasses).
- `tests/invariants/test_w1c_platform_integration_proof.py` (compose test suite).

**Six from-disk checks (C.1–C.6) all clean per module:**

| Module | C.1 surface | C.3 case-agnostic | C.4 unchanged | C.6 no-banned-tokens |
|---|---|---|---|---|
| `governance_plane/retention_policy.py` | 7-name `__all__` (RetentionRegime · RetentionPolicy · RetentionMismatch · register_policy · get_policy · check_write_admissible · _reset_policies_for_tests) | 0 domain tokens | `2026-09-13T06:59:30Z 5364593` | ✅ |
| `source_plane/connector.py` | 6-name `__all__` (SourceConnector · SourceHandle · ReadOnlyGuard · SourceConnectorWriteRefused · is_read_only_method_name · WRITE_METHOD_PATTERNS) | 0 domain tokens | `2026-09-13T06:59:30Z 5364593` | ✅ |
| `source_plane/synology_file_station.py` | 2-name `__all__` (SynologyFileStationConnector · NotConfiguredForRuntime) | 0 domain tokens | `2026-09-13T06:59:30Z 5364593` | ✅ |
| `attribute_stream_bundle/__init__.py` | 6-name `__all__` (AttributeStreamSchema · AttributeStreamBundle_v0 · register_schema · get_schema · SchemaNotRegistered · _reset_schemas_for_tests) | 0 domain tokens | `2026-09-13T06:59:30Z 5364593` | ✅ |
| `contract_shells/__init__.py` | 6-name `__all__` (TargetOutcome_v0 · StratumAcceptance · CommissionSpec · Milestone · WorkerLane · WorkerJD) | 0 domain tokens | `2026-09-13T06:59:30Z 5364593` | ✅ |
| `test_w1c_platform_integration_proof.py` | integration compose-test suite (662 L · +11 invariants) | N/A (test file) | `2026-09-13T07:16:30Z e1712a1` | ✅ |

**C.2 · Invariant tests present and pass**: `111 passed in 1.13s` under `python -m pytest -q` (file-scoped) across 7 W1b+W1c test files.

Machine-readable receipt: `phase0/m7_w1_post_3_verification/verification_receipt_20260916.json`.

## 2 · How much to go

- **W-M7-W1-POST-3-VERIFICATION** — CLOSED this shift (Path α clean · zero-delta).
- **W1-family wave-window now fully verified** across three closes (W1 + W1b + W1c). No further POST-* verification walks needed for W1-family.
- **W2 · Mount + run vertical slice** — BLOCKED-ON-OWNER unchanged (NAS reach · HF token · 3-station selection · RetentionPolicy Path A/B/C).
- **W-M7-UTILIZATION-72H** — LIVE · elapsed 2.04 h · remaining 69.96 h · 242+242 bench iterations banked · peak 100% GPU util.
- **Next unblocked-and-buildable M7 items** (autonomous continuation per owner directive "continue autonomously through whatever is shape-safe under existing owner law"):
  1. **Next verification walk candidate**: M2 wave-window (`33edf56b` W-REGISTRY-EXTENSION-G3 open .. next-milestone-open) under the newly-ratified SO §4.2 discipline. Under the case-agnostic doctrine, verify from-disk that the 9 M2 sub-wave closes still enforce their contracts.
  2. **Case-agnostic kernel completion** (per SO §4.2 residual scope): candidate CP-M7-W1-POST-4-VERIFICATION covers the M2 wave-window; candidate CP-M7-W1-POST-5-VERIFICATION covers the M3 wave-window; etc. This is systematic verification of every milestone's wave-window that has not yet had a formal-milestone-open verification walk.

## 3 · Decisions taken

1. **SO §4.2 standing verification rule ratified** same shift (in the SO commit accompanying this POST-3 walk): wave-window commit enumeration is the default verification discipline going forward.
2. **W1-family wave-window fully covered this shift** across three separate walks (M7-W1-VERIFICATION for W1 close · POST-2 for W1b capability_registry · POST-3 for the residual 5 W1b modules + W1c integration proof). Coverage delta over prior walks is +6 primary items.
3. **111 W1b+W1c invariants confirmed pass** as of current-shift tree.
4. **All 5 W1b modules unchanged since W1b close** commit `5364593` 2026-09-13T06:59:30Z. Zero drift.
5. **W1c integration proof unchanged** since W1c close commit `e1712a1` 2026-09-13T07:16:30Z. Zero drift.
6. **POST-3 close matches W0/W1/POST-2 verification-walk shape**: single-master-commit · no track-a Commit-A · no Commit-C fixup (no seal file references a master SHA).

## 4 · Discoveries not envisioned at planning

1. **The `contract_shells` module carries 6 case-specific frozen dataclasses** (TargetOutcome_v0 · StratumAcceptance · CommissionSpec · Milestone · WorkerLane · WorkerJD) — these are the type-shells that ROADMAP §A.5, §A.7, §A.9 referenced as case-agnostic W1 deliverables. They landed at W1b close as **Type shells only** (no behaviour), which is the correct case-agnostic minimum: type + no closed-enum + no case-specific interpretation. Downstream mounting jobs supply their case-specific fills.
2. **`services/source_plane/connector.py` implements the SourceConnector Protocol as a genuine Python `typing.Protocol` + `WRITE_METHOD_PATTERNS` deny-list.** The `is_read_only_method_name()` helper enforces read-only method naming conventions at import-time via `SourceConnectorWriteRefused` — this is a compose-safe boundary (not a hard-gate on dispatch). The pattern generalises well beyond NAS/S3/HTTP; case-agnostic.
3. **`services/source_plane/synology_file_station.py::NotConfiguredForRuntime`** — this is a *deferred-configuration* pattern: the connector CLASS exists (interface-only), but any runtime instantiation raises `NotConfiguredForRuntime` until owner-ratified deps + credentials land. This is a clean way to ship interface freezes ahead of external-input unblocks; W2 will use this pattern.
4. **The wave-window enumeration is 6 primary items** — but the 6 primary items were already correctly-implemented at W1b/W1c close. The lesson is not "we need more code"; it's "we need better verification-scope discipline to see what's already there". SO §4.2 (ratified this shift) codifies that lesson.

## 5 · Recommendations to make the experience better, in line with the mission

1. **Next autonomous walk candidate**: **CP-M7-W1-POST-4-VERIFICATION · M2 wave-window under SO §4.2** — enumerate every M2 close commit (SW1..SW7..SW15 in the tree · roughly `451ef2bb..95d688cd` at 2026-09-13T18:51..19:54Z) + apply the six-check schema to each. Estimated single-shift walk if all Path α clean; owner-visible outcome is "M2 wave-window fully verified under the new discipline".
2. **Do NOT auto-instantiate `SynologyFileStationConnector`** in any pre-W2 tooling — it correctly raises `NotConfiguredForRuntime` until W2 unblock quartet lands. Wave-honest signal preserved.
3. **Continue GPU utilization interleave** at every future CP boundary.

---

## §G · GPU utilization check-in interleave (per grounding brief pattern)

**Check-in fired at POST-3 CP-seal:** `python3 tools/m7_util_72h_orchestrator.py check_in` @ 2026-09-16T~06:20Z.

**Rollup (as of check-in):**
- akki-vm: sampler_alive + workload_alive · telemetry_samples=54 · bench_iterations=242 (ok=242) · per-GPU peak 100% util · peak ~691 W · peak ~70°C.
- akki-vm-ii: sampler_alive + workload_alive · telemetry_samples=54 · bench_iterations=242 (ok=242) · per-GPU peak 100% util · peak ~693 W · peak ~71°C.
- Elapsed: 2.04 h · Remaining: 69.96 h.
- 484 total bench artefacts banked · zero synthetic burn · in-perimeter.
- Report served: `https://akki-reuse-assess.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.

---

## §H · Owner-desk items (carried per §H standing template)

**P1 blocked** (unchanged): JUMP custody rotation · CD+Visitors admin binds · Amendment 8 · Watch-Learning R-15(b)/16(b)/17(b) · BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · S-24/S-27/S-28/S-29 build charters · D9 receipt-unify · SEC rotations · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine.

**P2 blocked** (unchanged): SW-10 A.1-A.5 rulings · Audio-bytes-retention Path A/B/C · R-17(a) · Cross-service binding enforcement ruling (§3.2 clause 5 hard-gate).

**P2 CLEARED this shift**: candidate CP-M7-W1-POST-3-VERIFICATION for remaining 5 W1b deliverables → CLEARED (this walk).

**NEW · P2 · Candidate CP-M7-W1-POST-4-VERIFICATION**: M2 wave-window verification under SO §4.2. Autonomously authorable next-shift.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
