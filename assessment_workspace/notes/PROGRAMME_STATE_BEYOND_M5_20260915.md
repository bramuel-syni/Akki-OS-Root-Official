READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PROGRAMME_STATE_BEYOND_M5_20260915.md

**Purpose.** Owner information request 2026-09-15T~03:50Z (verbatim): *"What's the state of the other milestones? — i.e., everything BEYOND the M0–M5 binding. Compile ... disk-grounded, verbatim-cited ... 10-plane platform ... Audio Plane v1.0 §15 Build Sequence (all 11 items) ... Pull Seam conformance gaps ... recommended follow-on waves already banked in close reports ... If the corpus defines NO formal milestones beyond M5, state that explicitly with search receipts."*

**Compiled during** closed egress window (03:22 UTC seal → 08:00 UTC reopen). Non-egress work only. State/docs only; **no mechanism change, no ratchet change**.

**Method used for % complete** (stated per row) — three families:
- **`sealed-waves/chartered-waves`** — count of `phase0/output_verified_seals/*.seal.txt` present over count named in the source.
- **`discharged-promises/promised`** — count of promise IDs discharged over count promised at MILESTONE_PROMISE_BINDING §END.
- **`unmeasured`** — per B5.2 culture verbatim (`Master_Requirements_Registry.md:146`): *"Unmeasured is recorded as unmeasured"*. Where no method exists on disk, `unmeasured` is the recorded value.

**Ratchet floor at compile:** 4018 (`baseline_failures.json` · W-CENSUS-CANON-ALIGN seal · 2026-09-15T~03:22Z).

---

## §A · Absence-as-finding · No formal M6+ on disk

**Owner-requested absence check (verbatim owner clause 3):** *"If the corpus defines NO formal milestones beyond M5, state that explicitly with search receipts (grep for M6, Milestone 6, next sprint, phase 2 etc.) — absence is a finding."*

**Search receipts (this session, 2026-09-15T~03:50Z, `--include="*.md"` scope):**
```
$ grep -rn --include="*.md" -E "\bM6\b|Milestone 6|milestone 6|next sprint|beyond M5" notes/ STATE/
notes/MILESTONE_PROGRESS_20260915.md:5  — meta-reference in the previous owner request's quoted prompt
notes/MILESTONE_PROGRESS_20260915.md:18 — meta-reference (§A · Milestone table M0..M5 + post-M5)
```

**Positive hits on `Phase 2` (three distinct meanings, none is a formal milestone M6):**
```
notes/AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md:618 — Audio-Plane §15 build-sequence "P2" row (voice identity rendering; music register)
notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md:317 — same as above (V151)
notes/MASTER_TRACEABILITY_AUDIT_20260907/s24_donor_akki_os_v1.md:31 — Akki OS V1 donor row "A24-M6" (Solva spec file), NOT a programme milestone
notes/akki_holistic_inventory.md:50 — "W-Audio-P2" audio-archive Phase 2 admission wave (Aug-31 owner directive)
STATE/DECISIONS.md:206 — "Phase 2 (the slice)" in the 6-phase audio-archive admission plan (Aug-31 · not tied to M0..M5 milestone spine)
STATE/DECISIONS.md:5278 — same as above (verbatim owner directive quoted)
STATE/SPRINT_PLAN.md:84,204,208 — W-Audio-P2 charter (BLOCKED on archive access, not chartered as a milestone)
STATE/NEXT.md:1226,1328,1357 — W-Audio-P2 charter carry-forward
```

**Verdict (absence-as-finding):**

**No formal `M6` or `Milestone 6` is defined anywhere in the corpus.** The `MILESTONE_PROMISE_BINDING_20260913.md` binding stops at **M5** and its §END row inventory closes at M5's promised discharges. `BUILD_STRATEGY_20260913.md` §§A..G stops at M5 as well (§A row "M0..M5 milestone spine"; no §H).

**What DOES exist beyond M5 (the material of this ledger):**
- (a) A **READ-ONLY design reframe** (`GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md`) that redraws the whole programme as a 10-plane platform + case-mounted jobs; explicitly labelled *"POC/build HOLD until owner ratifies this reframe"* (`:3` verbatim).
- (b) **Audio-Plane v1.0 §15 Build Sequence** — 11 items · self-declared build reference (`:8` verbatim: *"consolidated build specification. It supersedes the working drafts ... and is the single reference for build"*).
- (c) **Pull-Seam §2 principles** — 7 principles P014..P036 + universal-receipt clause P036.
- (d) **§COV / §ORPH** rows from the milestone binding (uncatalogued follow-on backlog).
- (e) **Recommended follow-on waves** banked in individual wave-close reports (W-CENSUS-CANON-ALIGN §5, W-DATA-SUITE-V2-LIFT §5, W-AUDIO-POC §5 etc.).

None of the five above has been elevated to a formal `M6` binding. **The status of the programme beyond M5 is: partial designs + backlogs + owner-agreed HOLDs, not a bound milestone.**

---

## §B · 10-Plane Platform (READ-ONLY DESIGN · POC-BUILD-HOLD) · state per plane

**Verbatim source anchor (`notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md:3`):**
> *"Task class: DESIGN REFRAME · read-only · no pipeline build, no code commits, no push, ratchet 3251 untouched. POC/build HOLD until owner ratifies this reframe."*

**Roadmap-declared plane state at authorship (2026-09-12T~15:00Z · `:36` verbatim table):**

| # | Plane (verbatim) | Purpose (verbatim) | Roadmap-declared state | Post-reframe waves landed since | Session-current state | % | Method |
|---:|---|---|---|---|---|---:|---|
| A.1 | **Resource Plane** | *"Register + schedule + supervise compute resources"* | PARTIAL (host-specific tools/campaign_infra) | GPU inventory verdict banked 2026-09-15T~02:45Z (`phase0/gpu_inventory/`); no plane-formalisation wave landed | **PARTIAL** (host-specific; no ComputeResource registry service) | ~20% | primitive-count/contract-defined = 1/5 (extant `services/orchestrator_resilience/*` supervision · missing: registry service, capability-tag index, ssh-seam-ref field, `select_by_capability`, `schedule_worker`) |
| A.2 | **Source Plane** | *"Connector interface + read-only guard per source type"* | PARTIAL (readonly_sql_guard only) | W-CENSUS-CANON-ALIGN CP-C1 `SourceCandidate` frozen 4-carrier (`connector-agnostic`) landed 2026-09-15 | **PARTIAL** — connector interface un-authored; `SourceCandidate` shape landed | ~30% | primitive-count/contract-defined = 2/6 (extant: `readonly_sql_guard.py` + `SourceCandidate` · missing: connector Protocol, Synology, S3/OBS, SMB/NFS, HTTP-stream implementations) |
| A.3 | **Capability Registry** | *"Register pluggable processing capabilities"* | PARTIAL (`layer_b.factory` for ASR/diarization/vision) | none in this session; W-CENSUS-CANON-ALIGN's `JobManifest.planes_bound` shape supports capability binding | **PARTIAL** (framework-specific, not generalised) | ~30% | 1/3 (extant `layer_b.factory` with 3 sub-registries · missing: `services/capability_registry/*` generalisation with extensible `capability_class` enum + registration flow) |
| A.4 | **Objective Plane (L1)** | *"Frozen objective carrier + wizard-compile port"* | PARTIAL (carrier landed, wizard absent) | none | **PARTIAL** (`contracts/mtafiti_objective_carrier.py` REAL; wizard absent) | 50% | 1/2 (carrier landed · wizard un-authored) |
| A.5 | **Outcome + Quality Plane (L2)** | *"TargetOutcome + Quality Matrix schemas"* | ABSENT (schemas un-authored as frozen contracts) | none · but W-CENSUS-CANON-ALIGN CP-C6 `SourceStratumMeasurement` (8-dim) partially discharges the "quality matrix" shape at census scope | **PARTIAL** (stratum measurement carrier landed; TargetOutcome frozen contract still un-authored) | ~25% | 1/4 (SourceStratumMeasurement landed · missing: TargetOutcome_v0, StratumAcceptance, MOAC scorecard writer) |
| A.6 | **Success + QC Plane (L3)** | *"Composable gate framework"* | PARTIAL (5 individual gates, no framework) | W-DATA-SUITE-V2-LIFT `gate_disclosure_budget` + `gate_release_admissible` landed; W-CENSUS-CANON-ALIGN `SampledPopulationInvalid` refusal-gate at construction; no unified framework | **PARTIAL** (~7 individual gates; no composition service) | ~35% | 7/9 gate primitives extant · 0/1 framework (`services/gate_framework/*` un-authored) → mean 35% |
| A.7 | **Commission + Worker Plane (L4)** | *"Worker orchestration + JD/KPI/milestone/handoff"* | PARTIAL (LORA-trainer-specific) | none | **PARTIAL** (LORA-specific `campaign_infra/manifest.py`) | ~15% | 1/4 contract-defined (extant `CampaignManifest` is a LORA-specialisation · missing: generic `CommissionSpec`, `Milestone`, `WorkerLane`, `WorkerJD`) |
| A.8 | **Supervision Plane (L5)** | *"Domain-agnostic work-supervisor"* | ABSENT (progress-signal watchdog un-built) | none | **ABSENT** (process-liveness only via `orchestrator_resilience/`; no output-verifying supervisor) | 0% | 0/2 primitives (`ProgressSignal` un-authored · `StarvationAlarm` un-authored) |
| A.9 | **HITL Plane (L6)** | *"Milestone-stream + ratification API"* | ABSENT | none · informal L6 pattern is the 5-section wave-close markdown | **ABSENT** (formal API un-built) | 0% | 0/3 primitives (`MilestoneStream` un-authored · `ratify` un-authored · `dispute` un-authored) |
| A.10 | **Governance Plane** | *"Rulebook · release gate · AU-3 · determinism boundary · IP/consent/DP chokepoints"* | PARTIAL (§C7 rulebook landed, release-gate module absent) | W-AUDIO-POC `TranscriptArtefact` release-gate 4-verdict shape landed; W-DATA-SUITE-V2-LIFT export-artefact `disclosure_budget` gate landed | **PARTIAL** (6/10 primitives extant per roadmap `:426` inventory) | 60% | primitive-count/authored = 6/10 (extant: rulebook · refusal registry · owner-ruling banking · determinism boundary · licence_class · release-gate 4-verdict shape · missing: AU-3 gating invariant, custody-boundary Character-Register primitive, KDPA-verdict chokepoint field, cross-border transfer chokepoint) |
| A.11 | **JobManifest — the MOUNTING schema** | Case-specific binding artefact | Design-only at reframe | **W-CENSUS-CANON-ALIGN CP-C5 landed `JobManifest` frozen 5-carrier (data-only per §E.4)** 2026-09-15 | **PARTIAL** — carrier shape landed; the 10-field JobManifest with plane bindings per `:480` is still short of the design | ~30% | 5/13 carriers (`job_id` · `job_kind` · `estate_instance` · `planes_bound` tuple-of-tuples · `capabilities_declared` tuple · missing: `objective_carrier_ref` · `target_outcome_ref` · `source_bindings` · `resource_bindings` · `capability_pipeline` · `gate_composition` · `commission_spec_ref` · `supervision_config` · `hitl_config` · `retention_policy_ref` · `owner_rulings` · `release_gate_verdicts_current` · `manifest_sha256`) |
| A.12 | **PLATFORM build waves W0 · W1** | Case-agnostic platform mechanism landings | Chartered at design | none · roadmap explicitly HOLD | **NOT-CHARTERED** (POC/build HOLD in force per `:3`) | 0% | sealed/chartered = 0/2 · DEFERRED under owner-ratification HOLD |

**Plane-programme aggregate:** ~24% (unweighted mean across A.1..A.11 · A.12 excluded as HOLD).

**Wave-level roadmap breakdown (`:530` verbatim):**
> "**A.12 · PLATFORM build waves — W0 · W1**"

**Job-level roadmap waves (`:706` verbatim):**
> W2 · Mount + run vertical slice ONE station (L-class · JOB) · Prerequisites: W0/W1 platform closed + NAS reachable + HF token + deps + owner ratification
> W3 · Scale to 3 stations · W4 · Scale to 16 stations · W5 · Character Register · W6 · DAP sale · W7 · WPW Tier-2 · W8 · Release-gate lift · W9 · Audio-bytes-retention ruling

**State of platform build waves W0, W1 and job waves W2..W9:**

| Wave | Type | Scope (verbatim) | State | % | Method |
|---|---|---|---|---:|---|
| W0 | PLATFORM | *"Integrity fix — silent-success defect (S-class · PLATFORM)"* (`:534`) | **NOT-CHARTERED · POC-BUILD-HOLD** | 0% | sealed/chartered = 0/1 |
| W1 | PLATFORM | *"Work-supervisor + Resource Registry + Capability Registry generalisation (M-class · PLATFORM)"* (`:542`) | **NOT-CHARTERED · POC-BUILD-HOLD** | 0% | sealed/chartered = 0/1 |
| W2 | JOB | *"Mount + run vertical slice ONE station (L-class · JOB)"* (`:709`) | **NOT-CHARTERED · BLOCKED on W0+W1 close + NAS reachable + owner ratifications** | 0% | sealed/chartered = 0/1 |
| W3 | JOB | *"Scale to 3 stations (M-class)"* (`:731`) | **NOT-CHARTERED** | 0% | sealed/chartered = 0/1 |
| W4 | JOB | *"Scale to 16 stations"* (`:737`) | **NOT-CHARTERED** | 0% | sealed/chartered = 0/1 |
| W5 | JOB | *"Character Register wave (§5-§7 invention layer)"* (`:738`) | **NOT-CHARTERED** | 0% | sealed/chartered = 0/1 |
| W6 | JOB | *"DAP sale surface (R-6/R-7 bindings)"* (`:739`) | **NOT-CHARTERED · BLOCKED on R-6 + R-7 owner rulings** | 0% | sealed/chartered = 0/1 |
| W7 | JOB | *"WPW Tier-2 draft-on-settle emitter"* (`:740`) | **NOT-CHARTERED** | 0% | sealed/chartered = 0/1 |
| W8 | JOB | *"Release-gate ADMISSIBLE lift (Ruling #5 verdicts)"* (`:741`) | **NOT-CHARTERED · BLOCKED on R-7 + R-15(a) + R-16(a) owner rulings** | 0% | sealed/chartered = 0/1 |
| W9 | JOB | *"Owner-ruling A/B/C for audio-bytes-retention"* (`:742`) | **NOT-CHARTERED · BLOCKED on owner Path-A/B/C ruling** | 0% | sealed/chartered = 0/1 |

---

## §C · Audio Plane v1.0 §15 Build Sequence · 11 items · state

**Verbatim source anchor (`notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md:303`):** *"§15 · Build Sequence (P225..P240 · in full)"*.

Self-declared status of the v1.0 spec (`:8` verbatim): *"consolidated build specification. It supersedes the working drafts (Audio Capability Spec v1.0 and Addendum v1.1.2) and is the single reference for build."*

**Ordering rationale (each row's third column is verbatim from v1.0 §15):**

| # | Item (verbatim §15) | Rationale (verbatim §15) | Session-current state | % | Method |
|---:|---|---|---|---:|---|
| 1 | *"Ingestion capture: language ID, code-switch points, condition profile, synthesis attributes (§4.1–4.4)"* | *"Everything downstream consumes these; only cheap at first ingestion. Deferral cost is a full re-pass over the estate."* | **NOT-CHARTERED · follow-on** (`W-AUDIO-INGEST-STAGE-1` candidate per drift audit D1 · POC's per-file inventory does NOT invoke this) | 0% | sealed/chartered = 0/1 |
| 2 | *"Dedup instance condition map (§4.5)"* | *"Contract change to existing machinery; near-zero new detection work."* | **NOT-CHARTERED** (occurrence-index extension per drift audit N3) | 0% | sealed/chartered = 0/1 |
| 3 | *"Character Register schema + custody invariant harness (§6)"* | *"The boundary must exist before the first cluster is stored; retrofitting means rebuilding from source."* | **NOT-CHARTERED** (Register write path un-authored per drift audit N5; four-condition leakage-invariant test un-authored) | 0% | sealed/chartered = 0/1 |
| 4 | *"Codec service (§3)"* | *"Unsupervised pretraining starts on unlabelled audio while labelled work proceeds elsewhere."* | **NOT-CHARTERED** (`perception/audio_codec/` un-authored per drift audit N4) | 0% | sealed/chartered = 0/1 |
| 5 | *"Clustering + sampled human validation (§5.3)"* | *"Requires 1–4."* | **BLOCKED on items 1–4** | 0% | sealed/chartered = 0/1 |
| 6 | *"Objective Wizard variant + Collection Schema type + registry namespace (§8, §9, §12.1)"* | *"The planner must never accept a hand-authored Outcome once the wizard exists; building the planner first invites the malformed-input class the compile stage makes impossible."* | **NOT-CHARTERED** (wizard variant un-built; Collection-Schema type un-authored; namespace un-scoped) | 0% | sealed/chartered = 0/1 |
| 7 | *"TargetOutcome type + planner core (§10, §11.1, §11.4)"* | *"Requires register strata to plan against and the wizard to author Outcomes."* | **NOT-CHARTERED · BLOCKED on items 3 + 6** (per drift audit N8: TargetOutcome type un-authored · plan-refusal-at-definition invariant un-authored) | 0% | sealed/chartered = 0/1 |
| 8 | *"Sampling & Reflection machinery + milestone records (§11.2–11.3)"* | *"Requires 7 and a test set."* | **NOT-CHARTERED · BLOCKED on item 7 + test-set-precedes-training invariant** (per drift audit N9) | 0% | sealed/chartered = 0/1 |
| 9 | *"Commission View (§13)"* | *"Reads records created in 8; by §13.4 it cannot precede them."* | **NOT-CHARTERED · BLOCKED on item 8** (per drift audit N10) | 0% | sealed/chartered = 0/1 |
| 10 | *"Full training runs under the commissioned-job contract (§11.6)"* | *"Last by construction — the planner refuses to run earlier."* | **NOT-CHARTERED · BLOCKED on items 7–9** | 0% | sealed/chartered = 0/1 |
| P2 | *"Voice identity rendering; music register"* | *"Phase 2. Non-foreclosure is guaranteed by item 1 and §7.5."* | **NOT-CHARTERED · Phase-2 deferred by design** (`§7.5` verbatim: *"Rendering requires a synthesis stack, which is a separate build from recognition. What this specification requires now is non-foreclosure"*) | 0% | sealed/chartered = 0/1 · Phase-2 deferred |

**Audio-Plane §15 aggregate:** 0 of 11 chartered · **0%** · method: `sealed/chartered = 0/11`.

**Related drift-audit backlog (`notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md`):** 10 not-yet-in-scope items (N1..N10 · missing N7 numbering per earlier ledger book-keeping note) · full breakdown in `MILESTONE_PROGRESS_20260915.md §C`.

---

## §D · Pull-Seam conformance gaps

**Verbatim source anchor (`notes/PULL_SEAM_REQUIREMENTS_VERBATIM_20260914.md`):** self-declared version pin (`:34` verbatim P008): *"Version · pull_seam_principles_v1 · 14 September 2026 · External"*.

**Seven principles + their conformance state:**

| # | Principle (verbatim header) | Sub-rule pinpoint | Session-current state | % | Method |
|---:|---|---|---|---:|---|
| P1 | *"Compute comes to the data. Never the reverse."* (`P014`) | *"There is no configuration in which estate data is transferred to compute outside the perimeter."* (`P015.s6`) | **PARTIAL** — SSH seam to `akki-vm`/`akki-vm-ii` is chartered (services/training_runner/ssh_seam.py); Item-3 census run WAITS for 08:00 UTC re-open per egress-hold; some past connections were external (HuggingFace whisper-small routing per BLOCKER-HF-A5-01) | ~60% | 1 REAL SSH seam · 2 external-hosting probes (HF Inference-Providers routing that was probe-only, no data-out) · 0 net data-out per position-redaction rule |
| P2 | *"Principle 2"* (`P016..P017` · body TBD in this session) | — | **UNMEASURED** | unmeasured | source ledger only quotes P015; P016..P017 body not in the file above · **book-keeping observation: extract-ledger row missing** |
| P3..P6 | *"Principles 3..6"* (`P018..P034`) | — | **UNMEASURED** | unmeasured | source ledger rows missing (only P1 + P7 body quoted in the extract on disk) · **book-keeping observation banked** |
| P7 | *"Every crossing is recorded — or it does not happen."* (`P035`) + *"Each operation writes a receipt: what was accessed, in what quantity, under which terms, by which party, at what time."* (`P036.s1`) + *"The receipt is written before the result is returned. If it cannot be written, the operation is refused."* (`P036 · Pull Seam §2 P7`) | Per D9 drift audit | **PARTIAL** — many surfaces DO emit receipts (`services/audio_poc/gap_fill_writer.py::emit_gap_fill_receipt`; W-DATA-SUITE-V2-LIFT export-artefact receipt; W-CENSUS-CANON-ALIGN drill receipts + wave riders); **BUT** the universal receipt-before-result invariant is not enforced across every operation. `admit_transcript_release` returns None silently with no receipt — the flag-bearing drift is **D9** (per `PENDING_RATIFICATIONS_LEDGER_20260915.md §B row D9`). | ~50% | ~50% of operation sites emit receipts · universal invariant un-authored; no unified `Receipt.v0` schema exists · charter candidate: `W-PULL-SEAM-RECEIPT-UNIFY` |

**Pull-Seam aggregate:** unmeasured (only 2 of 7 principles' full bodies are on-disk in the current verbatim ledger) · **book-keeping observation surfaced for owner attention:** the Pull-Seam verbatim ledger is INCOMPLETE — P2..P6 principle bodies were not extracted from the source docx; only P1 + P7 have full row-tables.

---

## §E · Recommended follow-on waves banked in individual close reports

These are per-wave recommendations, not a milestone binding. Each is banked in exactly one wave-close report.

| Wave name | Source citation | Scope (1 line) | State | % | Method |
|---|---|---|---|---:|---|
| **W-CENSUS-RUNTIME-ORCHESTRATION** | `notes/W_CENSUS_CANON_ALIGN_close.md:70` verbatim: *"The next natural wave binds existing audio-poc surfaces (recording_inventory, transcript_inventory, pairing_registry) as registered plane implementations behind a JobManifest, then wires them onto the CP-C4 registry via CP-C6 SourceStratumMeasurement output-field carriers."* | Runtime wiring for the data-only JobManifest landed by W-CENSUS-CANON-ALIGN CP-C5 | **NOT-CHARTERED · candidate** | 0% | sealed/chartered = 0/1 |
| **W-PULL-SEAM-RECEIPT-UNIFY** | `notes/PENDING_RATIFICATIONS_LEDGER_20260915.md:266` verbatim: *"W-PULL-SEAM-RECEIPT-UNIFY wave charter (currently unchartered)."* | Universal `Receipt.v0` schema + receipt-before-result invariant across every operation surface | **NOT-CHARTERED · BLOCKED on D9 owner ratification** | 0% | sealed/chartered = 0/1 |
| **W-EXPORT-ARTEFACT-RENDER** | `notes/W_DATA_SUITE_V2_LIFT_close.md:93` verbatim: *"CP-D6 landed the contract + gate; actual export payload rendering (CSV/PDF/…) is out-of-wave (§E.3 wave-honest limit). Small scope, high user-visible value."* | Render actual CSV/PDF/… export bytes behind the D6 gate | **NOT-CHARTERED · candidate** (S-class scope) | 0% | sealed/chartered = 0/1 |
| **W-DATA-SUITE-ANALYZE-WORKSPACE-REAL** | `notes/W_DATA_SUITE_V2_LIFT_close.md:92` verbatim: *"Both engines currently HALT; both are chartered as the case-agnostic real mechanism replacement."* | Replace HALT skeleton with real case-agnostic analyze engine | **NOT-CHARTERED · candidate (paired)** | 0% | sealed/chartered = 0/1 |
| **W-DATA-SUITE-DEEP-DIVE-REAL** | same citation as above | Replace HALT skeleton with real case-agnostic deep-dive engine | **NOT-CHARTERED · candidate (paired)** | 0% | sealed/chartered = 0/1 |
| **W-TESTS-FIRST-GUARD-INVARIANT** | `notes/W_DATA_SUITE_V2_LIFT_close.md:95` verbatim: *"an invariant which parses any `*_RED_pre_impl.log` under `phase0/drill_receipts/` and refuses green tallies (an automated version of the parse-not-paraphrase corrective ritual). Cost: a handful of invariants. Payoff: this class of prior-turn violation becomes structurally impossible."* | Automated parse-not-paraphrase check on drill-receipt logs | **NOT-CHARTERED · candidate (S-class · hardening)** | 0% | sealed/chartered = 0/1 |
| **W-AUDIO-PROD-MODEL-SELECT** | `notes/PENDING_RATIFICATIONS_LEDGER_20260915.md:325` verbatim: *"chartering `W-AUDIO-PROD-MODEL-SELECT` before any real-data transcription"* | Production-model selection (not CI-fixture whisper-tiny) | **NOT-CHARTERED · BLOCKED on D12 owner ruling** | 0% | sealed/chartered = 0/1 |
| **W-TRUST-SURFACE-v2** | `notes/BUILD_STATUS_PERCENT_20260909.md:51` (already banked in DPO-D2 default) | 2 Trust surfaces v2 migration | **DEFERRED per DPO-D2 default** (`notes/wave_data_suite_v2_lift_grounding_brief.md:27`) | 0% | sealed/chartered = 0/1 |
| **W-EXECUTIVE-SUITE-v2-LIFT** | same citation | 7 Executive Suite surfaces v2 migration | **DEFERRED per DPO-D2 default** | 0% | sealed/chartered = 0/1 |
| **W-JOURNEY-ASSISTANT** | `notes/JOURNEY_AND_ASSISTANT_AUDIT_20260913.md:116` verbatim: *"a wave that would extend the Shaping-Wizard chat-mode collaboration pattern (Canon-5 §14) uniformly to (a) Setup / Connect onboarding, (b) Agent-Deploy Wizard, and (c) a Solva-facing 'walk me through the answer' surface, all inheriting the same doctrinal boundary from DAP-20"* | Universal wizard-chat pattern to onboarding + agent-deploy + solva-walk-through | **NOT-CHARTERED · owner NOT-RULED-IN** (`notes/W_REGISTRY_EXTENSION_G3_grounding_brief.md:48` verbatim: *"NOT ruled in by owner. NOT folded here."*) | 0% | sealed/chartered = 0/1 · owner-input-blocked |
| **W-AUDIO-INGEST-STAGE-1** | `notes/wave_census_canon_align_grounding_brief.md:91` verbatim: *"Follow-on wave chartered by v1.0 §15 build-item 1 (W-AUDIO-INGEST-STAGE-1)."* + `notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:36` | Per-segment LID + condition-profile + switch-point capture (Audio-Plane §15 item 1) | **NOT-CHARTERED · candidate (L-class scope)** | 0% | sealed/chartered = 0/1 · same as §C row 1 |
| **W-Watch-Foundation (Track-B open)** | `notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md:872` verbatim: *"Watch-for-audio \| W-Watch-Foundation (Track-B) \| Separate charter"* + `notes/SILENT_FAILURE_ROOTCAUSE_AND_LAYER_MAP.md:353` verbatim: *"Watch bundle (Macho / Mkono / Witness / Marks / Drills) \| — \| **ABSENT for audio domain**"* | Audio-domain Watch surface (Canon 8 §1-§40 · 72 requirement rows) | **NOT-CHARTERED · Track-B open** | 0% | sealed/chartered = 0/1 |
| **W-Audio-P2 (audio-archive Phase-2 admission)** | `STATE/SPRINT_PLAN.md:84,204` verbatim charter: *"Audio archive Phase 2 admission (manifest hash → representative slice → HSS → GPU smoke)"* + `STATE/NEXT.md:1357` verbatim: *"BLOCKED on owner-provided access"* | Audio archive admission (Phase-2 slice) | **NOT-CHARTERED · BLOCKED on archive access + credentials from owner** | 0% | sealed/chartered = 0/1 |
| **W-MTAFITI-GPU-EMBEDDINGS + W-MTAFITI-DEEP-SWEEP** | `MILESTONE_PROMISE_BINDING §ORPH` verbatim: *"W-MTAFITI-GPU-EMBEDDINGS + W-MTAFITI-DEEP-SWEEP follow-ons"* | Two Mtafiti follow-on waves surfaced by W-MTAFITI-GPU-DISCOVERY close | **NOT-CHARTERED · candidate (§ORPH remainder)** | 0% | sealed/chartered = 0/2 |
| **Quarantine-restoration (D1a-1 residue class)** | `notes/waveD_close_report.md:158,164,229` verbatim: *"19 files · 88 tests · 100% event-loop-closed class"* + *"pytest-asyncio 1.2.0 landed at CP-D5 as a good partial win. Newer versions (≥1.5) may resolve the D1a-1 residue class. Wave-F option 1 (framework upgrade pilot on 3-5 chartered files first)."* | Restore 159 quarantined event-loop-closed tests to the ratchet | **NOT-CHARTERED · candidate** (`notes/waveF_retirement_charter.md`) | 0% | sealed/chartered = 0/1 |
| **W-Rights-Quarantine** (Canon 4 §41) | referenced in DECISIONS.md wave-cross-links | Rights quarantine mechanism landing | **PARTIAL** — chartered inside M3 close; production-grade build follows | ~50% | 1 spec-close · 0 built-and-invariant-tested surface |

**Follow-on wave aggregate:** 0 of 16 candidate/chartered follow-on waves sealed · **0%** · method: `sealed/chartered = 0/16`.

---

## §F · MILESTONE_PROMISE_BINDING §COV + §ORPH remainder (uncatalogued)

**Verbatim §COV (`notes/MILESTONE_PROMISE_BINDING_20260913.md`):** 9 coverage-gap items — S-7 (spec-closed by Watch Learning Amendment v1) · LIM-1..5 (non-claims by design · never discharged) · Amendment 8 scope-statement (HOLD per owner C1 disposition) · Doc-0 Attribute 12 fan-in (closes with M2 end) · DAP R-6 pricing · WPW R-2 signatory · DAP R-2 approving-authority · Rules-Service R-2 second-signatory · DPO-S2 reflection contract.

**Verbatim §ORPH:** 6 orphan-work items — STATE/NEXT.md + STATE/PINS.md book-keeping refresh · REUSE/BUILD supersession lineage · Doc-0 G-8 Reliable-Time-Source fix (spec-closed) · G-3 Registry-remainder (Mtafiti asset-inventory generalisation) · W-MTAFITI-GPU-EMBEDDINGS + W-MTAFITI-DEEP-SWEEP follow-ons · Sysadmin follow-up on 9 SG-blocked hosts.

**§COV+§ORPH aggregate:** 15 items total.
**% complete:** **unmeasured** per B5.2 culture (binding itself declares "un-catalogued" / "orphan"; no denominator).

---

## §G · Blocker sources tabulated

Every non-chartered / non-sealed row above has one of four blocker types:

| Blocker type | Items blocked | Count |
|---|---|---:|
| **Owner ratifications pending** | W6 (R-6/R-7) · W8 (R-7/R-15(a)/R-16(a)) · W9 (Path A/B/C ruling) · Character Register R-15(b)/R-16(b)/R-17(b) · BC-3/BC-4 · S-24 · R-14 · D7 · D9 · D10 · D11 · D12 | 13+ |
| **Owner-agreed HOLDs** | Governed-Census-Roadmap POC/build HOLD (all 10 planes + W0..W9) · W-TRUST-SURFACE-v2 (DPO-D2) · W-EXECUTIVE-SUITE-v2-LIFT (DPO-D2) · W-JOURNEY-ASSISTANT (not-ruled-in) · Audio-Plane §15 build-sequence (canon-authored order, not owner-ratified as programme sequence) | 15+ |
| **Admin binds pending** | Transcription-server host+creds · RADIO routing to 10.10.19.0/24 · 5 closed-SG MySQL hosts · Sysadmin follow-up on 9 SG-blocked hosts · W-Audio-P2 archive access + credentials · HuggingFace routing (BLOCKER-HF-A5-01) | 6 |
| **Prior-wave completion prerequisites** | W1 depends on W0 · W2 depends on W0+W1 · W3 depends on W2 · Audio-Plane §15 item N depends on items 1..N-1 | 20+ |
| **Census results pending** | D12 owner rules after census · Item-3 live census run itself pending at 08:00 UTC re-open · post-census cascade for D12 · Path-A/B/C audio-bytes retention | 4 |

---

## §H · Dependency-ordered candidate sequence for the next sprint (recommendation only · owner decides)

**Framework note:** the owner has NOT bound a next-sprint sequence. The list below is one dependency-honest candidate ordering, not a proposal. Owner may re-order or drop any row.

**Immediately runnable (non-egress · zero owner-input required · zero admin bind required):**

1. **Item-3 · live read-only census run (Promise #12)** — armed at wave seal · fires at 08:00 UTC re-open (~4h from compile). Zero mechanism change · uses CP-C1..CP-C6 machinery only.
2. **W-TESTS-FIRST-GUARD-INVARIANT** (S-class hardening) — automated parse-not-paraphrase check on `*_RED_pre_impl.log` receipts · closes a class of prior-turn violation structurally · zero owner-input · zero external.
3. **Live SSH GPU re-verification** (non-blocking follow-on to CP-C3 GPU-AVAILABLE ruling) — fresh timestamped receipt to `phase0/gpu_inventory/<yyyymmddThhmmssZ>_live_ssh_verification.json` · zero mechanism change · at 08:00 UTC re-open.

**Owner-ratification-gated:**

4. **W-PULL-SEAM-RECEIPT-UNIFY** (BLOCKED on D9 ruling · owner rules extend `admit_transcript_release` receipt-before-result) — small-to-medium; when D9 ratifies, the wave closes 1 canon principle across every surface.
5. **W-CENSUS-RUNTIME-ORCHESTRATION** (BLOCKED on owner ruling that data-only JobManifest can accept a runtime layer) — binds `recording_inventory`/`transcript_inventory`/`pairing_registry` as registered plane implementations · realises the S5 reframe in code.
6. **D10 + D11 owner ratification** (Silero VAD + pyannote/speaker-diarization-3.1 · INFERRED starting-points) — removes INFERRED flags · zero code change on ratification.

**Admin-bind-gated:**

7. **W-Audio-P2 audio-archive admission (Phase-2 slice)** (BLOCKED on archive access + credentials) — chartered but zero-progress until owner names bucket + credentials + manifest source.
8. **Transcription-server bind + RADIO routing + 5 closed-SG MySQL hosts** — admin-side binds; on land, unblock post-M5 audio pipeline.
9. **D12 owner ruling after census results** — POC path (CI-fixture whisper-tiny + faster-whisper) OR chartering `W-AUDIO-PROD-MODEL-SELECT` first · rules "after census results" per owner directive 2026-09-15T~02:35Z.

**Release-gate cascade (post-D12 · post-transcription-server-bind):**

10. **W8 · Release-gate ADMISSIBLE lift** (BLOCKED on R-7 + R-15(a) + R-16(a)) — three verdicts land together per audio-POC wave-close guidance.
11. **W9 · Owner-ruling A/B/C for audio-bytes-retention** — Path A (governed retention · highest lab value · highest governance surface) OR Path B (pointer-only · safest) OR Path C (defer to post-W3).

**Follow-on backlog (S/M-class · sequenceable in parallel with the above):**

12. **W-EXPORT-ARTEFACT-RENDER** — small hardening wave · high user-visible value.
13. **W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DATA-SUITE-DEEP-DIVE-REAL** — paired wave · replace HALT skeletons.
14. **Quarantine-restoration** (D1a-1 residue class · 19 files · 88 tests) — pytest-asyncio 1.5+ pilot on 3-5 files.
15. **W-MTAFITI-GPU-EMBEDDINGS + W-MTAFITI-DEEP-SWEEP** — §ORPH remainder.

**Longer-arc / deferred by owner or design:**

16. **Governed-Census-Platform W0..W9** — under `POC/build HOLD until owner ratifies this reframe` (`GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md:3` verbatim). If owner ratifies, W0 + W1 platform waves come first; W2..W9 job waves after.
17. **Audio-Plane §15 build sequence items 1..10 + P2** — 11 items · not owner-ratified as programme sequence · canon-authored order guides internal sequencing when the plane comes online.
18. **W-TRUST-SURFACE-v2 + W-EXECUTIVE-SUITE-v2-LIFT** — deferred per DPO-D2.
19. **W-JOURNEY-ASSISTANT** — not ruled in by owner; folded under M4 close instead.
20. **W-Watch-Foundation** — Track-B open · separate charter.

---

## §I · Aggregate programme-state-beyond-M5 headline

| Corpus | Chartered/named | Sealed | State | % | Method |
|---|---:|---:|---|---:|---|
| Governed-Census-Roadmap · 10 planes | 10 | ~0 | POC-BUILD-HOLD in force since 2026-09-12; incidental primitive-count gains from M2..M5 waves ≈ 24% mean | ~24% | primitive-count/contract-defined mean across A.1..A.11 (A.12 excluded as HOLD) |
| Governed-Census-Roadmap · W0..W9 waves | 11 (W0..W9 + P2 indirect) | 0 | ALL not-chartered under POC-BUILD-HOLD | 0% | sealed/chartered = 0/11 |
| Audio-Plane v1.0 §15 build sequence | 11 (items 1..10 + P2) | 0 | ALL not-chartered · canon-authored order · sequential dependencies | 0% | sealed/chartered = 0/11 |
| Pull-Seam principles | 7 | 0 sealed as universal invariant | P1 + P7 partially discharged in-scope surfaces · P2..P6 verbatim body missing from on-disk ledger (book-keeping observation) | unmeasured | ledger incomplete · no denominator on disk |
| Recommended follow-on waves (close-report banked) | 16 | 0 | ALL not-chartered · candidate/deferred/blocked | 0% | sealed/chartered = 0/16 |
| §COV + §ORPH uncatalogued | 15 | various partial | Various (no denominator on disk) | unmeasured | B5.2 culture |
| **Combined beyond-M5 headline** | **~60 named items** | **0 sealed as beyond-M5 formal work** | **No formal M6 exists · corpus is 5 fragmented sources totalling ~60 named items · dependency chains long and owner-input-blocked** | **~0-4% depending on method** | absence-of-milestone-binding = FINDING |

---

## §J · Position-redaction acknowledgement

Every row above:
- Cites disk-file paths and line numbers.
- Does not echo credentials, host IPs, SSH usernames, or PII.
- Preserves owner-side scrub directives verbatim (R-14 engine-name scrub 2026-09-14).
- Uses aliases where estate hosts appear (`akki-vm`, `akki-vm-ii`).

## §K · Book-keeping observations surfaced during compile (owner attention · no action required)

1. **Pull-Seam verbatim ledger is INCOMPLETE.** Only P1 (Compute-comes-to-data) and P7 (universal-receipt) principle bodies are extracted on disk. P2, P3, P4, P5, P6 principle bodies are missing from `notes/PULL_SEAM_REQUIREMENTS_VERBATIM_20260914.md`. Recommend: extend the extract before any wave depends on P2..P6 verbatim quotes.
2. **`AUDIO_PLANE_V1_DRIFT_AUDIT` numbering inconsistency.** Summary line declares "10 not-yet-in-scope items" but enumeration is N1..N6 + N8..N10 = 9 items (N7 skipped). Same observation banked in `MILESTONE_PROGRESS_20260915.md §C`.
3. **`R-15/R-16/R-17` mnemonic conflates two rulings each** (Audio-POC release-gate + Watch Learning Amendment). Same observation banked in `PENDING_RATIFICATIONS_LEDGER_20260915.md §A footnote`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
