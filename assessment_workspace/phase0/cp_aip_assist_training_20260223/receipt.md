# CP-AIP-ASSIST-TRAINING · comprehensive seal receipt

**Seal ID:** CP-AIP-ASSIST-TRAINING-20260223
**Ledger item:** EXECUTION_ORDER.md Item 5.11.g
**Boundary date (UTC):** 2026-02-23T~16:30Z
**Wave position:** 7th item of the Item 5.11 wave (final item before Item 5.12 CP-AIP-LANGUAGE-COGNITION SPEC ENHANCEMENT).

---

## Owner canon anchors (verbatim)

**SO §6.9 amendment · owner drop 2026-02-23 `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md`:**

Six binding conditions verbatim applied to training-run dialogue as MUST-DO/MUST-NOT test IDs:

1. **No path to any decision** (negative-scan import isolation).
2. **Confirmed turns only banked** (A5.16 receipted provenance).
3. **Training assistant read-only against Registry** (B5.1 byte-identical training-run commission with/without assistant).
4. **MOAC criteria owner-set only at commission time** (frozen at owner confirmation).
5. **Content generated · chat surface · anchored · gated** (R-32/A5.15/CON-6).
6. **No learning from dialogue** (L-4/L-5 only admission path).

Placement OUTSIDE the TCB. Every user-facing string is a Content Registry entry.

**Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:** E1 wires the seam INTO Census Autonomy Service; pod is never data path. Training compute + weights + labelled corpus NEVER leave Akki's boundary; no third-party export.

---

## Objective card

`STATE/OBJECTIVES/CP_AIP_ASSIST_TRAINING_20260223.md` · card_sha256 `e5bb78578557107ebe6301ae393ec5618592d8a8f3c01b79eabaeb38385017d3` (line-removed convention).

Fully conforming to SO §6.2 six-section schema (OBJECTIVE · MUST DO · MUST NOT · EXIT · STOP · ANCHORS).

---

## Ratchet

- **Delta:** +10 canonical measured own new pins.
- **passed_floor:** 6389 → 6399.
- **counts_at_baseline.passed:** 6389 → 6399.
- **baseline_failures.json sha256 post-bump:** `7a13a04a96e120ca403878e3cb985c41d284ef4fdde80377656a9ee93ade7c69`.

---

## Pre-Commit-A double-green byte-identity

BASELINE_GUARD=1 PYTHONHASHSEED=0 stripped_sha256 `b74d807fa2f6cc77240c659fad5f87690e2e3d38bdb865dae77d7b512a5dfdc2` IDENTICAL both sweeps:

- Sweep A (post-vendor-sync) · `phase0/drill_receipts_cp_aip_assist_training/20260923T162107Z_sweep_A_post_vendor_sync.log` · ~209s · 6399 passed / 13 skipped / 0 failed / 520 warnings.
- Sweep B · `phase0/drill_receipts_cp_aip_assist_training/20260923T162500Z_sweep_B.log` · ~209s · 6399 passed / 13 skipped / 0 failed / 520 warnings.

**Same-slice cure:** vendored twin file_count 1066→1067 mid-slice sync via `tools/prod_vendor_sync.py` resolved `test_vendored_tree_mirrors_spine` failure detected at first Sweep A (20260923T161705Z_sweep_A.log — 1 failure). Second Sweep A post-sync clean.

RED_pre 10/10 authentic ImportError right-reason (module absent) at `phase0/drill_receipts_cp_aip_assist_training/20260923T161609Z_RED_pre.log`.
GREEN_post 10/10 passed 0.73s at `phase0/drill_receipts_cp_aip_assist_training/20260923T161617Z_GREEN_post.log`.

---

## NEW additive module (SO §3.8 additive-only · §1.2 modality-extension composing sealed CP-AIP-ASSIST-CENSUS by identity)

`backend/services/census_autonomy/assist_training_v1.py` (~232 lines):

- **Refusal hierarchy** (extends sealed CP-AIP-ASSIST-CENSUS `AssistCensusBoundaryRefused` base by identity):
  - `UnconfirmedTrainingTurnBankRefused`.
  - `UngatedTrainingContentRefused`.
  - `FrozenMoacEditRefused`.
  - `LearningWriteFromDialogueRefused`.
  - `PodIsNeverDataPathAtAssistTrainingError`.
- **Posture markers (Final str · owner verbatim):**
  - `ASSIST_TRAINING_READONLY_POSTURE` — binding condition (3) verbatim + B5.1 byte-identity clause.
  - `MOAC_OWNER_SET_ONLY_AT_COMMISSION_POSTURE_TRAINING` — binding condition (4) verbatim.
  - `NO_LEARNING_FROM_DIALOGUE_POSTURE_TRAINING` — binding condition (6) verbatim.
  - `PLACEMENT_OUTSIDE_TCB_POSTURE_TRAINING` — placement clause verbatim.
  - `WEIGHTS_CORPUS_NEVER_LEAVE_AKKI_POSTURE` — Ruling (b) verbatim.
- **`SIX_BINDING_CONDITIONS_POSTURE_TRAINING`** — Final 6-tuple retagged for training scope.
- **Frozen carriers:**
  - `TrainingAssistantConfirmedTurn_v1` — 8-field frozen dataclass.
  - `TrainingCommissionProposal_v1` — 6-field frozen dataclass with `moac_frozen` boolean + `frozen_at_utc`.
- **Boundary callables:**
  - `bank_confirmed_training_turn(...)` — refuses unconfirmed turns + missing/malformed a5_16 refs + pod://* + /app/* refs.
  - `render_training_content_registry_entry(...)` — composes sealed 5.11.f `render_content_registry_entry` by identity.
  - `freeze_training_commission_on_owner_confirm(...)` — freezes proposal → moac_frozen=True; subsequent freeze attempts refused.

**§1.2 no-redeclaration** of 18 sealed symbols (CP-AIP-ASSIST-CENSUS + CP-TRACK-4-AUTONOMY-WIRING + CP-AIP-10-TRAINING-RUNS). **§1.2 modality-extension** composing sealed Census Autonomy Service surface.

---

## Test file (10 RED-first pins)

`backend/tests/invariants/test_cp_aip_assist_training.py` (~466 lines · 10 pins mapping to six binding conditions applied to training):

| # | Pin | Binding condition |
|---|-----|-------------------|
| 1 | `test_assist_training_no_path_to_any_decision_negative_scan_import_isolation` | (1) |
| 2 | `test_assist_training_confirmed_turn_only_banked_a5_16_receipted_provenance` | (2) |
| 3 | `test_assist_training_readonly_registry_b5_1_byte_identical` | (3) |
| 4 | `test_assist_training_moac_owner_set_only_at_commission_freeze_semantics` | (4) |
| 5 | `test_assist_training_content_r32_a515_con6_anchored_gated_honest_marker_over_refusal` | (5) |
| 6 | `test_assist_training_no_learning_from_dialogue_l4_l5_only_admission_path` | (6) |
| 7 | `test_assist_training_frozen_confirmed_turn_carrier_shape` | (2) shape lock |
| 8 | `test_assist_training_placement_outside_tcb_posture_marker_present` | structural |
| 9 | `test_assist_training_no_redeclaration_of_sealed_symbols_1_2` | §1.2 discipline |
| 10 | `test_assist_training_six_binding_conditions_posture_markers_all_present` | anchor |

---

## Sealed carriers UNCHANGED per SO §3.8 additive-only

- `services/census_autonomy/assist_census_v1.py` (CP-AIP-ASSIST-CENSUS · sealed 5.11.f) — composed by identity for all shared primitives.
- `services/census_autonomy/track_4_autonomy_wiring_v1.py` (CP-TRACK-4-AUTONOMY-WIRING · sealed 5.11.e) — `PodIsNeverDataPathAtTrack4Error` posture composed by identity.
- `services/audio_plane_v1/training_run_boundary_v1.py` (CP-AIP-10-TRAINING-RUNS · sealed).
- `services/census_autonomy/engine.py` (R-106 sealed).
- All prior sealed carriers untouched.

---

## EXIT EVIDENCE (structural)

No LIVE engine run required — the training-assistant module is READ-ONLY against the Registry, has NO learning-write callables, and has NO weight/corpus export callables. EXIT EVIDENCE is structural: import-isolation + boundary-refusal + posture-marker presence + frozen-carrier shape lock. The 10 RED-first pins ARE the exit evidence.

---

## Ruling (b) AKKI-RUNS-IT verbatim honored

- Training-assistant module lives INSIDE the Census Autonomy Service surface (`services/census_autonomy/*`).
- Training assistant is READ-ONLY against Registry — NO learning-write callables exposed.
- Training assistant NEVER decides — every user-facing string is a Content Registry entry with A5.15 anchor + CON-6 gate.
- Pod NEVER data path — `pod://*` + `/app/*` refused at all boundary callables via `PodIsNeverDataPathAtAssistTrainingError`.
- **Weights + corpus + compute stay in Akki's boundary** — module exposes ZERO callables returning weight bytes / corpus payload / model internals. Enforced by negative-scan on `return_weights` / `export_corpus` / `serialize_model` public names.

---

## Anchor to Item 5.12 CP-AIP-LANGUAGE-COGNITION (queued at `STATE/OBJECTIVES/queued/CP_AIP_LANGUAGE_COGNITION.md`)

This-card's `bank_confirmed_training_turn` + `freeze_training_commission_on_owner_confirm` boundary callables ARE the consumer path for Item 5.12 language-cognition training-run commission dialogue. Owner confirms MOAC set: ≥90% per-language accuracy + ≥85% code-switch span accuracy + no-speaker-ID probe passed + abstention reported. The frozen `TrainingCommissionProposal_v1` carrier IS the frozen-at-commission MOAC contract for Item 5.12.

---

## Ledger check

`Ledger check - this seal implements Item 5.11.g of EXECUTION_ORDER.md and nothing else.`
