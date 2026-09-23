# CP-AIP-8-SAMPLING-REFLECTION · objective card · 2026-02-23T05:05:00Z

**Spec anchor:** AIP v1.0 §11.2 + §11.3 · Build Sequence #8.

**Status:** ⚪ **QUEUED** (opens after CP-AIP-7 completes).

## Rationale for position (spec §15 verbatim)

> *"Requires 7 and a test set."*

## Scope

**§11.2 Sampling & Reflection (calibration) — MANDATORY FIRST STAGE.**

- Train at 3-4 data volumes.
- Evaluate per stratum against the test set.
- Fit scaling curve.
- Extrapolate to acceptance threshold.
- Only then is the full run quoted, with a stated **confidence interval — never a point estimate**.
- A plan without a calibration stage is REJECTED.
- **The first job prices the real job.**

**§11.3 Milestones — the accountability output.**

- S&R has two customers: (a) prices the real job, (b) authors the accountability structure.
- Output to the objective owner is NOT a curve but a **proposed milestone list** — the checklist of what must be done, in what order, for the commission to succeed.
- Each milestone carries a **done-condition** and an **owner**.
- Objective owner reviews and agrees the list at commission; from that point, ALL reporting is against it.
- **Accountability is set before spend, not discovered during.**

## §16.2 open decision (banked per owner 2026-02-23T04:15Z)

- **Codec choice** — deferred to this CP. Sampling & Reflection answers: adopt existing open codec vs training estate-specific per §11.2 measurement.

## Acceptance criteria (become RED-first pytest invariants)

1. Training plan without calibration stage → `PlanCalibrationMissing` refusal (§11.2 verbatim).
2. Cost quote from S&R MUST carry `confidence_interval` field (§11.2 verbatim `"never a point estimate"`).
3. S&R output shape MUST include `proposed_milestone_list` (§11.3 verbatim).
4. Each milestone MUST carry `done_condition` + `owner` fields (§11.3 verbatim).
5. Objective-owner agreement recorded as commissioning event (§11.3 verbatim `"from that point, all reporting is against it"`).

## New additive modules (proposed shape)

- `services/sampling_reflection/calibration.py` — 3-4 volume trainer + curve fitter.
- `services/sampling_reflection/scaling_curve.py`.
- `services/sampling_reflection/confidence_interval.py`.
- `services/sampling_reflection/milestone_authoring.py`.
- `contracts/milestone_v0.py` — frozen (`done_condition`, `owner`, `status`, etc.).
- Test file: `tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py` (≥5 RED-first pins).

## Sealed carriers to NOT edit

- CP-AIP-7 planner outputs (consumed byte-identically as input).

## Ledger check

> **Ledger check — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-8-SAMPLING-REFLECTION and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal · BASELINE_GUARD.**
