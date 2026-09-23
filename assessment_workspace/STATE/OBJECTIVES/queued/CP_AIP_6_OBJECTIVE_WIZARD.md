# CP-AIP-6-OBJECTIVE-WIZARD · objective card · 2026-02-23T05:05:00Z

**Spec anchor:** AIP v1.0 §8 + §9 + §12.1 · Build Sequence #6.

**Status:** ⚪ **QUEUED** (opens after CP-AIP-5 completes).

## Rationale for position (spec §15 verbatim · IMPORTANT ORDERING)

> *"The planner must never accept a hand-authored Outcome once the wizard exists; building the planner first invites the malformed-input class the compile stage makes impossible."*

The wizard MUST land BEFORE the planner (CP-AIP-7).

## Scope

**Extend the existing shaping-wizard state machine with an objective variant** (§16.1(c) recommendation VERIFIED). Do NOT stand up a sibling machine.

Sub-slices:

- **§8 Objective Wizard**: `variant="objective"` extension of `WizardCommitState_v0.variant` Literal (additive Pydantic 2.13 shape preserved).
- **§8.1 role**: elicit objective in plain language; compile two governed artifacts — `TargetOutcome` (§10) + `CollectionSchema` (§9).
- **§8.2 elicitation sequence**: (1) question · (2) population resolved against register strata · (3) acceptance bar per stratum two-dimensional · (4) collection consequences with cost visible before commission.
- **§8.3 propose-qualify-graduate**: agent proposes novel data points → qualified against objective on a sample → graduate into objective tier (per-commission). Baseline-tier graduation is ceremony-governed.
- **§8.4 compile-time rejections** (schema-shape refusals · not warnings):
  - Outcome without existing `test_set_ref` — REJECTED.
  - Acceptance bar missing per-stratum dimension — REJECTED.
  - Collection Schema requiring column violating §6.2 custody conditions — REJECTED.
- **§8.5 record + handoff**: `objective_session` data class stamped to ledger via existing `turn_ledger.py` (byte-identical reuse); options considered AND rejected recorded (answerable "why was the model built this way"); handoff to Targeta via existing `admission_handoff.py`.
- **§9 CollectionSchema**: two tiers per §9.2 (baseline · standing · objective-independent) + §9.3 (objective · declared per commission).
- **§12.1 registry namespace**: per-commission scoped namespace within registry (Mtafiti audio modality); reads compose with global registry, writes namespace-scoped; on close sealed not deleted.

## §16.2 open decision working defaults (banked per owner 2026-02-23T04:15Z)

- **Baseline tier contents (§9.2)**: v1.0 proposed set as-is (language ID, code-switch points, condition profile, dedup instance condition map, synthesis-relevant group acoustics) — banked as PENDING-OWNER-CONFIRMATION with working default.

## Acceptance criteria (become RED-first pytest invariants)

**§8.4 compile-time rejection tests** (mandatory · schema-shape):

1. Outcome without `test_set_ref` → `TestSetRefMissing` refusal.
2. Acceptance bar without per-stratum dimension → `AcceptanceBarNotStratified` refusal.
3. CollectionSchema requiring §6.2-violating column → `CustodyViolation` refusal.

**§9.2 baseline-tier invariants**:

4. Baseline tier column set matches §9.2 v1.0 list exactly (frozen constant · additive change requires ceremony).

**§12.1 registry namespace invariants**:

5. Namespace closure state is `sealed` (never `deleted`).
6. Reads compose with global · writes scoped.

**§8.5 ledger invariants**:

7. Every wizard session stamps `objective_session` data class to ledger.
8. Options considered AND rejected both recorded (§8.5 verbatim).

## New additive modules (proposed shape)

- `contracts/target_outcome_v0.py` (§10.1 seven-field schema).
- `contracts/collection_schema_v0.py` (§9 two-tier).
- `contracts/wizard_objective_commit_state_v0.py` (§8.5 extension of `WizardCommitState_v0`).
- `services/wizard/objective_state_machine.py` (§8 variant of `operator_state_machine.py`).
- `services/wizard/objective_compile.py` (§8.4 compile-time rejections).
- `services/registry/audio_modality_namespace.py` (§12.1 per-commission scoped namespace).
- Test file: `tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py` (≥8 RED-first pins).

## Sealed carriers to NOT edit

- `services/wizard/operator_state_machine.py`.
- `services/wizard/agent_interface.py`.
- `services/wizard/turn_ledger.py`.
- `services/wizard/session_persistence.py`.
- `services/wizard/admission_handoff.py`.
- `contracts/wizard_commit_state.py` — extended via new sibling contract, not edited.

## Ledger check

> **Ledger check — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal · BASELINE_GUARD.**
