# M6 Sub-wave 7 · W-M6-TARGET-OUTCOME-PLANNER · grounding brief

**Opened at UTC:** 2026-09-15T~23:05Z
**Canon scope:** §10 (P153..P169) + §11.1 (P171..P178) + §11.4 (P184..P188).
**Track-a HEAD at open:** `053d3f1` (last CP mechanism · sub-wave 6 hygiene).
**Master HEAD at open:** `c2b1c363` (last commit · sub-wave 6 wave-close report).
**Ratchet floor at open:** 4288 (verified on disk at boot ritual).
**M6 §15 walk position:** V147 · TABLE-ROW-08 verbatim: *"TargetOutcome type + planner core (§10, §11.1, §11.4). Requires register strata to plan against and the wizard to author Outcomes."*

---

## §A · Canon anchors (verbatim on single un-wrapped lines)

### §10 · The Target Outcome

**Schema (§10.1 · V98–V104 · P154..P164 verbatim TargetOutcome block):**

- V98 · P156 · *"task — operational statement of what the model must do"*
- V99 · P157 · *"domain — context of use"*
- V100 · P158 · *"population — defined by reference to register strata, not labels"*
- V101 · P159 · *"acceptance — threshold per stratum; two-dimensional (accuracy, coverage)"*
- V102 · P160 · *"gate_policy — per Outcome: missed stratum gates release | ships documented"*
- V103 · P161 · *"test_set_ref — must exist before the Outcome is accepted"* (LOAD-BEARING)
- V104 · P162 · *"constraints — latency, compute budget, deployment target"*

**Binding rules (§10.2 · V105–V108 · P165..P169):**

- V105 · P166 · *"Population is register-defined. 'Language L, accent clusters 1–4, telephone band and studio, adult' — never 'speakers of L.' This is what makes coverage computable."*
- V106 · P167 · *"Acceptance is per stratum. A single global threshold hides the failure that matters: 94% on the majority variant and 61% on the rest passes one test and fails the one that decides whether the work reaches the people it was built for."*
- V107 · P168 · *"The test set precedes the training. An Outcome without an existing, stratified test set is rejected at definition time."*
- V108 · P169 · *"The gate decision is recorded on the Outcome at definition — not decided ad hoc at ship time."*

### §11.1 · Training Planner Architecture

- V109 · P172 · *"The existing planner pattern is reused unchanged: a deterministic core computes eligibility; a learned layer may only reorder an already-eligible set it receives stripped of the values that decided eligibility; a gate compares learned output against the deterministic baseline; every plan is reproducible from its recorded inputs."*
- V110 · P175 · *"Object · Source locations · Register strata"* (extraction vs training contrast row)
- V111 · P176 · *"Floor · Defensibility class · Acceptance threshold — accuracy × coverage"*
- V112 · P177 · *"Output · Mining plan · Training plan + curriculum + milestones"*

### §11.4 · Planner outputs

- V115 · P185 · *"Coverage report — per target stratum: hours available, quality distribution, gaps, cost of closing each gap."*
- V116 · P186 · *"Curriculum — ordering and weighting across strata derived from the register, not from the corpus's natural distribution, which is always skewed toward whatever occurred most. The dedup instance condition map enters as a designated robustness stratum."*
- V117 · P187 · *"Proposed milestone list (§11.3)."* (§11.3 lands in sub-wave 8; V117 is a forward-reference stub carrier here)
- V118 · P188 · *"Cost quote with a stated confidence interval."*

---

## §B · CP breakdown (packaging decision, per owner delegation)

Sub-wave 7 walks three CPs.  Ceilings mirror sub-wave 6's owner-set discipline (≤10 per CP).

### CP-M6-7-1 · Full §10 TargetOutcome carrier + §10.2 binding rules (composes with CP-M6-6-1 STUB)

**New module:** `services/audio_plane_v1/target_outcome.py`.  Landing a new module (not extending `objective_wizard.py`) because sub-wave 7 is a new architectural area (§10 Target Outcome + §11 Training Planner) separate from sub-wave 6's compile-refusal machinery, and `objective_wizard.py` already carries the STUB territory that stays live for backward compat.

**Public API target:**

- `GATE_POLICY_VALUES` — frozenset `{"missed_stratum_gates_release", "ships_documented"}` (V102 closed-set verbatim).
- `PopulationSpec` — frozen carrier: `stratum_refs: Tuple[str, ...]` (V100 register-defined; refuses empty at `__post_init__` per V105).
- `Constraints` — frozen 3-carrier: `latency` · `compute_budget` · `deployment_target` (V104 verbatim triple).
- `TargetOutcome` — frozen 7-carrier: `task` · `domain` · `population: PopulationSpec` · `acceptance: AcceptanceBar` · `gate_policy: str` (∈ GATE_POLICY_VALUES · V102 closed-set enforced at `__post_init__`; V108 gate-at-definition enforced by frozen dataclass) · `test_set_ref: str` (mandatory · V107 test-set-precedes-training; not Optional) · `constraints: Constraints`.
- `construct_target_outcome(*, task, domain, population, acceptance, gate_policy, test_set_ref, constraints) -> TargetOutcome` — factory that additionally enforces cross-field:
    - `acceptance.has_per_stratum_dimension == True` (V106); refuses `AcceptancePerStratumMissingError` otherwise.
- Refusals (4): `GatePolicyInvalidError` (V102 closed-set) · `PopulationEmptyStrataRefsError` (V105 register-defined) · `TestSetRefMissingError` (V107 mandatory) · `AcceptancePerStratumMissingError` (V106 per-stratum acceptance).

**Composition with sub-wave 6:**
- Composes with existing `AcceptanceBar` from `objective_wizard.py` (imported).
- `TargetOutcomeStub` in `objective_wizard.py` remains untouched — backward compat preserved.
- Future work may re-wire `compile_objective_artifact` to accept full `TargetOutcome` in addition to `TargetOutcomeStub`; that is a follow-on CP not this one.

**Invariants (10 · owner-set ≤10 ceiling · WITHIN):**

1. module_fabric (10 public exports).
2. `GATE_POLICY_VALUES` verbatim frozenset.
3. `Constraints` frozen 3-carrier discipline.
4. `PopulationSpec` refuses empty stratum_refs with `PopulationEmptyStrataRefsError` (V105).
5. `TargetOutcome` frozen 7-carrier discipline.
6. `TargetOutcome` refuses invalid gate_policy at `__post_init__` with `GatePolicyInvalidError` (V102).
7. `construct_target_outcome` refuses when `test_set_ref` is empty string with `TestSetRefMissingError` (V107).
8. `construct_target_outcome` refuses when `acceptance.has_per_stratum_dimension is False` with `AcceptancePerStratumMissingError` (V106).
9. `construct_target_outcome` refuses when `population.stratum_refs` is empty (via `PopulationSpec` `__post_init__` — same refusal as #4; separate test for factory-level pass-through).
10. `construct_target_outcome` passes on well-formed input (positive path; both gate_policy values exercised).

### CP-M6-7-2 · §11.1 Planner architecture four-carrier (V109 verbatim + V110–V112)

**New module:** `services/audio_plane_v1/training_planner.py`.

**Public API target:**

- `PlanInputs` — frozen carrier for reproducibility: record every input the planner reads (V109 verbatim "every plan is reproducible from its recorded inputs").  Minimum shape: `outcome: TargetOutcome` · `register_strata_refs: Tuple[str, ...]` · `seed: int`.
- `PlannerCore` — Protocol · deterministic core computing eligibility (V109 first-clause).  Case-agnostic seam.
- `LearnedReorderLayer` — Protocol · takes an already-eligible set stripped of eligibility values (V109 second-clause).  Case-agnostic seam.
- `EligibilityGate` — function comparing learned output against deterministic baseline (V109 third-clause).  Refuses `EligibilityGateSlippageError` if learned set diverges from deterministic set membership (only ordering may differ).
- `PlanReproducibilityWitness` — frozen carrier binding `plan_inputs_sha256` to `plan_output_sha256` (V109 fourth-clause · reproducible from recorded inputs).
- Refusals: `LearnedReorderStrippingViolationError` (V109 · "stripped of the values that decided eligibility") · `EligibilityGateSlippageError` (V109 · gate rejects learned membership divergence).

**Invariants (target: 8-10 · owner-set ≤10 ceiling).**

### CP-M6-7-3 · §11.4 Planner outputs (V115 coverage + V116 curriculum + V117-forward-ref + V118 confidence-interval-mandatory) · CLOSES SUB-WAVE 7

**Extends:** `services/audio_plane_v1/training_planner.py` (append-only under Part-B header · no refactor).

**Public API target:**

- `PerStratumCoverageEntry` — frozen carrier for V115: `stratum_ref` · `hours_available_h` · `quality_distribution_summary_ref` · `gap_hours_h` · `cost_of_closing_gap`.
- `CoverageReport` — frozen 1-carrier: `entries: Tuple[PerStratumCoverageEntry, ...]`.
- `CurriculumOrdering` — frozen carrier for V116: `stratum_weight_pairs: Tuple[Tuple[str, float], ...]` (from register-not-corpus) · `robustness_stratum_ref: Optional[str]` (dedup instance condition map per V116).
- `CostQuoteWithCI` — frozen 3-carrier for V118: `point_estimate` · `ci_low` · `ci_high` (all mandatory; V118 verbatim "*a stated confidence interval*").  Refuses `CostQuoteMissingCIError` on `ci_low is None` or `ci_high is None`.
- `MilestoneListRef` — frozen 1-carrier: `ref: str` — V117 forward-reference stub (§11.3 milestone content lands in sub-wave 8).
- `PlannerOutputs` — frozen 4-carrier: `coverage_report` · `curriculum` · `milestone_list_ref` · `cost_quote`.
- Refusals: `CostQuoteMissingCIError` (V118) · `CurriculumWeightNormalizationError` (V116 · weights sum to 1.0 under floating-point tolerance).

**Invariants (target: 8-10 · owner-set ≤10 ceiling).**

---

## §C · §3.3 3-commit pattern (per CP; three times over)

Each CP walks:
1. **RED** — author test file → `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/ -q` → capture right-reason RED at `phase0/drill_receipts/<utc>_wm6_7_<n>_RED_pre_impl.log`.
2. **Mechanism** — author module.
3. **Targeted green** — fast sanity: `pytest tests/invariants/test_wm6_7_<n>_*.py -v`.
4. **Ratchet bump** — bump `passed` + `passed_floor` + append `ratchet_history`.
5. **Double-green** — full pytest twice · byte-match stripped-sha256.
6. **Rider** — `phase0/wave_riders/w_m6_target_outcome_planner_cp<n>/` (pip_freeze + collect_only).
7. **Boundary probe** — NOTE-SKIPPED per SEC halt · reference `sec_incident_jump_cred_leak_20260915T222935Z`.
8. **Seal** — `phase0/output_verified_seals/cp_m6_7_<n>_<module>.seal.txt` with `Kind:` first line; track-a SHA after Commit A; master SHA `TBD` at Commit B; landed at Commit C.
9. **STATE updates** — append CP entry to DECISIONS + NEXT.
10. **Commit A** (track-a) · **Commit B** (master · TBD) · **Commit C** (master · fixup).

---

## §D · Wave-honest limits

1. **§11 body scope-limited.**  Sub-wave 7 lands §11.1 (architecture) + §11.4 (planner outputs) ONLY.  §11.2 (Sampling & Reflection · V113 calibration procedure) + §11.3 (Milestones · V114 milestone-list contract) land in sub-wave 8.  §11.5 (Provenance · V119) is post-M6 (part of the wider training lifecycle).  §11.6 (Run governance · V120) — sub-wave 10 with expected HALT-to-owner.
2. **§10.2 rule V105 is population-shape only.**  This CP enforces "population references register strata (non-empty stratum_refs)".  It does NOT verify that the referenced stratum_refs actually exist in the CP-M6-3-1 CharacterRegister — that is a downstream composition, out of scope here.
3. **§11.1 V109 "learned layer" is Protocol-only.**  The actual model that instantiates `LearnedReorderLayer` is out of scope for M6 v1 (no live training in M6).  V109's four-carrier discipline is enforced at seam-composition, not at any specific backend.
4. **§11.4 V117 milestone list is forward-reference stub.**  V114 (§11.3 · P183) milestone semantics land in sub-wave 8.  V117 in this CP is a `MilestoneListRef` carrier only.
5. **No LLM invocation. No HTTP call. No filesystem write. No network. Synthetic fixtures only.**
6. **HALT boundary preserved.**  If any mechanism requires real estate voice/biometric material → HALT to owner immediately (unlikely this sub-wave; §11.6 is the primary HALT trigger and lands sub-wave 10).

---

## §E · Definition of Done

**Per-CP DoD** — as §C above.

**Sub-wave 7 DoD:**
- CP-M6-7-1 sealed under §3.3.
- CP-M6-7-2 sealed under §3.3.
- CP-M6-7-3 sealed under §3.3.
- Wave-close report `notes/W_M6_TARGET_OUTCOME_PLANNER_close.md` authored.
- Ratchet delta target: +24..+30 (three CPs at 8-10 each).
- Boundary probes #55..#57 target: all NOTE-SKIPPED per SEC halt (probe loop resumes only after JUMP custody rotation to JSON).
- Word-boundary executive-domain negative-scan CLEAN on every seal.
- §3.1 P038 tokens-not-waveforms discipline preserved on every new API surface.
- HALT boundary held.

**Owner-facing report cadence:** at sub-wave 7 seal OR genuine HALT.  No CP-level owner-facing reports.

**Owner-desk items still open (unchanged this shift):**
- SEC incident ratification in `STATE/DECISIONS.md`.
- JUMP root credential rotation (+ optional custody-format migration to JSON).
- Admin SG binds for CD + Visitors.

---

## §F · Onward (post-sub-wave-7)

- Sub-wave 8 · calibration (§11.2 V113) + acceptance (§11.3 V114 milestone-list contract).
- Sub-wave 9 · Commission View surface (§13).
- Sub-wave 10 · §11.6 full training runs on real estate data — **expected HALT-to-owner at sub-wave open** per owner direction (real estate voice/biometric material triggers M6 wave-honest-limit HALT; author sub-wave brief, surface the halt, do NOT train on real estate data without an explicit owner ruling).
- Post-M6: M7 opens (W0..W9 · already ratified).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
