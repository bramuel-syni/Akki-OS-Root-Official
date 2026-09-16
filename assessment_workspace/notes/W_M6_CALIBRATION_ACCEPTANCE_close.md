# W-M6-CALIBRATION-ACCEPTANCE · Sub-wave 8 · Wave-close report

**Wave closed at UTC:** 2026-09-16T~02:36Z
**Wave name:** W-M6-CALIBRATION-ACCEPTANCE (M6 · sub-wave 8 · eighth of ten sub-waves).
**Canon scope:** §11.2 (P179..P180 · V113 LOAD-BEARING) + §11.3 (P181..P182 · V114).
**Track-a HEAD at close:** `b7ebccbeffd9795573a0a9f6c1e3ed439fa235a7`
**Master HEAD at close:** `0b91b1dd6d7fa14a58a63f548180771d97aac5c4` (§3.3 · both SHAs recorded at CP close via Commit C fixup)
**Ratchet trajectory:** 4318 → 4328 → 4338 (+20 invariants across 2 CPs).

---

## §A · Progress made

Sub-wave 8 delivers the audio-plane's *calibration procedure* + *milestone-list contract* — the point at which the training planner's forward-reference stubs (`MilestoneListRef`, `CostQuoteWithCI` via CP-M6-7-3) crystallise into a live V113/V114 contract: a plan without a calibration stage is rejected, a full-run quote without a CI is rejected, and a commission cannot open until the objective owner has reviewed and agreed the milestone list.

**Two CPs sealed under §3.3 (both SHAs recorded at each CP close):**

1. **CP-M6-8-1 · §11.2 P179..P180 Calibration Procedure (V113 · LOAD-BEARING · verbatim) · +10 invariants · ratchet 4318 → 4328 · OPENS SUB-WAVE 8.**  New module `services/audio_plane_v1/calibration.py` — 11-export surface: `CALIBRATION_MIN_VOLUMES=3` · `CALIBRATION_MAX_VOLUMES=4` (V113a closed range) · `CalibrationVolume` (frozen 2-carrier) · `PerStratumTestSetEval` (frozen 3-carrier · V113b) · `ScalingCurveFit` (frozen 2-carrier · V113c) · `CalibrationOutput` (frozen 4-carrier · V113a refusal + V113d extrapolation Mapping) · `assert_full_run_quote_has_ci` (V113e refusal on bare float + duck-type) · `assert_plan_has_calibration_stage` (V113f refusal on False) · 3 error classes.  Composes with CP-M6-7-3: imports `CostQuoteWithCI` from `training_planner.py` (no modification; verified by module_fabric asserting CP-M6-7-3's 18 exports remain present).
2. **CP-M6-8-2 · §11.3 P181..P182 Milestone-list contract (V114 · verbatim) · +10 invariants · ratchet 4328 → 4338 · CLOSES SUB-WAVE 8.**  New module `services/audio_plane_v1/milestones.py` — 10-export surface: `Milestone` (frozen 3-carrier · V114b done-condition + owner mandatory) · `MilestoneList` (frozen 3-carrier · V114a ordered milestones + Optional agreement ref + commission_id) · `construct_milestone_list` (V114a factory · refuses empty) · `agree_milestone_list` (V114c gate · returns new frozen with agreement ref; refuses re-agreement per V114d) · `assert_commission_open_only_after_agreement` (V114c refusal) · 5 error classes.  Standalone authoring surface — no composition-import with prior audio_plane_v1 modules in this CP (V117 forward-reference `MilestoneListRef.ref` will resolve at sub-wave 9 §13 Commission View).

**Discipline held throughout:**

- Tests-first RED banked per CP with right-reason `ModuleNotFoundError` for the new module before implementation existed.
- Double-green byte-match at every seal: stripped-sha256 recorded (CP-M6-8-1 `2f88dd07…` · CP-M6-8-2 `56e402a6…`); both runs byte-identical after transient-timing strip.
- Ratchet monotonic-up in `baseline_failures.json` `counts_at_baseline.passed` + `passed_floor` bumped in tandem; `ratchet_history` entries appended at each CP.
- §3.3 3-commit pattern executed at each CP (A code → B state · master TBD → C state fixup · master landed); both SHAs recorded in seal + DECISIONS + NEXT at CP close.
- No refactor of prior `audio_plane_v1/*` modules (CP-M6-7-2 · CP-M6-7-3 Part-B · calibration.py stays untouched from CP-M6-8-1 through CP-M6-8-2).
- Verbatim canon anchors in every gating test's docstring AND in each module's docstring (SO §2 CONDITION 1 discipline).
- Word-boundary executive-domain + audio-material negative-scans CLEAN at every seal.
- §3.1 P038 tokens-not-waveforms discipline preserved — no audio bytes / waveforms cross any surface added this sub-wave; every field is opaque metadata.
- Synthetic-fixtures-only in tests; no real estate voice/biometric material touched.
- Boundary probes #58 (CP-M6-8-1) + #59 (CP-M6-8-2) both NOTE-SKIPPED per standing SEC halt (JUMP custody rotation to JSON pending owner action).

---

## §B · How much to go

**M6 §15 walk position after sub-wave 8 close: 8 of 10 sub-waves complete + M6 open report banked · 2 sub-waves remain in M6.**

| Sub-wave | Scope | Status |
|---|---|---|
| 1 · W-M6-INGEST-STAGE-1 | §4.1..§4.4 pluggable seams (language ID · code-switch · channel condition · synthesis attributes) | ✅ CLOSED (2026-09-15) |
| 2 · W-M6-DEDUP-INSTANCE-CONDITION-MAP | §4.5..§4.6 dedup + condition-map | ✅ CLOSED |
| 3 · W-M6-CHARACTER-REGISTER | §5.1..§6.4 register + §6.3 P100 four-leakage-path lock | ✅ CLOSED |
| 4 · W-M6-CODEC-SERVICE | §3 perception/audio_codec/ registration + census + perimeter | ✅ CLOSED |
| 5 · W-M6-CLUSTERING-HUMAN-VALIDATION | §5.3 clustering + human validation + cluster-stability | ✅ CLOSED |
| 6 · W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA | §8 + §9 + §12.1 wizard/schema/namespace + Ratified-vs-INFERRED registry | ✅ CLOSED |
| 7 · W-M6-TARGET-OUTCOME-PLANNER | §10 + §11.1 + §11.4 outcome + planner architecture + outputs | ✅ CLOSED |
| 8 · W-M6-CALIBRATION-ACCEPTANCE | §11.2 + §11.3 calibration procedure + milestone-list contract | ✅ **CLOSED THIS WAVE** |
| 9 · W-M6-COMMISSION-VIEW | §13 commission-view surface | 📋 OPEN NEXT (owner standing GO covers this SW · synthetic-fixture-safe) |
| 10 · W-M6-FULL-TRAINING-RUNS | §11.6 full training runs on real estate data | 📋 **HALT-TO-OWNER at open** (real estate voice/biometric material triggers M6 §E.5 HALT · brief authored then stop) |

**M6 remaining ratchet estimate:** sub-wave 9 target +15..+25 (commission-view surface §13 · listing + status + acceptance-bar readout + milestone rollup) · sub-wave 10 owner-gated (no build until owner rules on real-estate audio access · grounding brief only, then HALT).

---

## §C · Decisions taken

- **CP-M6-8-1 module packaging** — landed as new module `calibration.py` (not extension of `training_planner.py`) because V113 is architecturally distinct from V109..V112 planner architecture and V115..V118 planner outputs: calibration is the *pricing procedure* (first commissioned stage), whereas the planner outputs are the *authoring surface* that consumes calibration's extrapolation.  Two modules · clear one-way import (`calibration` reads `CostQuoteWithCI` from `training_planner`).
- **CP-M6-8-2 module packaging** — landed as new module `milestones.py` (standalone).  V114 defines the milestone-list contract as `Sampling & Reflection's output to the objective owner` — a distinct authoring surface from either calibration or the planner outputs.  Keeping the three concepts in three modules (`calibration.py` · `training_planner.py` · `milestones.py`) matches the canon's own paragraph flow (§11.2 · §11.4 · §11.3 respectively) and keeps each CP's public API small and reviewable.
- **V114c agreement-ref opacity** — chose to treat `commission_agreement_ref` as an opaque `str` (no signature / no authenticator / no receipt binding at this CP).  Rationale: V114c gates the shape ("None → refused; non-None → accepted"); the *verification* of the reference is a Watch / Commission View concern (sub-wave 9 + Watch surface).  Documented in `agree_milestone_list`'s docstring and CP-M6-8-2 seal §B.
- **V114d re-agreement refusal** — `agree_milestone_list` returns a NEW frozen `MilestoneList` via `dataclasses.replace`; re-calling `agree_milestone_list` on an already-agreed list refuses `MilestoneListAlreadyAgreedError`.  This makes V114d ("from that point, all reporting is against it") a *value-semantics* invariant, not a mutation invariant: the original unagreed list is not corrupted, and an agreed list cannot silently drift.
- **No composition-import in CP-M6-8-2** — `milestones.py` intentionally does NOT import from `calibration.py` or `training_planner.py` in this CP.  V117's forward-reference stub `MilestoneListRef.ref` will resolve to a concrete `MilestoneList` at sub-wave 9's Commission View surface via a downstream registry.  This keeps sub-wave 8 scope focused on V113 + V114 alone and defers the cross-carrier composition to §13 where it belongs.
- **Boundary probe suspension continues** — probes #58 + #59 NOTE-SKIPPED under standing SEC halt from `sec_incident_jump_cred_leak_20260915T222935Z`; owner Path β ratification unchanged.

---

## §D · Discoveries not envisioned at planning

- **Boot-ritual disk-state reconciliation at session open** — the incoming session-analysis claimed run-1 was banked and ratchet-bumped, and disk confirmed both.  However, disk also carried: (i) an uncommitted `.pyc` cache modification, (ii) a stray untracked `backend/phase0/drill_receipts/` directory in the Extraction-Akki code repo (Sep-15 09:33–10:54 legacy from a prior session's misdirected write; not related to sub-wave 8), and (iii) unrelated modifications on the workspace master (`STATE/PINS.md` commissioning_record pointer drift and `phase0/mtafiti_gpu_discovery/*` snapshot updates from an unrelated automation).  None of these blocked sub-wave 8 seals; all deferred to a future housekeeping cycle.  Documented for future §3.3 boot rituals to expect: dirty working trees are common, and the discipline is to stage ONLY the CP-scoped files.
- **Double-green run-2 output-mode discrepancy** — the sub-wave-8 opening receipt authoring convention runs `BASELINE_GUARD=1 python -m pytest tests/invariants/` under `-q` to yield 9844 B outputs matching CP-M6-8-1's byte-match convention.  A first run-2 attempt without `-q` produced a 46,819 B verbose per-file listing (same 4338 passed tally) — non-matching raw byte count with run-1.  Redone with `-q` → clean 9844 B match.  Documented so future double-green runs mirror the previous CP's invocation exactly (not just the STANDING_ORDERS §3 canonical form).
- **§11.3 V114 shape debate settled at authoring time** — V114b names two mandatory fields on each milestone (`done-condition` + `owner`).  A candidate optional field `mission_alignment_ref` was considered (per SW-8 grounding brief §D DEFAULT-PENDING-OVERRIDE) but not landed.  V114 text itself does not name a mission-alignment carrier; the mission-alignment concern lives at the Commission View level (§13) where the milestone list is *reviewed against* the objective's mission.  Kept the minimal 3-carrier form; owner override remains available if V114-plus surfaces later.
- **V117 forward-reference posture confirmed at close** — CP-M6-7-3's `MilestoneListRef` (a 1-carrier ref-string stub) and CP-M6-8-2's `MilestoneList` (full 3-carrier authoring surface) do not import each other.  They connect at sub-wave 9's Commission View registry.  This keeps the module-fabric graph acyclic and makes sub-wave 9's job explicit: "resolve MilestoneListRef.ref → MilestoneList and enforce V114c agreement before commission-open" is one concrete CP in SW-9.

---

## §E · Recommendations to make the experience better, in line with the mission

The mission this sub-wave serves — *the training planner's forward-references become live V113/V114 contracts that price the real job (calibration → CI-quoted full-run) and author accountability before spend (milestone list · agreed before commission-open)* — is now landed in code.  Three recommendations for the owner:

1. **Consider ratifying the SEC incident** in the owner's next DECISIONS turn.  Boundary probes #54 through #59 have all NOTE-SKIPPED at CP boundaries under the standing SEC halt.  The probe loop is a distinct honesty surface (proves the estate boundary is closed against CD/Visitors even though those admin binds are pending); it is not blocking sub-wave build progress, but a formal ratification would let the loop resume observing (not gating) if the owner authorizes a JUMP custody rotation to JSON with the current Redaction Hardening Option 1 helper.  Standing recommendation only — no action required to continue building.
2. **Sub-wave 9 is synthetic-fixture-safe** and covered by the owner's standing GO ("Continue with build autonomously") per the session-open ruling.  Sub-wave 9's §13 Commission View surface reads the CP-M6-7-1 TargetOutcome + CP-M6-8-1 CalibrationOutput + CP-M6-8-2 MilestoneList and renders them as a first-class review artefact.  No real-estate material required; all fixtures can be synthesised from the frozen carriers in `audio_plane_v1/*`.  Sub-wave 9 grounding brief follows this close report in the same session turn.
3. **Sub-wave 10 HALT-to-owner boundary is one sub-wave away.**  §11.6 full training runs on real estate voice/biometric material is the M6 §E.5 HALT trigger.  When sub-wave 9 closes, sub-wave 10 will open a grounding brief that flags the HALT immediately and stops before touching estate audio.  Owner may want to prepare the ruling on real-estate audio access ahead of that boundary so the sub-wave doesn't sit idle at the HALT gate.  Concrete decision surfaces for the ruling: (i) which estate audio corpus is in-scope (§4.1 language IDs · §4.3 channel classes) · (ii) which retention path applies (Audio-bytes-retention Path A/B/C · currently pending) · (iii) whether §6.3 P100 four-leakage-path harness is exercised against synthetic-only fixtures or against a small chartered real-material fixture with §6.4 P102 read-scope enforcement.

---

## §F · Owner-desk items outstanding (carried per SO §2 milestone-boundary cadence)

- **SEC incident ratification** in `STATE/DECISIONS.md` (`sec_incident_jump_cred_leak_20260915T222935Z` · owner Path β pending formal ratification).
- **JUMP root credential rotation** (+ optional custody-format migration from CSV to JSON — the CP-SW6-HYG-1 helper is version-controlled and ready).
- **Admin SG binds for CD + Visitors** — filed credentials at `/app/backend/estate_keys/data_sources/admin_bind_20260915_bramuel_cd_visitors.json` await SG openings; NAS-username spelling correction pending (`bramuel` filed vs `bramwel` as NAS spelling).
- **Audio-source unblocks + Audio-plane sensitivity declarations** — parked per owner.
- **Path α/β ruling for M6-INGEST-STAGE-1** — parked per owner.
- **BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 build charters · D9 receipt-unify · Amendment 8 HOLD · SEC rotations · R-17(a) (non-blocking) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine** — all unchanged from prior milestone-boundary reports.

---

## §G · Onward

**Sub-wave 9 · W-M6-COMMISSION-VIEW · §13 Commission View surface.**  Grounding brief follows this close report in the same session turn (owner standing GO covers SW-9 · synthetic-fixture-safe).  Tests-first RED → mechanism → double-green byte-match → seal → §3.3 3-commit per CP.  Ratchet target: +15..+25.

**Sub-wave 10 · W-M6-FULL-TRAINING-RUNS · §11.6 full training runs — HALT-TO-OWNER at open.**  After SW-9 closes, author the SW-10 grounding brief, flag the HALT, and stop until owner rules on real-estate audio access.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
