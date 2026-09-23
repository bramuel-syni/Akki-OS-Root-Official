# CP-AIP-7-TARGET-OUTCOME-PLANNER · objective card · 2026-02-23T05:05:00Z

**Spec anchor:** AIP v1.0 §10 + §11.1 + §11.4 · Build Sequence #7.

**Status:** ⚪ **QUEUED** (opens after CP-AIP-6 completes).

## Rationale for position (spec §15 verbatim)

> *"Requires register strata to plan against and the wizard to author Outcomes."*

## Scope

- **§10.1 TargetOutcome seven-field schema**: `task`, `domain`, `population`, `acceptance`, `gate_policy`, `test_set_ref`, `constraints`.
- **§10.2 binding rules**:
  - Population is register-defined (not label-defined).
  - Acceptance is per-stratum (never single global threshold).
  - Test set precedes training (rejected at definition time if absent).
  - Gate decision recorded on Outcome at definition (not ad hoc at ship time).
- **§11.1 planner architecture**: reuse existing planner pattern — deterministic core computes eligibility; learned layer may only reorder an already-eligible set stripped of eligibility-values; gate compares learned vs baseline; every plan reproducible from recorded inputs.
- **§11.4 planner outputs**:
  - Coverage report per target stratum (hours available · quality distribution · gaps · cost of closing each gap).
  - Curriculum ordering + weighting (register-derived · NOT corpus-natural-distribution which is always skewed).
  - Proposed milestone list (§11.3 · lands in CP-AIP-8).
  - Cost quote with confidence interval (never point estimate).

## §16.2 open decision (banked per owner 2026-02-23T04:15Z)

- **Platform default for `gate_policy` where Outcome does not set it**: `"missed stratum gates release"` (fail-closed per §1.5 doctrine) — owner-approved default. Owner may override later. This decision silently decides how minority-variant quality is treated under schedule pressure.

## Acceptance criteria (become RED-first pytest invariants)

1. `TargetOutcome` without `test_set_ref` → `TestSetRefMissing` refusal at definition time (§10.2 verbatim).
2. `TargetOutcome.acceptance` shape rejects single-global threshold; per-stratum required.
3. `TargetOutcome.gate_policy` frozen Literal `{"missed_stratum_gates_release", "ships_documented"}` — default `"missed_stratum_gates_release"` per owner working default.
4. Planner input immutability: `plan_id` is deterministic hash of recorded inputs (§11.1 verbatim `"reproducible from its recorded inputs"`).
5. Learned-layer scope: cannot re-admit an eligibility-excluded item (§11.1 gate check).
6. Cost quote payload MUST carry `confidence_interval` field — point-estimate rejected.

## New additive modules (proposed shape)

- `contracts/target_outcome_v0.py` (shared with CP-AIP-6).
- `services/training_planner/eligibility_core.py` (deterministic core).
- `services/training_planner/learned_reorder.py` (learned layer with baseline gate).
- `services/training_planner/coverage_report.py`.
- `services/training_planner/curriculum.py`.
- `services/training_planner/cost_quote_with_ci.py`.
- Test file: `tests/invariants/test_cp_aip_7_planner_aip_v1_0_section_10_11.py` (≥6 RED-first pins).

## Sealed carriers to NOT edit

- Existing extraction planning pattern (`services/*_planner/`) reused byte-identically as pattern reference.

## Ledger check

> **Ledger check — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-7-TARGET-OUTCOME-PLANNER and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal · BASELINE_GUARD.**
