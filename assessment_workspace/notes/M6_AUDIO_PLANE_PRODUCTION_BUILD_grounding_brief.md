READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M6 · Audio-Plane v1.0 Production Build · Grounding Brief

**Milestone:** M6 (FORMAL as of 2026-09-15T~04:12Z owner ratification · see `notes/MILESTONE_PROMISE_BINDING_20260915_delta_M6M7M8_ratified.md` §Δ2).

**Source canon:** `notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md` §15 (P225..P240) + all v1.0 §-references cited per sub-wave.

**Standing law:** `STATE/STANDING_ORDERS.md` — every clause below binds unmodified.

**Authored:** 2026-09-15T~04:15Z (closed egress window · non-egress work) · owner authorization for authoring-and-proceeding without ack gate at §A below.

**Discipline of this brief:** every requirement in scope carries a verbatim quote from `AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md` with its paragraph index `P###` and section reference · zero paraphrasing.

---

## §A · Owner ratification · verbatim

Owner text 2026-09-15T~04:12Z (`STATE/DECISIONS.md` 2026-09-15T~04:12Z · `notes/MILESTONE_PROMISE_BINDING_20260915_delta_M6M7M8_ratified.md` §A):

> "🧭M6 (Audio-Plane production build, §15 order) ... are now FORMAL milestones."

> "Then M6 open: author the M6 grounding brief (fix the N7 numbering gap there), then walk §15 items in canon order starting W-M6-INGEST-STAGE-1. Post the brief in your report and PROCEED — no ack gate, per owner autonomy ruling."

**Authoring authority:** this brief is authored under the autonomous-execution mode ratified 2026-09-15T~04:12Z. Proceed to W-M6-INGEST-STAGE-1 at the sequenced open time (owner order: M5 completion → M8 quick hardening → M6 opens). No ack gate.

---

## §B · Verbatim §15 build sequence (canon-authored dependency order)

Source: `notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md:303-303+` (§15 P225..P240).

**§15 P225 opener (verbatim):**

> *"The following order is a build sequence, not a scope statement. Every item in this section is required for the Plane to function; the ordering minimises rework by making each item's prerequisites exist before the item lands."*

**§15 §15.1..§15.11 (verbatim in canon order):**

| # | Verbatim §15 item | Location | Prerequisite (verbatim if stated) |
|--:|---|---|---|
| 1 | *"Ingestion capture — language ID, code-switch points, condition profile, synthesis attributes (§4.1–§4.4)"* | P232 | Independent (first ingestion pipeline landing) |
| 2 | *"Dedup instance condition map (§4.5)"* | P233 | *"Requires ingestion capture in place (item 1)"* |
| 3 | *"Character Register schema + custody invariant harness (§6)"* | P234 | *"Boundary must exist before first cluster stored"* (P234.s2) |
| 4 | *"Codec service (§3) · perception/audio_codec/"* | P235 | *"Independent of 1–3 (unsupervised pretraining is parallel)"* (P235.s2) |
| 5 | *"Clustering + sampled human validation (§5.3)"* | P236 | *"Requires items 1–4"* (P236.s2) |
| 6 | *"Objective Wizard variant + Collection Schema type + registry namespace (§8, §9, §12.1)"* | P237 | *"Independent — but planner-first refuses malformed input"* (P237.s2) |
| 7 | *"TargetOutcome type + planner core (§10, §11.1, §11.4)"* | P238 | *"Requires items 3 + 6"* (P238.s2) |
| 8 | *"Sampling & Reflection machinery + milestone records (§11.2–§11.3)"* | P239.a | *"Requires item 7 + a test set to reflect against"* (P239.a.s2) |
| 9 | *"Commission View (§13)"* | P239.b | *"Requires item 8"* (P239.b.s2) |
| 10 | *"Full training runs under the commissioned-job contract (§11.6)"* | P239.c | *"Requires items 7–9"* (P239.c.s2) |
| P2 | *"Voice identity rendering; music register (§7.5 non-foreclosure)"* | P240 | *"Non-foreclosure only this milestone; production landing is Phase-2."* (P240.s2) — **DEFERRED BY DESIGN** |

---

## §C · Sub-wave breakdown · 10 core + 1 P2-deferred

### Sub-wave 1 · W-M6-INGEST-STAGE-1 · Ingestion capture (§4.1–§4.4)

**Scope (verbatim canon anchors):**
- §4.1 language ID at segment level — `AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md:92 (N1)` verbatim: *"A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."*
- §4.2 code-switch points — verbatim per §4.2 P061..P062 (specify at CP-M6-1-1 open per verbatim §4.2).
- §4.3 channel condition profile — `:93 (N2)` verbatim: *"Channel condition — studio / field / telephone band, transmission artefacts, background class — is derived per segment at first ingestion."*
- §4.4 synthesis attributes — verbatim per §4.4 P068..P070 (specify at CP-M6-1-4 open per verbatim §4.4).

**Open owner-input rulings folded but NOT gating open:**
- **D10** (Silero VAD INFERRED) — grounding brief at CP-M6-1-1 open MUST name the canon-INFERRED starting point (currently `w11_stepA_base_models.md:148` fastText LID.176 mentioned but not canon-named) and mark for owner ratification.
- **D11** (pyannote/speaker-diarization-3.1 INFERRED) — same discipline.
- Both drift-items are RULING_LEDGER OPEN row 13. Proceed with `[INFERRED-pending-ratification]` markers; wave lands the pluggable seam that admits ratified model on ratification.

**CP breakdown (estimate: L · ~1 week concentrated):**
- CP-M6-1-1 · language ID at segment level (D10-anchor) — TESTS-FIRST · new invariant: language ID emitted per-segment · offline · in-perimeter · CPU-viable check.
- CP-M6-1-2 · code-switch point detection — TESTS-FIRST · new invariant: code-switch points annotated with confidence + language-pair.
- CP-M6-1-3 · channel condition profile derivation — TESTS-FIRST · new invariant: per-segment channel condition ∈ {studio, field, telephone-band} + transmission-artefacts + background-class carriers.
- CP-M6-1-4 · synthesis attributes — TESTS-FIRST · new invariant: synthesis-attribute carrier per Audio-Plane §4.4 verbatim.

**Prerequisite for open:** M5 complete (census + release-gate + D12 POC) — provides the transcript-tokenized artefact + release-gate machinery that CP-M6-1-4 releases synthesis attributes through.

---

### Sub-wave 2 · W-M6-DEDUP-INSTANCE-CONDITION-MAP · §4.5

**Scope (verbatim canon anchor):**
- `:94 (N3)` verbatim: *"[F]or each deduplicated item, the instance condition map … is retained."*

**CP breakdown (estimate: S · ~2 days):**
- CP-M6-2-1 · instance condition map schema — TESTS-FIRST · new invariant: dedup preserves per-instance condition map (channel + language + synthesis attributes per §4.3–§4.4).
- CP-M6-2-2 · dedup path extension — TESTS-FIRST · new invariant: dedup collapse never drops a distinct condition; distinct conditions produce distinct instances even when text-identical.

**Prerequisite for open:** W-M6-INGEST-STAGE-1 sealed (dedup extends over §4.1–§4.4 carriers).

---

### Sub-wave 3 · W-M6-CHARACTER-REGISTER · §6

**Scope (verbatim canon anchors):**
- `:96 (N5)` verbatim: *"An automated invariant test attempts each known leakage path (small stratum, idiolect marker, narrowing combination, exemplar storage) and must fail to store all of them on every change to the register code."*
- §6.1..§6.4 write-path boundary rules (specify at CP-M6-3-1 open per verbatim §6.1–§6.4).

**CP breakdown (estimate: L · ~1 week concentrated):**
- CP-M6-3-1 · Character Register schema (frozen dataclass carriers per §6.1 verbatim).
- CP-M6-3-2 · custody-invariant harness — TESTS-FIRST · 4 leakage-path invariants (small stratum · idiolect marker · narrowing combination · exemplar storage) all right-reason RED before register code lands.
- CP-M6-3-3 · write-path boundary — TESTS-FIRST · every register write refuses on leakage-path fire.
- CP-M6-3-4 · read-path scope enforcement per §6.4 verbatim.

**Prerequisite for open:** *"Boundary must exist before first cluster stored"* (§15 P234.s2 verbatim).

---

### Sub-wave 4 · W-M6-CODEC-SERVICE · §3

**Scope (verbatim canon anchor):**
- `:95 (N4)` verbatim: *"perception/audio_codec/ — registered like any other perception model; census-visible; runs in-perimeter on tenant compute."*
- §3.1–§3.2 codec registration + census surface (specify at CP-M6-4-1 open per verbatim §3.1–§3.2).

**Fold-in D7 (codec_version drift):** grounding-brief anchor for D7 lands at CP-M6-4-2 as an invariant: every codec artefact carries `codec_version` and the version identifier is a first-class carrier in the census surface.

**CP breakdown (estimate: L · ~1 week concentrated):**
- CP-M6-4-1 · perception/audio_codec/ module skeleton — TESTS-FIRST · registered-like-any-perception-model invariant.
- CP-M6-4-2 · codec_version carrier (D7 fold-in) — TESTS-FIRST · every codec artefact refuses on missing/mismatched codec_version.
- CP-M6-4-3 · census-visibility invariant — TESTS-FIRST · codec service appears in Mtafiti census surface as a registered perception capability.
- CP-M6-4-4 · in-perimeter-on-tenant-compute invariant — TESTS-FIRST · codec service refuses cross-perimeter dispatch.

**Prerequisite for open:** *"Independent of 1–3 (unsupervised pretraining is parallel)"* (§15 P235.s2) — MAY open in parallel with sub-waves 1–3.

---

### Sub-wave 5 · W-M6-CLUSTERING-HUMAN-VALIDATION · §5.3

**Scope (verbatim canon anchor):**
- §5.3 clustering with sampled human validation (specify at CP-M6-5-1 open per verbatim §5.3).

**CP breakdown (estimate: M · ~3 days):**
- CP-M6-5-1 · clustering algorithm registration per §5.3.
- CP-M6-5-2 · sampled human validation loop — TESTS-FIRST · sampling deterministic + validation record ledgered.
- CP-M6-5-3 · cluster stability invariants.

**Prerequisite for open:** *"Requires items 1–4"* (§15 P236.s2).

---

### Sub-wave 6 · W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA · §8, §9, §12.1

**Scope (verbatim canon anchors):**
- `:98 (N7)` verbatim: *"The wizard cannot emit an artifact the downstream contracts would refuse. Rejected at compile, not warned: An Outcome without an existing test_set_ref. An acceptance bar missing the per-stratum dimension. A Collection Schema requiring a column whose capture violates the custody conditions of §6.2."*
- §8 Objective Wizard audio variant (specify at CP-M6-6-1 open per verbatim §8).
- §9 Collection Schema type (specify at CP-M6-6-2 open per verbatim §9).
- §12.1 registry namespace (specify at CP-M6-6-3 open per verbatim §12.1).

**Book-keeping correction · this brief:** prior observation that N7 was skipped in the drift audit is **RETRACTED**. `AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:98` carries N7 with the full verbatim quote and `[VERIFY]` status per §16.1 P245. All 10 N-items (N1..N10) enumerated correctly. Retraction banked in `STATE/DECISIONS.md` 2026-09-15T~04:12Z Effect 6 and `notes/MILESTONE_PROMISE_BINDING_20260915_delta_M6M7M8_ratified.md` §Δ7 Correction 2.

**N7 ratification cross-link:** N7 currently PARTIAL (`AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:98` verbatim status). CP-M6-6-1 open MUST verify Objective Wizard's compile-refusal machinery (against v1.0 §16.1 P245 [VERIFY] enumeration) before landing new §8 mechanism.

**CP breakdown (estimate: M · ~4 days):**
- CP-M6-6-1 · Objective Wizard audio-variant compile-refusal (N7 fold-in) — TESTS-FIRST · 3 refusal invariants per verbatim clauses:
  - refuse *"An Outcome without an existing test_set_ref"* — RED before mechanism.
  - refuse *"An acceptance bar missing the per-stratum dimension"* — RED before mechanism.
  - refuse *"A Collection Schema requiring a column whose capture violates the custody conditions of §6.2"* — RED before mechanism.
- CP-M6-6-2 · Collection Schema type (frozen carrier per §9).
- CP-M6-6-3 · registry namespace per §12.1.

**Prerequisite for open:** *"Independent — but planner-first refuses malformed input"* (§15 P237.s2). MAY open in parallel with sub-waves 3–5.

---

### Sub-wave 7 · W-M6-TARGET-OUTCOME-PLANNER · §10, §11.1, §11.4

**Scope (verbatim canon anchors):**
- `:99 (N8)` verbatim: *"The test set precedes the training. An Outcome without an existing, stratified test set is rejected at definition time."*
- §10 TargetOutcome type (specify at CP-M6-7-1 open per verbatim §10).
- §11.1 planner core (specify at CP-M6-7-2 open per verbatim §11.1).
- §11.4 planner-first refusal (specify at CP-M6-7-3 open per verbatim §11.4).

**CP breakdown (estimate: L · ~1 week concentrated):**
- CP-M6-7-1 · TargetOutcome type (frozen carrier per §10 verbatim).
- CP-M6-7-2 · planner core per §11.1 verbatim.
- CP-M6-7-3 · N8 fold-in — TESTS-FIRST · test-set-precedes-training invariant.
- CP-M6-7-4 · planner-first refusal machinery per §11.4.

**Prerequisite for open:** *"Requires items 3 + 6"* (§15 P238.s2).

---

### Sub-wave 8 · W-M6-SAMPLING-REFLECTION · §11.2–§11.3

**Scope (verbatim canon anchors):**
- `:100 (N9)` verbatim: *"A plan without a calibration stage is rejected. The first job prices the real job."*
- §11.2 sampling machinery (specify at CP-M6-8-1 open per verbatim §11.2).
- §11.3 reflection loop + milestone records (specify at CP-M6-8-2 open per verbatim §11.3).

**CP breakdown (estimate: M · ~4 days):**
- CP-M6-8-1 · sampling machinery per §11.2.
- CP-M6-8-2 · reflection-loop per §11.3.
- CP-M6-8-3 · N9 fold-in — TESTS-FIRST · calibration-stage-required + first-job-prices-real-job invariants.
- CP-M6-8-4 · milestone-records ledger.

**Prerequisite for open:** *"Requires item 7 + a test set to reflect against"* (§15 P239.a.s2).

---

### Sub-wave 9 · W-M6-COMMISSION-VIEW · §13

**Scope (verbatim canon anchor):**
- `:101 (N10)` verbatim: *"Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified."*
- §13.1–§13.4 Commission View surface (specify at CP-M6-9-1 open per verbatim §13).

**CP breakdown (estimate: S · ~2 days):**
- CP-M6-9-1 · Commission View surface skeleton.
- CP-M6-9-2 · N10 fold-in — TESTS-FIRST · commission-view-reads-existing-artefacts-only invariant (surface element requiring new backend computation refuses at compile).
- CP-M6-9-3 · SO §4 rule-zero four-questions topline invariant on the view.

**Prerequisite for open:** *"Requires item 8"* (§15 P239.b.s2).

---

### Sub-wave 10 · W-M6-FULL-TRAINING-RUNS · §11.6

**Scope (verbatim canon anchor):**
- §11.6 commissioned-job contract for full training runs (specify at CP-M6-10-1 open per verbatim §11.6).

**CP breakdown (estimate: L · ~1 week concentrated · likely spans multi-day GPU windows):**
- CP-M6-10-1 · commissioned-job contract landing per §11.6.
- CP-M6-10-2 · full-training-run dispatch (composes with W-M5 W-SHIELD-TRAIN + W-CENSUS-CANON-ALIGN + BC packet Tier-1 GPU-DCP checkpointing if ratified).
- CP-M6-10-3 · release-gate composition with M5 W-RELEASE-GATE-PILOT-LIFT (tokenized/derivative-only artefacts).
- CP-M6-10-4 · training-run output-verified seal (`Kind: audio_plane_training_run_v1`).

**Prerequisite for open:** *"Requires items 7–9"* (§15 P239.c.s2).

**Composition note:** if M3 W-BC-DYNAMIC-RECOVERY-BUILD lands before this sub-wave opens, CP-M6-10-2 folds in BC-Tier-1 GPU-DCP async checkpointing (Young/Daly cadence · ~10-15 min GPU compute loss ceiling). If not yet ratified, sub-wave uses existing checkpoint machinery from W-Shield-Train era.

---

### Sub-wave P2 · W-M6-VOICE-IDENTITY-RENDERING · §7.5 · **DEFERRED BY DESIGN**

**Scope (verbatim canon anchors):**
- `:97 (N6)` verbatim: *"Every constructed identity is scored against every speaker representation derivable from the corpus using standard speaker-verification methods. A minimum distance from all of them is required. Below threshold, the identity is rejected and resampled. There is no override."*
- §7.5 non-foreclosure clause (specify at Phase-2 open per verbatim §7.5).

**Standing:** DEFERRED BY DESIGN this milestone. Non-foreclosure only. Production landing is Phase-2 (post-M6). No CP walk under M6.

---

## §D · Book-keeping corrections

**Correction 1 · N7 numbering RETRACTION.** Prior observation that N7 was skipped in `AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md` is WRONG. N7 is present at `:98` with the full verbatim wizard-compile-refusal quote (v1.0 §8.4 P139..P142) with `[VERIFY]` status per §16.1 P245. All 10 N-items enumerated correctly. Fold-in position: N7 → sub-wave 6 CP-M6-6-1.

**Correction 2 · Pull-Seam P2..P6 backfill RETRACTION.** Prior observation that Pull-Seam Principles 2–6 bodies were missing from the on-disk ledger is WRONG. `notes/PULL_SEAM_REQUIREMENTS_VERBATIM_20260914.md` §2 contains all 8 principle bodies with sentence-level detail (39 sentence-rows) plus the six-crossing table (30 cell-quotes). No backfill required before W-PULL-SEAM-RECEIPT-UNIFY charter opens under M2.

**Standing rule banked from these corrections:** before surfacing a book-keeping observation as owner-actionable, the observation MUST cite the target file + section + line-range and quote the observed gap. An observation that cannot supply the citation is an inference, not a finding, and does not surface to the owner. Applies to all future book-keeping observations.

---

## §E · Wave-honest limits carried into M6

- **D10 · D11 · D7 drift-items** — INFERRED starting-points; grounding-brief-at-CP-open discipline names canon anchor + marks for owner ratification. Wave lands pluggable seams that admit ratified model on ratification without wave rework.
- **Speaker-verification threshold (N6 · Phase-2)** — DEFERRED BY DESIGN this milestone. Non-foreclosure only.
- **Commission View backend-reads-only rule (N10)** — sub-wave 9 CP-M6-9-2 refuses any surface element requiring new backend computation beyond reading existing artefacts. Strict; no wave-honest-limit relaxation.
- **Test-set-precedes-training (N8)** — sub-wave 7 CP-M6-7-3 refuses training without stratified test set. Strict.
- **Calibration-stage-required (N9)** — sub-wave 8 CP-M6-8-3 refuses plan without calibration stage. Strict; ties to metering/pricing.
- **Character Register leakage-path invariants (N5)** — sub-wave 3 CP-M6-3-2 fires 4 leakage-path RED before register code lands. Strict.

---

## §F · Definition of Done (per-CP · per-sub-wave · per-milestone)

**Per-CP DoD (uniform across all M6 sub-waves):**
1. Grounding-brief-at-CP-open banked at `notes/wave_M6_<sub-wave>_grounding_brief.md` (or extend this brief with `## §CP-M6-N-M` section).
2. Verbatim canon quote in gating test docstring (Condition 1 §A of `STATE/NEXT.md`).
3. Mechanical RED drill receipt banked at `phase0/drill_receipts/<yyyymmddThhmmssZ>_wave_M6_<sub-wave>_cp<N-M>_RED_pre_impl.log` (right-reason failures on new-truth invariants BEFORE any implementation code lands).
4. Mechanism lands on `programme/track-a`; ratchet floor bumps in tandem with `passed_floor` in `baseline_failures.json` + `ratchet_history` entry.
5. Double-green `BASELINE_GUARD=1 python -m pytest tests/invariants/` — Run 1 + Run 2 byte-identical tally.
6. Two commits: (a) code commit on `programme/track-a`, (b) state commit on `master`.
7. `phase0/output_verified_seals/<sub-wave-id>_cp<N-M>.seal.txt` writes with `Kind: audio_plane_cp` payload.

**Per-sub-wave DoD:**
- All CPs sealed (per-CP DoD above satisfied).
- Wave-close composite seal at `phase0/output_verified_seals/<sub-wave-id>.seal.txt` with `Kind: audio_plane_sub_wave_close`.
- Wave rider 1 banked (pip freeze + pytest --collect-only counts).
- Sub-wave-close report at `notes/W_M6_<sub-wave>_close.md` in END-OF-WAVE format (SO §2).

**M6 milestone-close DoD:**
- All 10 core sub-waves sealed (P2 is DEFERRED BY DESIGN this milestone).
- Milestone-boundary report at `notes/M6_close.md` in END-OF-WAVE format carrying:
  - Ratchet trail across all 10 sub-waves.
  - Owner-desk items outstanding (per `notes/MILESTONE_PROMISE_BINDING_20260915_delta_M6M7M8_ratified.md` §Δ6).
  - What's newly unblocked for M7 (10-plane platform composition).
- M5-LIFTING deferral status (W-TRUST-SURFACE-v2 · W-EXECUTIVE-SUITE-v2-LIFT) surfaced for owner-override availability.

---

## §G · Commit protocol

**Per-CP (two commits):**
1. `programme/track-a` (Extraction-Akki HEAD advances) — CP commit message: `W-M6-<SUB-WAVE-ID> · CP-M6-<N-M> · <verbatim canon anchor summary> · ratchet <prev> -> <curr> (+<delta>)`.
2. `master` (assessment_workspace HEAD advances) — state commit message: `state: W-M6-<SUB-WAVE-ID> CP-M6-<N-M> close · <one-line summary> · ratchet <prev> -> <curr> · track-a <sha7> · 3 drill receipts banked · master-only state commit · no push`.

**NEVER push** (Owner Clarification 1 · 2026-08-14 · unchanged).

**Terminal pytest only** (owner ruling 2026-08-26 · unchanged). `testing_agent` and every other test-orchestrating subagent BANNED.

---

## §H · Egress protocol

M6 sub-waves are code-and-state work; most CPs are non-egress (contract/schema/invariant landing). Any CP that requires egress (e.g., CP-M6-10-2 full-training-run dispatch to GPU hosts) MUST respect the 08:00–02:00 UTC egress window. Closed-window CPs proceed with non-egress work (contract landing · invariant authoring · state documentation).

Position-redaction hard-lock preserved throughout (no credentials · no host-IPs · no PII in receipts/logs/notes/commit-messages).

---

## §I · When done · these promises hold

- **Audio-Plane v1.0 in full** — every §1..§14 clause discharged (verbatim canon anchors closed).
- **N1..N10 NOT-YET-IN-SCOPE items** — all absorbed per §15 assignment map (see §Δ2 in successor binding note).
- **Promise #12 audio extension** — Mtafiti census + Audio-Plane share the same platform spine (composes with M7 W1 platform generalisation for full 10-plane platform lift).
- **D7 · D10 · D11 drift-items** — closed at ratification-time via pluggable seam.
- **Canon-1 §4.6 audio modality** — fully instantiated.

---

## §END

M6 is FORMAL. Grounding brief authored. Autonomous execution armed. Wave opens per owner-authored sequencing: **AFTER M5 completion + M8 quick hardening**. No ack gate at open; sub-wave charters open per this brief.

Next hard action: Item-3 census run at 08:00 UTC egress re-open (M5 completion path · not M6 open).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
