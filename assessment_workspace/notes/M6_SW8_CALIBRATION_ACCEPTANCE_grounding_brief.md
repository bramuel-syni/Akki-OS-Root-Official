# M6 Sub-wave 8 · W-M6-CALIBRATION-ACCEPTANCE · grounding brief

**Opened at UTC:** 2026-09-16T~02:07Z
**Canon scope:** §11.2 (P179..P180 · V113) + §11.3 (P181..P182 · V114).
**Track-a HEAD at open:** `d411cc70bea163f75f082e3ac5a0e688338d6e54` (CP-M6-7-3 · Sub-wave 7 close).
**Master HEAD at open:** `51ec75cdacc4fc837d1bdbf5f409a1f8a7e05cbb` (CP-M6-7-3 Commit C amended).
**Ratchet floor at open:** 4318 (verified on disk).
**M6 §15 walk position:** 8 of 10 sub-waves.

---

## §A · Canon anchors (verbatim on single un-wrapped lines)

### §11.2 · Sampling & Reflection (calibration) — mandatory first stage

- **V113 · P179..P180 (LOAD-BEARING · full paragraph):** *"Data requirements for low-resource fine-tuning are empirical; no analytical answer exists. The first commissioned stage is therefore a calibration: train at three to four data volumes, evaluate per stratum against the test set, fit the scaling curve, extrapolate to the acceptance threshold. Only then is the full run quoted, with a stated confidence interval — never a point estimate. A plan without a calibration stage is rejected. The first job prices the real job."*

Sub-clauses (for gating tests):

- V113a — *"train at three to four data volumes"* (closed-range enforcement)
- V113b — *"evaluate per stratum against the test set"* (per-stratum discipline)
- V113c — *"fit the scaling curve"* (curve-fit carrier)
- V113d — *"extrapolate to the acceptance threshold"* (extrapolation carrier)
- V113e — *"Only then is the full run quoted, with a stated confidence interval — never a point estimate."* (CI-mandatory in full-run quote · composes CP-M6-7-3 `CostQuoteWithCI`)
- V113f — *"A plan without a calibration stage is rejected."* (existence gate)
- V113g — *"The first job prices the real job."* (accountability anchor)

### §11.3 · Milestones — the accountability output

- **V114 · P181..P182 (full paragraph):** *"Sampling & Reflection has two customers. It prices the real job, and it authors the accountability structure: its output to the objective owner is not a curve but a proposed milestone list — the checklist of what must be done, in what order, for the commission to succeed. Each milestone carries a done-condition and an owner. The objective owner reviews and agrees the list at commission; from that point, all reporting is against it. Accountability is set before spend, not discovered during."*

Sub-clauses (for gating tests):

- V114a — *"a proposed milestone list — the checklist of what must be done, in what order"* (ordered list carrier)
- V114b — *"Each milestone carries a done-condition and an owner."* (per-milestone mandatory fields)
- V114c — *"The objective owner reviews and agrees the list at commission; from that point, all reporting is against it."* (agreement gate; commission-open only after agreement)
- V114d — *"Accountability is set before spend, not discovered during."* (before-spend discipline; refusals fire at agreement time, not at run time)

---

## §B · CP breakdown

Sub-wave 8 walks two CPs.  Ceilings mirror sub-wave 6/7 owner-set discipline (≤10 per CP).

### CP-M6-8-1 · §11.2 V113 Calibration procedure carrier + refusals

**New module:** `services/audio_plane_v1/calibration.py`.

**Public API target (10 exports · owner-set ≤10 ceiling · WITHIN):**

- `CALIBRATION_MIN_VOLUMES = 3` · `CALIBRATION_MAX_VOLUMES = 4` — closed-range constants per V113a.
- `CalibrationVolume` — frozen 2-carrier: `volume_id: str` · `hours: float`.
- `PerStratumTestSetEval` — frozen 3-carrier: `stratum_ref` · `volume_id` · `accuracy_at_volume` (V113b · per-stratum test-set eval row).
- `ScalingCurveFit` — frozen 2-carrier: `fit_type: str` · `fit_params: Mapping[str, float]` (V113c).
- `CalibrationOutput` — frozen 4-carrier: `volumes: Tuple[CalibrationVolume, ...]` (3..4 length) · `per_stratum_evals: Tuple[PerStratumTestSetEval, ...]` · `curve_fit: ScalingCurveFit` · `extrapolated_hours_to_threshold: Mapping[str, float]` (V113d).  Refuses `CalibrationVolumeCountError` at `__post_init__` when len(volumes) ∉ [3, 4].
- `assert_full_run_quote_has_ci(*, quote)` — V113e composition-check: composes with CP-M6-7-3 `CostQuoteWithCI` (already enforces mandatory CI); this helper refuses `PointEstimateOnlyQuoteRefused` on any *non-CostQuoteWithCI* quote-shaped object passed for the full-run quote — closes the surface where a caller might pass a bare number instead of the CI-bearing carrier.
- `assert_plan_has_calibration_stage(*, plan_has_calibration_output: bool)` — V113f existence gate: refuses `PlanWithoutCalibrationStageRefused` when False.
- `CalibrationVolumeCountError` — V113a refusal.
- `PointEstimateOnlyQuoteRefused` — V113e refusal.
- `PlanWithoutCalibrationStageRefused` — V113f refusal.

**Invariants (target 10):**

1. module_fabric (10 exports).
2. V113 verbatim in module docstring (single-line SO §2 CONDITION 1 anchor).
3. `CALIBRATION_MIN_VOLUMES == 3 and CALIBRATION_MAX_VOLUMES == 4` (V113a closed-range).
4. `CalibrationVolume` frozen 2-carrier.
5. `PerStratumTestSetEval` frozen 3-carrier.
6. `ScalingCurveFit` frozen 2-carrier.
7. `CalibrationOutput` refuses `CalibrationVolumeCountError` when volumes count is 2 (below-min) and 5 (above-max); passes on 3 and 4.
8. `assert_full_run_quote_has_ci` passes on real `CostQuoteWithCI`; refuses `PointEstimateOnlyQuoteRefused` on bare float and duck-typed lookalike.
9. `assert_plan_has_calibration_stage` refuses `PlanWithoutCalibrationStageRefused` when False; passes silently on True.
10. Composes with CP-M6-7-3 without modification: import-only reference to `CostQuoteWithCI`.

### CP-M6-8-2 · §11.3 V114 Milestone-list contract · CLOSES SUB-WAVE 8

**New module:** `services/audio_plane_v1/milestones.py`.

**Public API target (10 exports · owner-set ≤10 ceiling · WITHIN):**

- `Milestone` — frozen 3-carrier: `milestone_id: str` · `done_condition: str` (mandatory non-empty per V114b) · `owner: str` (mandatory non-empty per V114b).  Refuses `MilestoneMissingDoneConditionError` at `__post_init__` on empty `done_condition`.  Refuses `MilestoneMissingOwnerError` on empty `owner`.
- `MilestoneList` — frozen 3-carrier: `milestones: Tuple[Milestone, ...]` (ordered · V114a) · `commission_agreement_ref: Optional[str]` (None until owner agrees per V114c) · `commission_id: str`.
- `construct_milestone_list(*, milestones, commission_id) -> MilestoneList` — factory; commission_agreement_ref defaults None.  Refuses `MilestoneListEmptyError` on empty milestones tuple.
- `agree_milestone_list(*, milestone_list, commission_agreement_ref) -> MilestoneList` — V114c gate: returns a new frozen `MilestoneList` with the agreement ref set.  Refuses `MilestoneListAlreadyAgreedError` on re-agreement (V114d "from that point, all reporting is against it").
- `assert_commission_open_only_after_agreement(*, milestone_list) -> None` — refuses `CommissionOpenBeforeAgreementError` when `commission_agreement_ref is None` (V114c).
- `MilestoneMissingDoneConditionError` — V114b refusal.
- `MilestoneMissingOwnerError` — V114b refusal.
- `MilestoneListEmptyError` — V114a refusal.
- `MilestoneListAlreadyAgreedError` — V114d refusal.
- `CommissionOpenBeforeAgreementError` — V114c refusal.

**Invariants (target 10):**

1. module_fabric (10 exports).
2. V114 verbatim in module docstring (single-line SO §2 CONDITION 1 anchor).
3. `Milestone` frozen 3-carrier.
4. `Milestone` refuses `MilestoneMissingDoneConditionError` on empty done_condition.
5. `Milestone` refuses `MilestoneMissingOwnerError` on empty owner.
6. `MilestoneList` frozen 3-carrier · ordering preserved (V114a).
7. `construct_milestone_list` refuses `MilestoneListEmptyError` on empty milestones.
8. `agree_milestone_list` happy path: returns new MilestoneList with agreement ref set; original untouched (frozen).
9. `agree_milestone_list` refuses `MilestoneListAlreadyAgreedError` on re-agreement (V114d).
10. `assert_commission_open_only_after_agreement` refuses `CommissionOpenBeforeAgreementError` when agreement ref None; passes silently when set.

---

## §C · §3.3 3-commit pattern (per CP; twice over)

Standard §3.3 pattern applies (per M6 SW7 grounding brief §C).

---

## §D · Wave-honest limits

1. **§11.2 body scope-limited.**  Calibration procedure lands as *carriers + refusals + composition-checks*; the actual training-run mechanics (§11.6 V120 · sub-wave 10 HALT) are out of scope.  V113a "train at three to four data volumes" is enforced as a shape rule on the `CalibrationOutput.volumes` tuple length — the training is not executed.
2. **§11.3 body scope-limited.**  Milestone-list is the compile-time authoring surface + agreement gate.  Runtime status (done/on-track/behind/missed) is the §13.2 Commission View concern — lands sub-wave 9.
3. **V113e CI composition-check is a defensive gate.**  `CostQuoteWithCI` (CP-M6-7-3) already enforces CI at construction; `assert_full_run_quote_has_ci` closes the surface where a caller might bypass by passing a bare number to a downstream function.
4. **V114c agreement ref is opaque.**  This CP does NOT verify the ref binds to any specific authenticator / receipt / signature — it is a string carrier.  The verification surface is a Watch / Commission View concern (sub-wave 9 or Track-B).
5. **No LLM / HTTP / filesystem / network. Synthetic-fixtures-only. Case-agnostic. §3.1 P038 preserved.**
6. **HALT boundary preserved.**  If any mechanism requires real estate voice/biometric material → HALT to owner immediately.  §11.6 is the primary HALT trigger and lands sub-wave 10.

---

## §E · Definition of Done

**Per-CP DoD** — as §C above.

**Sub-wave 8 DoD:**
- CP-M6-8-1 sealed under §3.3.
- CP-M6-8-2 sealed under §3.3.
- Wave-close report `notes/W_M6_CALIBRATION_ACCEPTANCE_close.md` authored.
- Ratchet delta target: +18..+22 (two CPs at 8-10 each).
- Boundary probes #58 + #59 target: all NOTE-SKIPPED per SEC halt (probe loop resumes only after JUMP custody rotation to JSON).
- Word-boundary executive-domain + audio-material negative-scan CLEAN on every seal.
- §3.1 P038 tokens-not-waveforms discipline preserved on every new API surface.
- HALT boundary held.

**Owner-facing report cadence:** at sub-wave 8 seal OR genuine HALT.

**Owner-desk items still open (unchanged this shift):**
- SEC incident ratification in `STATE/DECISIONS.md`.
- JUMP root credential rotation (+ optional custody-format migration to JSON).
- Admin SG binds for CD + Visitors + NAS-username spelling correction ('bramuel' vs 'bramwel').

---

## §F · Onward (post-sub-wave-8)

- Sub-wave 9 · Commission View surface (§13).
- Sub-wave 10 · §11.6 full training runs on real estate data — **expected HALT-to-owner at sub-wave open** per owner direction.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
