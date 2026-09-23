---
card_id: CP_AIP_ASSIST_TRAINING
title: Training Assistant · objective-shape-and-evolve dialogue as first-class Training-Runs-Service behavior · §1.2 extension of sealed CP-AIP-6 Objective Wizard agent interface + CP-AIP-10 training-run contract seat
ratified_at_utc: 2026-02-23T10:35:00Z
ratified_by: Owner Standing Directive 1 (2026-02-23) verbatim: "This is the work of the assistants in census and training. Card two objectives (on-ledger, owner-directed, not PARKED): CP-AIP-ASSIST-CENSUS and CP-AIP-ASSIST-TRAINING."
card_sha256: DRAFT-PENDING-COMMIT-B
milestone_status: DRAFT (owner-directed · not PARKED · on active ledger · card draft banked at CP-AIP-9 boundary for review in CP-AIP-10 REPORT-AND-CONTINUE · ratification then build)
---

# CP-AIP-ASSIST-TRAINING — Training Assistant

## OBJECTIVE

Extend (§1.2 modality-extension, NOT parallel) the sealed CP-AIP-6 Objective Wizard agent interface + the CP-AIP-10 training-run contract seat (once sealed) + sealed CP-AIP-8 Sampling-and-Reflection boundary + sealed CP-AIP-7 Target-Outcome planner boundary into a **Training Assistant** that conducts the shape-and-evolve dialogue with tenant/owner as **first-class Training-Runs-Service behavior**.

The assistant runs **inside Akki autonomy** (not the E1 pod) per Ruling (b) 2026-02-23: proposes training scope options (model choice, data slice, calibration stage, cost/CI quote), refines against tenant custody + ENT-16 pilot licence (Compute dial Managed, Frontier dial Your Keys) + budget constraints, records each turn as a one-record receipted ledger entry, carries **§6.9 markers** rather than refusing where a marker makes the state honest, and re-derives the training objective as new leads land (e.g., the google-transcripts corpus census result, the LID admission-gate agreement number).

`canon_ref: AIP v1.0 §1.2 modality-extension + §8 Objective Wizard + §10 Target Outcome + §11 Sampling-and-Reflection + §11.6 Training Runs + §16.2 gate_policy + §1.4 cost/compute receipt + §1.5 unrepresentable-not-policed + SO §6.9 desk discipline + Ruling (b) 2026-02-23 verbatim + Standing Directive 1 2026-02-23 verbatim.`

**Extends sealed carriers (unchanged per SO §3.8):**
- `services.wizard.objective_compile.compile_target_outcome` + `compile_collection_schema` (CP-AIP-6 · sealed)
- `services.audio_plane_v1.target_outcome_planner_boundary_v1` (CP-AIP-7 · sealed)
- `services.audio_plane_v1.sampling_reflection_boundary_v1` (CP-AIP-8 · sealed)
- CP-AIP-10 training-run contract seat (**pending; sealed at next boundary**)
- ENT-16 pilot licence seed (**pending; SO-6.9 wave item f**)

## MUST DO

1. **Assistant-turn record shape (frozen carrier)** — every dialogue turn is stored as a `TrainingAssistantTurn_v0` frozen record: `{turn_id · session_id · tenant_id · role: 'assistant' | 'owner' · content · proposed_training_delta · rationale · markers_carried: [] · superseded_by: turn_id | None · cost_ci_snapshot · calibration_stage_ref · created_at_utc}`. Additive alongside sealed `ObjectiveSession_v0` (CP-AIP-6) and CP-AIP-10 training contract.
2. **Proposal-without-rationale refused** — same shape as CP-AIP-ASSIST-CENSUS.
3. **Proposal-without-cost-CI refused** — a proposed training delta MUST reference a `CostQuoteWithCI` (CP-M6-7-3 sealed) sourced from sealed CP-AIP-7 planner boundary; a training proposal with a point estimate raises `PointEstimateTrainingProposalRefused`. Per §11.2 P179 verbatim: 'stated confidence interval — never a point estimate.'
4. **Proposal-without-calibration-stage refused** — a proposed training delta MUST reference a `CalibrationOutput` (CP-M6-8-1 sealed) sourced from sealed CP-AIP-8 S&R boundary; a training proposal without a calibration stage raises `PlanWithoutCalibrationStageProposalRefused`. Per §11.2 P179 verbatim: 'A plan without a calibration stage is rejected.'
5. **Evolved-objective supersedes-additively (nothing relabelled/rewritten)** — same shape as CP-AIP-ASSIST-CENSUS.
6. **Markers-over-refusal per §6.9** — same shape as CP-AIP-ASSIST-CENSUS.
7. **Autonomy-wiring per Ruling (b)** — the assistant registers itself as a **Training-Runs-Service job** (extending the sealed Census Autonomy Service pattern for training-runs seat), so the running Akki system schedules and executes assistant turns autonomously.
8. **Weights + corpus + compute stay in Akki boundary** — per Ruling (b) verbatim: training compute, model weights, and the labelled corpus **never leave Akki's boundary; no third-party export.** Enforced by structural invariant scanning the assistant module for outbound network calls or filesystem writes outside `/tenant/*` scope.
9. **RED-first pins (planned; not yet written):**
   - `test_training_assistant_proposal_without_rationale_refused`
   - `test_training_assistant_proposal_without_cost_ci_refused` (§11.2 P179)
   - `test_training_assistant_proposal_without_calibration_stage_refused` (§11.2 P179)
   - `test_training_assistant_evolved_objective_supersedes_additively_never_relabels`
   - `test_training_assistant_marker_over_refusal_enforced_structurally`
   - `test_training_assistant_registers_as_training_runs_service_job`
   - `test_training_assistant_turn_record_frozen_shape`
   - `test_training_assistant_no_outbound_network_calls_outside_tenant_boundary` (Ruling (b) verbatim)
   - `test_training_assistant_extends_not_parallels_sealed_planner_boundary`
   - `test_new_module_carries_training_assistant_v1_posture_marker_citing_ruling_b_and_standing_directive_1_verbatim`

## MUST NOT

- Edit any sealed CP-AIP-6/7/8/10 carrier or sealed Census Autonomy Service carrier.
- Run the assistant inside the E1 pod. `Ruling (b) verbatim: E1 to wire it into Akki's autonomy so Akki runs it, then step back.`
- Export weights / corpus / compute outside Akki's tenant boundary. `Ruling (b) verbatim: never leave Akki's boundary; no third-party export.`
- Propose a training run without a calibration stage (§11.2 P179 verbatim).
- Propose a training run with a point-estimate cost quote (§11.2 P179 verbatim).
- Relabel or rewrite historical assistant turns.
- Refuse where a §6.9 marker makes the state honest.
- Sprawl beyond the ledger item.

## EXIT

**RED-first invariants (10 planned):** all listed under MUST DO §9 above; specific test node IDs finalize at slice authorship (after CP-AIP-10 training-run contract seat is sealed).

**Autonomy-pickup receipt as exit evidence** — a receipt from the Akki autonomy engine's run log showing it scheduled and executed at least one Training Assistant turn on its own cadence, AND a §1.4 measured cost/compute receipt for any executed training run (never claimed without receipt).

## STOP

Stop at owner ratification of this draft card (in CP-AIP-10 REPORT-AND-CONTINUE report). If ratified, build **after** CP-AIP-10 seals + SO-6.9 wave completes + CP-AIP-ASSIST-CENSUS seals (natural ordering: Census Assistant supplies the corpus/leads, Training Assistant consumes them).

If a SPEC-CONFLICT is discovered between this card and sealed CP-AIP-6/7/8/10 carriers / AIP v1.0 §1.2 modality-extension discipline / Ruling (b) verbatim, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report immediately.

## ANCHORS

- **Owner Ruling (b) verbatim (2026-02-23):** 'E1 to wire it into Akki's autonomy so Akki runs it, then step back' + 'Training compute, model weights, and the labelled corpus never leave Akki's boundary; no third-party export.'
- **Standing Directive 1 verbatim (2026-02-23):** 'note the natural back and forth you and i are having when shaping the objectives and evolving it both for training and census. This is the work of the assistants in census and training.'
- **Owner drop verbatim (2026-02-23):** `STATE/OWNER_DROPS/ruling_b_akki_runs_it_plus_standing_directives_20260223/DROP.md` §1-3.
- **Sealed carriers extended (unchanged):** listed under OBJECTIVE above.
- **AIP v1.0 §11.2 P179 verbatim:** 'The first job prices the real job.' + 'stated confidence interval — never a point estimate.' + 'A plan without a calibration stage is rejected.'
- **Standing Orders:** SO §3 RED-first · SO §3.8 additive-only · SO §6.2 objective-card + hash-pin · SO §6.9 desk discipline · SO §7 17-guard consolidated set · §1.4 measured cost/compute receipt discipline.
- **Ledger check:** this card owner-directs `CP-AIP-ASSIST-TRAINING` and nothing else. Build sequenced after CP-AIP-10 + SO-6.9 wave + CP-AIP-ASSIST-CENSUS.
