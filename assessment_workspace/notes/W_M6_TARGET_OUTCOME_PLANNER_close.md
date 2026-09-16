# W-M6-TARGET-OUTCOME-PLANNER · Sub-wave 7 · Wave-close report

**Wave closed at UTC:** 2026-09-16T~01:59Z
**Wave name:** W-M6-TARGET-OUTCOME-PLANNER (M6 · sub-wave 7 · third of ten sub-waves).
**Canon scope:** §10 (P153..P169) + §11.1 (P171..P178) + §11.4 (P184..P188).
**Track-a HEAD at close:** `d411cc70bea163f75f082e3ac5a0e688338d6e54`
**Master HEAD at close:** `664c51f7d93aae7605aa08656b70086857fcf1b5`
**Ratchet trajectory:** 4288 → 4298 → 4308 → 4318 (+30 invariants across 3 CPs).

---

## §A · Progress made

Sub-wave 7 delivers the audio-plane's *Target Outcome authoring* + *Training Planner* seams — the point at which the register-derived strata become the object of a planner that must remain deterministic-at-core, learned-only-on-reorder, gate-checked against baseline, and reproducible from recorded inputs.

**Three CPs sealed under §3.3 (both SHAs recorded at each CP close):**

1. **CP-M6-7-1 · Full §10 TargetOutcome carrier + §10.2 binding rules (V98..V108 verbatim) · +10 invariants · ratchet 4288 → 4298.**  New module `services/audio_plane_v1/target_outcome.py` — 10-export frozen 7-carrier + factory + four construction-time refusals (`GatePolicyInvalidError` V102 · `PopulationEmptyStrataRefsError` V105 · `TestSetRefMissingError` V107 LOAD-BEARING · `AcceptancePerStratumMissingError` V106).  Composes with sub-wave 6 `AcceptanceBar` via import; `objective_wizard.py` unchanged (`TargetOutcomeStub` remains callable for backward compat).
2. **CP-M6-7-2 · §11.1 P171..P178 Training Planner architecture (V109..V112 verbatim) · +10 invariants · ratchet 4298 → 4308.**  New module `services/audio_plane_v1/training_planner.py` — 10-export four-clause seam: deterministic core (`PlannerCore` Protocol) → strip (`strip_eligibility_decision`) → learned reorder (`LearnedReorderLayer` Protocol) → gate (`run_eligibility_gate`) → reproducibility witness (`PlanReproducibilityWitness` bound via sha256 pair).  Two refusals: `LearnedReorderStrippingViolationError` (V109 · strict `type(x) is EligibilityDecision` check refuses subclasses AND duck-types) · `EligibilityGateSlippageError` (V109 · membership divergence rejected; ordering may differ).
3. **CP-M6-7-3 · §11.4 P184..P188 Planner outputs (V115..V118 verbatim) · +10 invariants · ratchet 4308 → 4318 · CLOSES SUB-WAVE 7.**  Append-only Part-B extension of `training_planner.py` — 8 new exports across 6 frozen carriers (`PerStratumCoverageEntry` · `CoverageReport` · `CurriculumOrdering` · `CostQuoteWithCI` · `MilestoneListRef` · `PlannerOutputs`) + 2 refusals (`CostQuoteMissingCIError` V118 LOAD-BEARING · `CurriculumWeightNormalizationError` V116).

**Discipline held throughout:**

- Tests-first RED banked per CP with right-reason ModuleNotFoundError / ImportError before implementation existed.
- Double-green byte-match at every seal: stripped-sha256 recorded in each CP's seal file; both runs byte-identical after transient-timing strip.
- Ratchet monotonic-up in `baseline_failures.json` `counts_at_baseline.passed` + `passed_floor` bumped in tandem; `ratchet_history` entries appended at each CP.
- §3.3 3-commit pattern executed at each CP (A code → B state · master TBD → C state fixup · master landed); both SHAs recorded in seal + DECISIONS + NEXT.
- No refactor of prior audio_plane_v1 modules (CP-M6-3-1 CharacterRegister · CP-M6-5-1..5-3 clustering + human-validation + stability · CP-M6-6-1..6-4 sub-wave 6 all unchanged).
- Verbatim canon anchors in every gating test's docstring AND in each module's docstring (SO §2 CONDITION 1 discipline).
- Word-boundary executive-domain + audio-material negative-scans CLEAN at every seal.
- §3.1 P038 tokens-not-waveforms discipline preserved — no audio bytes / waveforms cross any surface added this sub-wave; every field is opaque metadata.
- Synthetic-fixtures-only in tests; no real estate voice/biometric material touched.
- Boundary probes #55 + #56 + #57 all NOTE-SKIPPED per SEC halt (JUMP custody rotation to JSON pending).

---

## §B · How much to go

**M6 §15 walk position after sub-wave 7 close: 7 of 10 sub-waves complete + M6 open report banked · 3 sub-waves remain in M6.**

| Sub-wave | Scope | Status |
|---|---|---|
| 1 · W-M6-INGEST-STAGE-1 | §4.1..§4.4 pluggable seams (language ID · code-switch · channel condition · synthesis attributes) | ✅ CLOSED (2026-09-15) |
| 2 · W-M6-DEDUP-INSTANCE-CONDITION-MAP | §4.5..§4.6 dedup + condition-map | ✅ CLOSED |
| 3 · W-M6-CHARACTER-REGISTER | §5.1..§6.4 register + §6.3 P100 four-leakage-path lock | ✅ CLOSED |
| 4 · W-M6-CODEC-SERVICE | §3 perception/audio_codec/ registration + census + perimeter | ✅ CLOSED |
| 5 · W-M6-CLUSTERING-HUMAN-VALIDATION | §5.3 clustering + human validation + cluster-stability | ✅ CLOSED |
| 6 · W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA | §8 + §9 + §12.1 wizard/schema/namespace + Ratified-vs-INFERRED registry | ✅ CLOSED |
| 7 · W-M6-TARGET-OUTCOME-PLANNER | §10 + §11.1 + §11.4 outcome + planner architecture + outputs | ✅ **CLOSED THIS WAVE** |
| 8 · W-M6-CALIBRATION-ACCEPTANCE | §11.2 + §11.3 calibration procedure + milestone-list contract | 📋 OPEN NEXT |
| 9 · W-M6-COMMISSION-VIEW | §13 commission-view surface | 📋 FOLLOWS |
| 10 · W-M6-FULL-TRAINING-RUNS | §11.6 full training runs on real estate data | 📋 **HALT-TO-OWNER at open** (real estate voice/biometric material triggers M6 §E.5 HALT) |

**M6 remaining ratchet estimate:** sub-wave 8 target +18..+24 (calibration procedure ≥ V113 verbatim + milestone-list contract V114) · sub-wave 9 target +15..+25 (commission-view surface §13) · sub-wave 10 owner-gated (no build until owner rules on real-estate audio access).

---

## §C · Decisions taken

- **CP-M6-7-1 packaging** — landed as new module `target_outcome.py` (not extension of `objective_wizard.py`) because sub-wave 7 opens a new architectural area (§10 Target Outcome + §11 Training Planner) separate from sub-wave 6's compile-refusal machinery, and `objective_wizard.py` already carries the STUB territory that stays live for backward compat.  `TargetOutcomeStub` untouched.
- **CP-M6-7-2 module packaging** — landed as new module `training_planner.py` (not extension of `target_outcome.py`) because the four-clause architecture seam is a distinct concept from the outcome carrier: outcome is authored by the wizard; planner-run reads the outcome and produces an ordered plan.  Two modules · clear one-way import (`training_planner` reads `target_outcome`).
- **CP-M6-7-3 packaging** — landed as append-only Part-B extension of `training_planner.py` under a marked header (`# Part-B · §11.4 ...`) rather than a third module.  Rationale: `PlannerOutputs` is the *result* of `run_eligibility_gate` + downstream composition; keeping outputs alongside architecture in one module keeps the planner-shape surface cohesive and reflects §11's own paragraph flow (§11.1 → §11.4).
- **V109 strip enforcement discipline** — chose strict `type(x) is EligibilityDecision` (identity check) over `isinstance(x, EligibilityDecision)` because subclasses can carry extra attributes that would silently leak values-that-decided-eligibility into the learned reorder layer's view.  Documented in `strip_eligibility_decision`'s docstring and refusal message.
- **V116 register-not-corpus discipline** — refusal fires only on the numerical clause (weight normalization); the architectural clause ("derived from the register, not from the corpus's natural distribution") is stated as a wave-honest limit and enforced by downstream composition, not by carrier shape.  Documented in CP-M6-7-3 seal §B.
- **V117 forward-reference stub** — `MilestoneListRef` carries only a `ref: str`; the §11.3 milestone-list content contract (V114) is scheduled for sub-wave 8 alongside the calibration procedure.  This keeps sub-wave 7 scope focused and avoids landing partial §11.3 machinery.
- **Boundary probe suspension** — probes #55 + #56 + #57 all NOTE-SKIPPED under the standing SEC halt from `sec_incident_jump_cred_leak_20260915T222935Z`; owner Path β ratification unchanged.

---

## §D · Discoveries not envisioned at planning

- **§3.3 partial-seal drift on CP-M6-7-1 re-grounding at session boot.**  The prior handoff summary claimed Commit A landed at `88cff9a`; disk showed the CP mechanism + tests + ratchet-bump present but the seal file, DECISIONS entry, and NEXT pin still carrying `TBD-COMMIT-A` and `TBD` (master).  Boot-ritual disk reconciliation showed the true track-a HEAD at CP-M6-7-1 was `479377c` (not `88cff9a`), and Commits B/C for CP-M6-7-1 had never landed on master.  Healed under §3.3 pattern: Commit B on master at `868f694e` → Commit C fixup at `b51e7044`.  This surfaces §3.3's protection against exactly the "partial-seal drift" class the rule was written to close: the CP-M6-7-1 mechanism was authored and green but not §3.3-sealed until this shift's boot-ritual work.
- **Ruff `F822 Undefined name in __all__`** during Part-B `__all__` update.  Expected under tests-first authoring (declare exports before defining them); resolves on Part-B class definitions landing.  Not a §3 discipline violation; the true gate is `BASELINE_GUARD=1 pytest`, which stays green at 4318 after Part-B implementation.  Documented so future §3.3 3-commit patterns anticipate the transient lint state between `__all__` update and class definitions.
- **Stray untracked `backend/phase0/drill_receipts/` in the code repo.**  Legacy directory from a prior session's misplaced write.  Not related to this sub-wave's work; not staged into any Commit A.  Logged for a future housekeeping cycle; no action this sub-wave.
- **PINS.md auto-emit** during the same session window (a `commissioning_record` pointer update from `_update_pins()` in `services/connect/gpu_submit.py`).  Unrelated to sub-wave 7; left uncommitted per the standing pattern.

---

## §E · Recommendations to make the experience better, in line with the mission

The mission this sub-wave serves — *audio-plane authoring surfaces the register-derived strata to the model builder as a first-class contract, and the training planner enforces that reproducibility is a property of the plan, not a promise of the person building it* — is now landed in code.  Three recommendations for the owner:

1. **Consider ratifying the SEC incident in the owner's next DECISIONS turn.**  Boundary probes #54 through #57 have all NOTE-SKIPPED at CP boundaries.  The probe loop is a distinct honesty surface (proves the estate boundary is closed against CD/Visitors even though those admin binds are pending); it is not blocking sub-wave build progress, but a formal ratification would let the loop resume observing (not gating) if the owner authorizes a JUMP custody rotation to JSON with the current Redaction Hardening Option 1 helper.  Standing recommendation only — no action required to continue building.
2. **Sub-wave 8's §11.3 milestone-list contract will need one small owner ruling.**  V114 (§11.3 P183) mentions "the mission that the milestone list expresses" but is otherwise architectural.  Sub-wave 8's grounding brief will surface a `DEFAULT-PENDING-OVERRIDE` on the milestone-list carrier shape (e.g., whether to include a `binding_ruling_ref` field for the mission owner's approval anchor); the default will be minimal (name + ordering only), overridable in the next owner turn.
3. **Sub-wave 10 HALT-to-owner boundary is now approximately 2 sub-waves away.**  §11.6 full training runs on real estate voice/biometric material is the M6 §E.5 HALT trigger.  When sub-wave 8 + sub-wave 9 close, sub-wave 10 will open a grounding brief that flags the HALT immediately and stops before touching estate audio.  Owner may want to prepare the ruling on real-estate audio access ahead of that boundary so the sub-wave doesn't sit idle at the HALT gate.

---

## §F · Owner-desk items outstanding (carried per SO §2 milestone-boundary cadence)

- **SEC incident ratification** in `STATE/DECISIONS.md` (`sec_incident_jump_cred_leak_20260915T222935Z` · owner Path β pending formal ratification).
- **JUMP root credential rotation** (+ optional custody-format migration from CSV to JSON — the CP-SW6-HYG-1 helper is version-controlled and ready).
- **Admin SG binds for CD + Visitors** — filed credentials at `/app/backend/estate_keys/data_sources/admin_bind_20260915_bramuel_cd_visitors.json` await SG openings; NAS-username spelling correction pending ('bramuel' filed vs 'bramwel' as NAS spelling).
- **BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 build charters · D9 receipt-unify · Amendment 8 HOLD · SEC rotations · R-17(a) (non-blocking) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine** — all unchanged from prior milestone-boundary reports.

---

## §G · Onward

Sub-wave 8 · W-M6-CALIBRATION-ACCEPTANCE · §11.2 (V113 · sampling & reflection · calibration procedure) + §11.3 (V114 · milestone-list contract).  Grounding brief authored at wave open.  Tests-first RED → mechanism → double-green byte-match → seal → §3.3 3-commit per CP.  Ratchet target: +18..+24.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
