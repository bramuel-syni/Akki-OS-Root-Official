# CP-AIP-10-TRAINING-RUNS — comprehensive receipt · LAST BY CONSTRUCTION

**Seal boundary:** 2026-02-23T~11:50Z · **AIP v1.0 §11.6 + §11.5 + Ruling (b) AKKI-RUNS-IT verbatim** · **§1.2 modality-extension** · **RUN-TO-COMPLETION mandate ACTIVE**.

## §1 — What sealed

**AIP v1.0 §11.6 Training-Runs commissioned-job compose-boundary** GREEN · **§11.5 per-example-provenance-through-training** enforced structurally · **Ruling (b) AKKI-RUNS-IT verbatim** Census-Autonomy-Service registration seam with pod-never-data-path structural refusal. §1.2 modality-extension composing sealed **CP-AIP-8** `enter_sr_with_planner_result` + `PlanWithoutCalibrationAtSRBoundary` + sealed **CP-AIP-7** planner-boundary + sealed **CP-M6-7-3** `CostQuoteWithCI` + sealed **CP-AIP-4** `pretraining_contract_v1` `HONEST_GAP_V1_POSTURE` pattern.

## §2 — Ratchet

| Stage | passed | skipped | failed | delta |
|---|---:|---:|---:|---:|
| Pre-authorship (post-CP-AIP-9) | 6313 | 13 | 0 | — |
| Post-CP-AIP-10 RED-first authorship | 6321 | 13 | 0 | +8 canonical measured |
| Ratchet floor **post-seal** | **6321** | — | — | — |

- `baseline_failures.json` sha256 post-bump: `0c7968cdf19694f301e67dc28fee7180e693b0e1f7053fbd3e8226fef5490abd`.

## §3 — Modules added

**One new module under `backend/services/audio_plane_v1/`:**

- `training_run_boundary_v1.py` (~347 lines):
  - `TrainingRunCommissionedJobRefused` base exception + 6 subclasses (§11.6 P189a + P190a-e + §11.5 P185a + Ruling (b) verbatim).
  - `PerStratumResult_v1` frozen dataclass (§11.6 P190e Literal `{"passed","failed"}`).
  - `CompletionCertificate_v1` frozen dataclass (§11.6 P190a-d 4-field verbatim).
  - `TrainingManifestExampleRow_v1` frozen dataclass (§11.5 P185a provenance_ref).
  - `TrainingManifest_v1` (append_row refuses empty provenance_ref).
  - `RightsLapseDetector_v1` frozen dataclass (§11.5 P187 frozenset return).
  - `TrainingRunCensusAutonomyRegistration_v1` frozen dataclass (Ruling (b) 4-field verbatim).
  - `register_training_run_as_census_autonomy_job` boundary callable (refuses `pod://` and `/app/` prefixed refs).
  - `open_training_run` boundary callable composing sealed CP-AIP-8.
  - `HEAVY_FINETUNE_DEFERRED_TO_COMMISSIONED_JOB_POSTURE` Final marker (§11.6 + §1.4 verbatim).
  - `POD_IS_NEVER_DATA_PATH_POSTURE` Final marker (Ruling (b) verbatim).

## §4 — Test authorship (RED-first · GREEN post)

- **RED_pre:** 8/8 failed 0.78s (authentic `ImportError` right-reason — module did not exist).
- **GREEN_post:** 8/8 passed 0.73s.
- Test file: `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py`.

## §5 — Double-green byte-identity (BASELINE_GUARD=1 PYTHONHASHSEED=0)

- **sweep_A_invariants** (re-run): 6330 passed / 13 skipped / 0 failed / 520 warnings / 201.15s
- **sweep_B_invariants**: 6330 passed / 13 skipped / 0 failed / 520 warnings / 198.48s
- **stripped_sha256:** `92d09b7d7f27897fdc7827bbcde23f584cdcb46c3f8be56f4cb23e150ecc7378` IDENTICAL both sweeps (12458 stripped bytes).

## §6 — Objective card

`STATE/OBJECTIVES/CP_AIP_10_TRAINING_RUNS.md` (fully-conforming SO §6.2 · promoted from `queued/` · card_sha256 `f1cd77d7c2cfae3bd68b4aa21dc7cfc764f076c1c5c962049771f8e8d8fb5246` · 6 required sections: OBJECTIVE + MUST DO + MUST NOT + EXIT + STOP + ANCHORS).

## §7 — Milestone-seal continuity (SO §6.9(5) AMENDED · 2nd application)

- **Code bundle** (this-seal): `continuity_bundles/code_20260923T114743Z_CP_AIP_10.bundle` · 18,285 KiB · sha256 `48b2c169e5d04985f1754ff17d9ca0ce9688bd9c6067ba1dc9ca1252c7b08a41` @ `programme/track-a` `8ef25c1`.
- **State bundle** (post-Commit-C fixup): PENDING — emitted after State Commit-C fixup lands.

## §8 — Owner Ruling (b) AKKI-RUNS-IT posture (verbatim)

> "ALL Akki-based training + census EXECUTION runs INSIDE the live Akki OS system — via the Census Autonomy Service / commissioned-job path — within the tenant compute + custody boundary. Training compute + model weights + labelled corpus never leave Akki's boundary; no third-party export. E1's role = build and WIRE the seams INTO the Census Autonomy Service so Akki runs them autonomously — then STEP BACK. E1's pod is never the training host and never a data path."

**Applied at this seal:** the `register_training_run_as_census_autonomy_job` boundary structurally refuses (`PodAsDataPathAtRegistrationError` · `PodAsTrainingHostAtRegistrationError`) any `data_source_adapter_ref` or `engine_response_queue_ref` starting with `pod://` or `/app/` prefix. Heavy fine-tune runs DEFERRED to commissioned-job contract per §1.4 measured cost/compute receipt (`HEAVY_FINETUNE_DEFERRED_TO_COMMISSIONED_JOB_POSTURE` Final marker).

## §9 — 5-commit seal chain (in flight)

| # | Commit | SHA | Branch | Status |
|---|---|---|---|---|
| 1 | Code Commit-A | `8ef25c1` | `programme/track-a` | ✅ LANDED |
| 2 | /app companion A | `a47b3ab03` | `main` | ✅ LANDED |
| 3 | State Commit-B | *(this bank)* | `master` | 🟡 PENDING |
| 4 | State Commit-C fixup | *(pending)* | `master` | 🟡 PENDING |
| 5 | /app companion C | *(pending)* | `main` | 🟡 PENDING |
| 6 | State mini-bank | *(pending)* | `master` | 🟡 PENDING |

## §10 — Ledger check

**This seal implements Item 5.10 of `EXECUTION_ORDER.md` and nothing else.** Additive-only. No sealed carrier edit. RED-first · terminal pytest only · BASELINE_GUARD double-green byte-identical stripped_sha256 · SO §6.9(5) AMENDED continuity bundles.
