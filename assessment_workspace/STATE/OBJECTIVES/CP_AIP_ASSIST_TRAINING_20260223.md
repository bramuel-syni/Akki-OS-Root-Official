---
ratified_at_utc: 2026-02-23T16:15:00Z
card_id: CP-AIP-ASSIST-TRAINING
ledger_item: EXECUTION_ORDER.md · Item 5.11.g
authority: SO §6.8 standing authority (owner drop `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md`)
status: PROMOTED — Item 5.11.g open
card_sha256: e5bb78578557107ebe6301ae393ec5618592d8a8f3c01b79eabaeb38385017d3
---

# CP-AIP-ASSIST-TRAINING — Training-run dialogue assistant

**Owner authority:** SO §6.8 (2026-02-23) · owner drop `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md`. Card lands under standing authority once its RED tests exist. **No GO needed.**

## OBJECTIVE

Extend (§1.2 modality-extension) the sealed CP-AIP-ASSIST-CENSUS surface (Item 5.11.f · assist_census_v1) into a **Training-run dialogue assistant** applying the same six binding conditions verbatim to training-run dialogue. The assistant proposes objective + criteria; the owner confirms; the assistant NEVER decides; MOAC criteria are set by the owner's confirmation only at commission time. Placement OUTSIDE the TCB. Every user-facing string is a Content Registry entry.

**Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:** E1 wires the seam INTO Census Autonomy Service; pod is never data path. Training compute + weights + labelled corpus NEVER leave Akki's boundary; no third-party export.

**Anchor to Item 5.12 CP-AIP-LANGUAGE-COGNITION:** the training-run dialogue assistant is the interface through which owner/tenant confirms the frozen commission criteria for the Item 5.12 language-cognition training run (MOAC set: ≥90% per-language accuracy · ≥85% code-switch span accuracy · no-speaker-ID probe passed · abstention reported). This-card's `bank_confirmed_training_turn` boundary callable + `render_training_content_registry_entry` boundary callable ARE the consumer path for Item 5.12 commission dialogue.

## MUST DO

1. **Binding condition (1): No path to any decision** (negative-scan import isolation · §1.2 discipline). The training assistant module MUST NOT import any decision-boundary module. Placement OUTSIDE the TCB is enforced structurally. `canon_ref: SO §6.8 assist_cards binding condition (1) verbatim.`

2. **Binding condition (2): Confirmed turns only banked** (A5.16 receipted provenance). An unconfirmed training-assistant turn MUST NEVER be persisted; every banked turn carries an A5.16 receipt reference. `canon_ref: SO §6.8 assist_cards binding condition (2) verbatim.`

3. **Binding condition (3): Training assistant read-only against Registry** (B5.1 byte-identical training-run commission with/without assistant). The training assistant MUST NEVER mutate the Registry; a training-run commission derived WITH assistant activation is byte-identical to a training-run commission derived WITHOUT assistant activation, given identical Registry state. `canon_ref: SO §6.8 assist_cards binding condition (3) verbatim.`

4. **Binding condition (4): MOAC owner-set only at commission time** (frozen at commission). MOAC criteria are frozen by the owner's confirmation only at commission time. The training assistant NEVER edits MOAC criteria after freeze. `canon_ref: SO §6.8 assist_cards binding condition (4) verbatim + AIP v1.0 §11.6 Training Runs commissioned-job freeze semantics.`

5. **Binding condition (5): Content · chat surface · anchored · gated** (R-32 Content Registry + A5.15 anchor + CON-6 gate). Every user-facing string the training assistant renders is a Content Registry entry with an A5.15 anchor and a CON-6 gate; §6.9 markers over refusal where a marker makes the state honest. `canon_ref: SO §6.8 assist_cards binding condition (5) verbatim.`

6. **Binding condition (6): No learning from dialogue** (L-4/L-5 only admission path). Training-assistant dialogue MUST NEVER feed training material. L-4/L-5 is the only admission path for training material. The training-assistant module exposes ZERO learning-write callables. `canon_ref: SO §6.8 assist_cards binding condition (6) verbatim.`

7. **§1.2 modality-extension composing sealed CP-AIP-ASSIST-CENSUS by identity.** The training assistant module MUST compose the sealed 5.11.f `bank_confirmed_assistant_turn` + `render_content_registry_entry` + `CensusAssistantConfirmedTurn_v1` + `ContentRegistryEntry_v1` by identity — never redeclare. Training-specific carriers (`TrainingAssistantConfirmedTurn_v1` + `TrainingCommissionProposal_v1`) are ADDITIVE. `canon_ref: SO §1.2 modality-extension + §3.8 additive-only.`

8. **Training-run commission freeze at owner confirmation** (owner drop §4 binding condition (4) verbatim + AIP v1.0 §11.6 verbatim). The training assistant proposes training scope options (model choice, data slice, calibration stage, cost/CI quote); the owner confirms; on confirmation, the training commission FREEZES and MOAC becomes owner-set only. Subsequent training-assistant turns MUST NOT re-open the frozen commission — they can propose a NEW commission superseding the prior, never rewrite it. `canon_ref: AIP v1.0 §11.6 commissioned-job freeze.`

9. **Placement OUTSIDE the TCB** (owner drop §placement verbatim). The training-assistant module is not part of the Trusted Computing Base; import-isolation on decision-boundary modules is structurally enforced. `canon_ref: SO §6.8 assist_cards placement clause verbatim.`

10. **`SIX_BINDING_CONDITIONS_POSTURE_TRAINING`** Final 6-tuple pinning the six binding conditions verbatim inside the code carrier — mirror of sealed 5.11.f `SIX_BINDING_CONDITIONS_POSTURE`, retagged for training scope. `canon_ref: SO §6.8 assist_cards binding conditions verbatim.`

## MUST NOT DO

1. **Redeclare sealed CP-AIP-ASSIST-CENSUS symbols** (§1.2 discipline). Compose by identity; never redeclare `bank_confirmed_assistant_turn` / `render_content_registry_entry` / `CensusAssistantConfirmedTurn_v1` / `ContentRegistryEntry_v1` / `SIX_BINDING_CONDITIONS_POSTURE` / `AssistCensusBoundaryRefused` / `UnconfirmedTurnBankRefused` / `UngatedContentRefused`.

2. **Persist an unconfirmed training-assistant turn** (binding condition 2). `bank_confirmed_training_turn` refuses `confirmed_by_owner is False` and refuses missing/malformed `a5_16_receipt_ref` — raises `UnconfirmedTrainingTurnBankRefused`.

3. **Render user-facing content without A5.15 anchor + CON-6 gate** (binding condition 5). `render_training_content_registry_entry` refuses missing/malformed anchors — raises `UngatedTrainingContentRefused`.

4. **Edit MOAC criteria after owner-confirmation freeze** (binding condition 4). `re_edit_frozen_moac` MUST NOT exist as a callable; frozen commission carriers use frozen dataclass semantics.

5. **Import any decision-boundary module** (binding condition 1). Negative-scan import isolation enforces this structurally.

6. **Expose any learning-write callable** (binding condition 6). No `learn_*` / `admit_to_training_*` / `feed_training_*` public names in the module.

7. **Run the assistant inside the E1 pod as data path** (Ruling (b) verbatim). The assistant module has no I/O; boundary callables only take value objects. Any `pod://*` / `/app/*` prefixed refs at training-turn banking are refused per sealed CP-TRACK-4-AUTONOMY-WIRING `PodIsNeverDataPathAtTrack4Error` posture (composed by identity, no redeclaration).

8. **Export training weights / labelled corpus outside Akki's boundary** (Ruling (b) verbatim). The training-assistant module MUST NOT expose any callable that returns weight bytes, corpus payload, or model internals. Enforced by negative-scan on `return_weights` / `export_corpus` / `serialize_model` public names.

## NEW ADDITIVE MODULES

`backend/services/census_autonomy/assist_training_v1.py` (~220 lines):

- **Refusal hierarchy** (composes sealed 5.11.f `AssistCensusBoundaryRefused` by identity — no redeclaration; adds training-specific subclasses):
  - `UnconfirmedTrainingTurnBankRefused` (extends sealed base).
  - `UngatedTrainingContentRefused` (extends sealed base).
  - `FrozenMoacEditRefused` (extends sealed base).
  - `LearningWriteFromDialogueRefused` (extends sealed base).
  - `PodIsNeverDataPathAtAssistTrainingError` (composes CP-TRACK-4 posture by identity).
- **Posture markers (Final str · owner verbatim):**
  - `ASSIST_TRAINING_READONLY_POSTURE` citing binding condition (3) verbatim + B5.1 byte-identity clause.
  - `MOAC_OWNER_SET_ONLY_AT_COMMISSION_POSTURE_TRAINING` citing binding condition (4) verbatim.
  - `NO_LEARNING_FROM_DIALOGUE_POSTURE_TRAINING` citing binding condition (6) verbatim.
  - `PLACEMENT_OUTSIDE_TCB_POSTURE_TRAINING` citing placement clause verbatim.
  - `WEIGHTS_CORPUS_NEVER_LEAVE_AKKI_POSTURE` citing Ruling (b) verbatim.
- **`SIX_BINDING_CONDITIONS_POSTURE_TRAINING`** — Final 6-tuple pinning all six binding conditions verbatim (retagged for training scope).
- **Frozen carriers:**
  - `TrainingAssistantConfirmedTurn_v1` — 8-field frozen dataclass (session_id + tenant_id + role + content_registry_ref + confirmed_by_owner + confirmed_at_utc + a5_16_receipt_ref + proposed_training_commission_ref).
  - `TrainingCommissionProposal_v1` — 6-field frozen dataclass (model_choice_ref + data_slice_ref + calibration_stage_ref + cost_ci_quote_ref + moac_frozen + frozen_at_utc). `moac_frozen` becomes True on owner confirmation; subsequent proposals must reference this as prior via `supersedes` field (append-only supersession, never in-place rewrite).
- **Boundary callables:**
  - `bank_confirmed_training_turn(...)` — refuses `confirmed_by_owner is False`, refuses missing/malformed `a5_16_receipt_ref`, refuses missing `proposed_training_commission_ref`.
  - `render_training_content_registry_entry(...)` — composes sealed 5.11.f `render_content_registry_entry` by identity + adds training-scope validation on `content_registry_ref` prefix.
  - `freeze_training_commission_on_owner_confirm(proposal, owner_confirmation_ref, frozen_at_utc)` — freezes proposal → `moac_frozen=True`; subsequent edits to the frozen carrier raise `FrozenMoacEditRefused`.

## SEALED CARRIERS TO NOT EDIT (§3.8 additive-only · §1.2 modality-extension composing by identity)

- `services/census_autonomy/assist_census_v1.py` (CP-AIP-ASSIST-CENSUS · Item 5.11.f · sealed 2026-02-23T~16:05Z) — all symbols composed by identity, NO redeclaration.
- `services/census_autonomy/track_4_autonomy_wiring_v1.py` (CP-TRACK-4-AUTONOMY-WIRING) — `PodIsNeverDataPathAtTrack4Error` posture composed by identity.
- `services/audio_plane_v1/training_run_boundary_v1.py` (CP-AIP-10-TRAINING-RUNS) — training-run boundary composed by identity for commissioned-job semantics.
- `services/census_autonomy/engine.py` (R-106 sealed).
- All prior CP-AIP-1..10 + CP-CENSUS-THREE-WAVES + CP-SO-6.9-LID-WAVE + CP-ENT-16 + CP-TENANT-SEPARATION modules.

## EXIT (RED-first invariant node IDs)

Minimum 10 RED-first structural pins:

1. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_no_path_to_any_decision_negative_scan_import_isolation` (binding condition 1)
2. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_confirmed_turn_only_banked_a5_16_receipted_provenance` (binding condition 2)
3. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_readonly_registry_b5_1_byte_identical` (binding condition 3)
4. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_moac_owner_set_only_at_commission_freeze_semantics` (binding condition 4)
5. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_content_r32_a515_con6_anchored_gated_honest_marker_over_refusal` (binding condition 5)
6. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_no_learning_from_dialogue_l4_l5_only_admission_path` (binding condition 6)
7. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_frozen_confirmed_turn_carrier_shape` (shape lock · 8-field)
8. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_placement_outside_tcb_posture_marker_present` (placement anchor)
9. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_no_redeclaration_of_sealed_symbols_1_2` (§1.2 discipline · sealed 5.11.f symbols composed by identity)
10. `tests/invariants/test_cp_aip_assist_training.py::test_assist_training_six_binding_conditions_posture_markers_all_present` (owner-verbatim anchor)

## STOP

- STOP if any of the MUST-NOT §§1-8 fires — the seal does not close.
- STOP if `pytest tests/invariants/test_cp_aip_assist_training.py` does not reach GREEN post-authorship.
- STOP if sealed CP-AIP-ASSIST-CENSUS / CP-TRACK-4-AUTONOMY-WIRING / CP-AIP-10-TRAINING-RUNS carriers are edited (SO §3.8 additive-only).
- STOP if double-green `BASELINE_GUARD=1 PYTHONHASHSEED=0` stripped_sha256 does not match byte-identically between sweep_A and sweep_B.

## ANCHORS (§6.3 rule 1 — underlying components this builds on)

- **CP-AIP-ASSIST-CENSUS (Item 5.11.f · SEALED 2026-02-23T~16:05Z)** — sealed `assist_census_v1` module composed by identity for §1.2 modality-extension. This card is the training-side mirror of the census-side.
- **CP-TRACK-4-AUTONOMY-WIRING (Item 5.11.e · SEALED 2026-02-23T~15:22Z)** — `training_runs` job kind + `PodIsNeverDataPathAtTrack4Error` posture composed by identity.
- **CP-AIP-10-TRAINING-RUNS (Item 5.11 pre-wave · SEALED 2026-02-23T~12:10Z)** — training-run boundary + AIP v1.0 §11.6 commissioned-job freeze semantics.
- **CP-ENT-16-PILOT-LICENCE-SEEDS (Item 5.11.b · SEALED)** — pilot licence Compute dial Managed + Frontier dial Your Keys for training-run cost/CI resolution.
- **CP-TENANT-SEPARATION (Item 5.11.d · SEALED)** — tenant custody boundary for training-run per-tenant commission scoping.
- **Owner drop `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md`** — six binding conditions verbatim (2026-02-23).
- **Ruling (b) AKKI-RUNS-IT verbatim (2026-02-23):** E1 wires the seam INTO Census Autonomy Service; pod is never data path; training compute + weights + labelled corpus NEVER leave Akki's boundary.
- **AIP v1.0 §11.2 P179** — `CostQuoteWithCI` + calibration-stage requirement (composed by identity via referenced fields in `TrainingCommissionProposal_v1`).
- **AIP v1.0 §11.6** — commissioned-job freeze semantics.
- **Coupling to Item 5.12 CP-AIP-LANGUAGE-COGNITION (queued):** this-card's `bank_confirmed_training_turn` + `freeze_training_commission_on_owner_confirm` boundary callables ARE the consumer path for the Item 5.12 language-cognition training-run commission dialogue (owner-confirms MOAC set: ≥90% per-language + ≥85% code-switch span + no-speaker-ID probe passed + abstention reported).

## RATIFICATION

Card promoted from `STATE/OBJECTIVES/queued/CP_AIP_ASSIST_TRAINING.md` (drafted 2026-02-23T10:35Z pre-CP-AIP-ASSIST-CENSUS · restructured this-turn to fully-conforming SO §6.2 six-section schema post-5.11.f seal + Item 5.12 coupling anchor added). SO §6.8 standing authority — builds under standing authority once its RED tests exist. No GO needed.

**Card status:** PROMOTED — Item 5.11.g open. card_sha256 computed and pinned at Code Commit-A time.
