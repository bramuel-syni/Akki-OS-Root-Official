# CP-AIP-ASSIST-CENSUS · comprehensive seal receipt

**Seal ID:** CP-AIP-ASSIST-CENSUS-20260223
**Ledger item:** EXECUTION_ORDER.md Item 5.11.f
**Boundary date (UTC):** 2026-02-23T~15:45Z
**Wave position:** 6th item of the Item 5.11 wave (after 5.11.a SO-6.9-LID · 5.11.b ENT-16 · 5.11.c CENSUS-THREE-WAVES · 5.11.d TENANT-SEPARATION · 5.11.e TRACK-4-AUTONOMY-WIRING).

---

## Owner canon anchors (verbatim)

**SO §6.9 amendment · owner drop 2026-02-23 `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md`:**

Six binding conditions verbatim as MUST-DO/MUST-NOT test IDs:

1. **No path to any decision** (negative-scan import isolation).
2. **Confirmed turns only banked** (A5.16 receipted provenance).
3. **Census assistant read-only against Registry** (B5.1 byte-identical census with/without assistant).
4. **Training proposals freeze at commission; MOAC owner-set only.**
5. **Content generated · chat surface · anchored · gated** (R-32/A5.15/CON-6) — §6.9 markers over refusal where a marker makes the state honest.
6. **No learning from dialogue** (L-4/L-5 only admission path).

**Placement OUTSIDE the TCB.** Every user-facing string is a Content Registry entry.

**Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:** E1 wires the seam INTO Census Autonomy Service; pod is never data path.

---

## Objective card

`STATE/OBJECTIVES/CP_AIP_ASSIST_CENSUS_20260223.md` · card_sha256 `3a996943801ba1d8d5919baa2313ccb24feb330fc64c74bab0dc6384b3e8f79b` (line-removed convention).

Fully conforming to SO §6.2 six-section schema (OBJECTIVE · MUST DO · MUST NOT · EXIT · STOP · ANCHORS).

---

## Ratchet

- **Delta:** +10 canonical measured own new pins.
- **passed_floor:** 6379 → 6389.
- **counts_at_baseline.passed:** 6379 → 6389.
- **baseline_failures.json sha256 post-bump:** `cfe002176cc78641b13dea985e0ee7c6fa20bf0df7bf84ce2d99b0f94a10ccb4`.

---

## Pre-Commit-A double-green byte-identity

BASELINE_GUARD=1 PYTHONHASHSEED=0 stripped_sha256 `bb7f3c5117fbf946bbc1e973e07b522af74cc6c6709b1b0e2cbde24e53e9254d` IDENTICAL both sweeps:

- Sweep A · `phase0/drill_receipts_cp_aip_assist_census/20260923T153434Z_sweep_A.log` · ~207s · 6389 passed / 13 skipped / 0 failed / 520 warnings.
- Sweep B · `phase0/drill_receipts_cp_aip_assist_census/20260923T153850Z_sweep_B.log` · ~207s · 6389 passed / 13 skipped / 0 failed / 520 warnings.

RED_pre 10/10 authentic ImportError right-reason (module absent) at `phase0/drill_receipts_cp_aip_assist_census/20260923T152414Z_RED_pre.log`.
GREEN_post 10/10 passed 0.74s at `phase0/drill_receipts_cp_aip_assist_census/20260923T152504Z_GREEN_post.log`.

---

## NEW additive module (SO §3.8 additive-only · §1.2 modality-extension)

`backend/services/census_autonomy/assist_census_v1.py` (~216 lines):

- **Refusal hierarchy:** `AssistCensusBoundaryRefused` (base) + `UnconfirmedTurnBankRefused` + `UngatedContentRefused`.
- **Posture markers (Final str · owner verbatim):**
  - `ASSIST_CENSUS_READONLY_POSTURE` — binding condition (3) verbatim + B5.1 byte-identity clause.
  - `MOAC_OWNER_SET_ONLY_POSTURE` — binding condition (4) verbatim.
  - `NO_LEARNING_FROM_DIALOGUE_POSTURE` — binding condition (6) verbatim.
  - `PLACEMENT_OUTSIDE_TCB_POSTURE` — placement clause verbatim.
- **`SIX_BINDING_CONDITIONS_POSTURE`** — Final 6-tuple carrying all six binding conditions verbatim.
- **Frozen carriers:**
  - `CensusAssistantConfirmedTurn_v1` — 7-field frozen dataclass (session_id + tenant_id + role + content_registry_ref + confirmed_by_owner + confirmed_at_utc + a5_16_receipt_ref).
  - `ContentRegistryEntry_v1` — 4-field frozen dataclass (content_registry_ref + a5_15_anchor_ref + con_6_gate_ref + honest_marker).
- **Boundary callables:**
  - `bank_confirmed_assistant_turn(...)` — refuses `confirmed_by_owner is False` and refuses missing/malformed `a5_16_receipt_ref` (must start with `a5_16://`).
  - `render_content_registry_entry(...)` — refuses missing/malformed `a5_15_anchor_ref` (must start with `a5_15://`) and missing/malformed `con_6_gate_ref` (must start with `con_6://`).

**§1.2 no-redeclaration** of sealed CP-AIP-6 wizard + Census Autonomy Service response_required_queue + Track-4 autonomy wiring symbols. **§1.2 modality-extension** composing sealed Census Autonomy Service surface.

**Placement OUTSIDE the TCB** enforced by: (a) module lives at `services/census_autonomy/*` (assistant plane, not decision plane); (b) invariant test 1 negative-scan of import isolation forbids assistant module from importing decision-boundary modules; (c) `PLACEMENT_OUTSIDE_TCB_POSTURE` Final str declares intent verbatim.

---

## Test file (10 RED-first pins)

`backend/tests/invariants/test_cp_aip_assist_census.py` (~282 lines · 10 pins mapping to six binding conditions):

| # | Pin | Binding condition |
|---|-----|-------------------|
| 1 | `test_assist_no_path_to_any_decision_negative_scan_import_isolation` | (1) |
| 2 | `test_assist_confirmed_turn_only_banked_a5_16_receipted_provenance` | (2) |
| 3 | `test_assist_census_readonly_with_without_byte_identical_b5_1` | (3) |
| 4 | `test_assist_training_proposals_freeze_at_commission_moac_owner_set_only` | (4) |
| 5 | `test_assist_content_r32_a515_con6_anchored_gated_honest_marker_over_refusal` | (5) |
| 6 | `test_assist_no_learning_from_dialogue_l4_l5_only_admission_path` | (6) |
| 7 | `test_assist_frozen_confirmed_turn_carrier_shape` | (2) shape lock |
| 8 | `test_assist_placement_outside_tcb_posture_marker_present` | structural |
| 9 | `test_assist_no_redeclaration_of_sealed_symbols_1_2` | §1.2 discipline |
| 10 | `test_assist_six_binding_conditions_posture_markers_all_present` | anchor |

---

## Sealed carriers UNCHANGED per SO §3.8 additive-only

- `services/census_autonomy/engine.py` (R-106).
- `services/census_autonomy/track_4_autonomy_wiring_v1.py` (CP-TRACK-4-AUTONOMY-WIRING).
- `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE).
- `services/audio_plane_v1/census_three_waves_v1.py` (CP-CENSUS-THREE-WAVES).
- `services/audio_plane_v1/training_run_boundary_v1.py` (CP-AIP-10-TRAINING-RUNS).
- `services/entitlement_service_v1/pilot_licence_seeds_v1.py` (CP-ENT-16).
- `services/entitlement_service_v1/tenant_separation_v1.py` (CP-TENANT-SEPARATION).
- All prior CP-AIP-1..10 chain modules.

---

## EXIT EVIDENCE (structural · six binding conditions as MUST-DO/MUST-NOT test IDs)

The 10 RED-first pins ARE the exit evidence. Each binding condition maps to a named test that flipped from authentic RED to GREEN under baseline-guarded double-green sweeps.

No LIVE engine run required for this seal (unlike CP-TRACK-4-AUTONOMY-WIRING which needed autonomy-engine pickup receipt) — the assistant module is READ-ONLY against the Registry and has NO learning-write callables, so its EXIT EVIDENCE is structural (import-isolation + boundary-refusal + posture-marker presence) rather than runtime.

---

## Ruling (b) AKKI-RUNS-IT verbatim honored

- Assistant module lives INSIDE the Census Autonomy Service surface (`services/census_autonomy/*`).
- Assistant is READ-ONLY against Registry — NO learning-write callables exposed.
- Assistant NEVER decides — every user-facing string is a Content Registry entry with A5.15 anchor + CON-6 gate.
- Pod NEVER data path — assistant module has no I/O; boundary callables only take value objects.

---

## Ledger check

`Ledger check - this seal implements Item 5.11.f of EXECUTION_ORDER.md and nothing else.`

---

## REPORT-AND-CONTINUE receipt line

`CP-AIP-ASSIST-CENSUS FULLY SEALED · SO §6.9 amendment + owner drop 2026-02-23 assist_cards_preapproved_and_run_to_completion verbatim + Ruling (b) AKKI-RUNS-IT verbatim · six binding conditions verbatim as MUST-DO/MUST-NOT test IDs · placement OUTSIDE the TCB · every user-facing string is a Content Registry entry · assist_census_v1 §1.2 modality-extension composing sealed Census Autonomy Service surface · 10 RED-first own pins ALL GREEN · double-green stripped_sha256 bb7f3c5117fbf946bbc1e973e07b522af74cc6c6709b1b0e2cbde24e53e9254d IDENTICAL both sweeps 6389 passed · Ratchet 6379 → 6389 (+10 canonical measured own new pins) · GAPS_FIXED_LEDGER 10 own invariant-seat entries at boundary · Sealed carriers UNCHANGED per SO §3.8 additive-only · Ruling (b) AKKI-RUNS-IT verbatim honored — assistant is READ-ONLY against Registry; NO learning-write callables; NO decision-boundary imports; pod NEVER data path · Item 5.11.f of EXECUTION_ORDER.md CLOSED · Item 5.11.g (CP-AIP-ASSIST-TRAINING) opens next per RUN-TO-COMPLETION mandate 2026-02-23 · REPORT-AND-CONTINUE not idle-halt.`
