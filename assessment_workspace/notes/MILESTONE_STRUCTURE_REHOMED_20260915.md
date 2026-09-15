READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# MILESTONE_STRUCTURE_REHOMED_20260915.md

**Purpose.** Owner correction 2026-09-15T~04:05Z (verbatim): *"Now can you surface the milestones as we had mapped them. You seem to have jumbled up things, all work need to exist within the milestone structure."*

**Compiled during** closed egress window (03:22 UTC seal → 08:00 UTC reopen). Non-egress work only. State/docs only; **no mechanism change, no ratchet change**.

**Method.** Every item that has been surfaced free-floating in recent work (waves / backlogs / candidates / ratifications / drift-items / DPO defers / §COV / §ORPH) is placed inside the owner-bound milestone structure below. Zero orphans by construction. Where the M0..M5 spine has no home, a PROPOSED post-M5 milestone is offered — marked **PROPOSED** and NOT self-ratified; owner ratifies before it becomes binding.

---

## §A · Authoritative milestone map on disk

**Base binding (canonical):** `notes/MILESTONE_PROMISE_BINDING_20260913.md` (522 lines · dated 2026-09-13 · owner-ratified · ratchet-agnostic document lane).
**Amending delta:** `notes/MILESTONE_PROMISE_BINDING_20260913_delta_watch_learning.md` (88 lines · owner constraint 2026-09-13 verbatim: *"do NOT alter the plan; do NOT create new waves; do NOT resequence"* — new requirements ride EXISTING wave homes).

**Structural summary (verbatim `§END` row inventory · line 494):**

| Milestone | Name (verbatim §M* header) | Discharges (§END verbatim) |
|---|---|---|
| **M0** | Canon-delta extractions + supersession of Aug-14 REUSE / BUILD_STRATEGY | 0 canon promises · discharges SO §2 engagement discipline + Canon-1 §4.11 doctrine |
| **M1** | W-DAP-STACK · DAP-1..DAP-30 (admission · trust · crossing · approval · metering) | DAP-A1..A9 (full); A10 (partial); DAP-33/34/35 (partial); Promise #4 partial; Promise #22, #25 (consumed); doctrines §4.1, §4.9, §4.11 |
| **M2** | Rules-Service mechanism + 6 remaining Doc-0 attribute waves | Doc-0 Attr 1..12; Rules-Service ceremony R-1/R-3/R-4; Promise #22 (fully), #27, #29; Amendments 6, 7; doctrines §4.10, §4.11 |
| **M3** | Watch (Doc-03 62 BUILD rows) + Registry CP10 DOM proof + Pruning + Agent-Containment | Watch composite #6 + S-1..S-21 + S-24 + S-26 + S-27 (Voice) + S-28/S-29 (Watch-Learning) + AC-1..AC-14 + AC-15..AC-18 + RBM-20 + RBM-23 + CP10; doctrine §4.1 |
| **M4** | Assistant surfaces (Shaping Wizard · Connect Wizard · DAP-20 boundary · Journey handoff) | Promise #32; Canon-5 §14; Canon-6 §3/§6/§12; DAP-20 boundary verified; doctrine §4.6 |
| **M5** | Data-Suite-v2 (donor lift) + Audio-POC (build) | DAP-A10 (remainder); Promise #12 (fully); Audio-Plane §1.2; doctrine §4.6 |

**PROPOSED post-M5** (below · not self-ratified · owner ratifies): M6 · Audio-Plane v1.0 production build · M7 · Governed Census/Harvest Platform · M8 · Post-launch hardening + §COV/§ORPH catch-all.

---

## §B · Delta note · original owner mapping vs 2026-09-13 binding

**Earlier structure on disk (pre-2026-09-13):** `STATE/SPRINT_PLAN.md` (327 lines · dated 2026-08-31 · last updated 2026-09-06T~14:35Z). Uses **priority tracks P1..P6** derived from wave-honest-limits after W-Shield-Train-run and W-Multi-Table-Extract closes; also enumerates named waves W-Shield-Train / W-Audio-P2 / W-WPW-v1 / W-TxtTrain-v2 / W-Orchestrator-Resilience-r1 / Reuse-audit. **NOT organized around milestone IDs M0..M5.** Owner picked sequencing per prompt.

**Structure transition:** The M0..M5 milestone spine was introduced 2026-09-13 via `MILESTONE_PROMISE_BINDING_20260913.md` §CONFIRM section which explicitly reconciles against the "owner-proposed BUILD/LIFT/KEEP shape" and applies corrections. The binding self-declares (`:32` verbatim): *"Standing. ROLE OVERRIDE · Phase-1 Canon Assessment · NO production code · NO scaffolding touched · local commit only, NEVER push · NO egress · HALT after delivery."* The 2026-09-13 binding is the OWNER-RATIFIED spine the programme has operated under since.

**No drift found between owner's original mapping and current binding for M1..M5 scope.** Owner's SPRINT_PLAN.md items map cleanly into M-spine:

| SPRINT_PLAN.md item | 2026-09-13 spine home | Status |
|---|---|---|
| W-Shield-Train (a..g) | M5-adjacent (pre-M5 · closed 2026-09-06) | ✅ CLOSED (ratchet 2024→2924 across a..g runs) |
| W-Multi-Table-Extract | M5-adjacent (pre-M5) | ✅ CLOSED (ratchet 2924→2954) |
| W-G5c-close + W-G5c-COMPUTE-v2 | M5-adjacent (pre-M5) | ✅ CLOSED (ratchet 2680→2703) |
| W-WPW-v1 (a..d) | M5-adjacent (pre-M5) | ✅ CLOSED (ratchet 2703→2732 across c/d) |
| W-TxtTrain-v2 | M5-adjacent (pre-M5) | ✅ CLOSED |
| W-Orchestrator-Resilience-r1 | M5-adjacent (pre-M5) | ✅ CLOSED |
| W-Shield-Train follow-ons P1..P6 (TaskEval-v1, Gradient-Step-Checkpoint, Row-Stream-Extractor, Adapter-Tensor-Persist, Queue-Watchdog, Cross-Table-Consistency-Check) | **UNHOMED** in 2026-09-13 binding — carried as follow-on backlog under SPRINT_PLAN.md priorities · candidates for §D of this document | Various states (below) |
| W-Audio-P2 (a..e) | UNHOMED · owner-blocked on archive access | BLOCKED (below) |
| W-WPW-v1-e Tier-3 | UNHOMED · owner-blocked on R1/R2/R3 | BLOCKED (below) |

**Verdict:** the 2026-09-13 M0..M5 binding is the current authoritative structure; the SPRINT_PLAN.md items either landed pre-M5 (all ✅ CLOSED above · pre-milestone ratchet 2024→2954) OR remain unhomed follow-ons that this document places below. **No owner-original mapping is being drifted from — the earlier structure and the current spine are consistent, with unhomed items surfaced explicitly.**

---

## §C · Re-homing tree (every item lives in a milestone · zero orphans)

Legend for state column:
- ✅ SEALED · has `phase0/output_verified_seals/*.seal.txt` or wave-close note
- ▶️ IN-FLIGHT · chartered + partly landed
- 🚧 CHARTERED · grounding brief authored · not yet started
- 🟡 CANDIDATE · named in a close-report recommendation · not yet chartered
- ⛔ BLOCKED-on-X · has an explicit blocker
- 🕰 DEFERRED-by-ruling · owner-agreed defer
- 🧭 PROPOSED · this document proposes; owner ratifies

---

### 🟢 M0 · Canon-delta extractions + supersession · **✅ SEALED (book-keeping)**

**Discharges:** SO §2 engagement discipline + Canon-1 §4.11 doctrine.
**% complete:** 100% (discharged-artefacts/promised-artefacts).

| Item | State | Notes |
|---|---|---|
| Canon-delta extractions (10 `canon_*_requirements.md` files) | ✅ SEALED | All present on disk |
| REUSE_ASSESSMENT_20260913.md + BUILD_STRATEGY_20260913.md supersession | ✅ SEALED | Aug-14 originals preserved |
| STATE/NEXT.md + STATE/PINS.md book-keeping refresh | 🕰 DEFERRED-by-ruling (Q5 DEFAULT-PENDING-OVERRIDE) | Owner-agreed defer |
| REUSE/BUILD supersession lineage note (§ORPH row) | ✅ SEALED under M0 | Part of the dated-successor artefacts |

---

### 🟢 M1 · W-DAP-STACK · DAP-1..DAP-30 · **✅ SEALED**

**Discharges (§END):** 10 DAP-A + 3 partial S + 2 Promise-# + 3 doctrines.
**% complete:** 100% (sealed-waves/chartered-waves = 8/8).

| Sub-wave | State | Seal |
|---|---|---|
| W-DAP-STACK 2A External-party admission | ✅ SEALED | `wdap_2a.seal.txt` |
| W-DAP-STACK 2B Trust-domain browse | ✅ SEALED | `wdap_2b.seal.txt` |
| W-DAP-STACK 2C Approval routing | ✅ SEALED | `wdap_2c.seal.txt` |
| W-DAP-STACK 2D Objective freeze + assistance-chat boundary | ✅ SEALED | `wdap_2d.seal.txt` |
| W-DAP-STACK 2E Metering + cumulative disclosure | ✅ SEALED | `wdap_2e.seal.txt` |
| W-DAP-STACK 2F Suspension + revocation | ✅ SEALED | `wdap_2f.seal.txt` |
| W-DAP-STACK 2G Coalition joint evaluation | ✅ SEALED | `wdap_2g.seal.txt` |
| W-DAP-STACK 2H Component boundary + composition close | ✅ SEALED | `wdap_2h.seal.txt` |
| **M1 openings (owner-input, blocking specific production-grade closes only):** DAP R-2 approving-authority · DAP R-6 pricing · **DAP R-3 per-party ceilings (COUPLED · re-rules at pilot end from R-7 PILOT-OPEN measured-usage · DECISIONS 2026-09-15T~03:55Z)** | ⛔ BLOCKED-on-owner | Wired tests-first with DEFAULT-PENDING-OVERRIDE markers |
| SFP-8 declared-dependency markers (per 2026-09-13 M3-Addendum) | ✅ SEALED as declared-dep markers | `[framing, not canon]` per owner C5 disposition |

---

### 🟢 M2 · Rules-Service + 11 Doc-0 attribute sub-waves · **✅ SEALED**

**Discharges (§END):** 12 Attributes + 3 Rules-R + 3 Promise-# + 2 Amendments + 2 doctrines + 1 new SFP-8 + TCB serving-integrity-gate row + FP hash-mismatch row.
**% complete:** 100% (close-notes/chartered-batches = 7/7 covering 11 sub-waves).

| Sub-wave / attribute | State | Close-note |
|---|---|---|
| W-M2-SW1 Rule Registry Bootstrap (Attr-4) | ✅ SEALED | `W_M2_SW1_RULE_REGISTRY_BOOTSTRAP_close.md` |
| W-M2-SW2 Rules Service Ceremony | ✅ SEALED | `W_M2_SW2_RULES_SERVICE_CEREMONY_close.md` |
| W-M2-SW3 Rule Book Library | ✅ SEALED | `W_M2_SW3_RULE_BOOK_LIBRARY_close.md` |
| W-M2-SW4 286-Rule Enumeration Classify | ✅ SEALED | `W_M2_SW4_286_RULE_ENUMERATION_CLASSIFY_close.md` |
| W-M2-SW5 G-8 Reliable-Time-Source | ✅ SEALED | `W_M2_SW5_G8_RELIABLE_TIME_SOURCE_close.md` |
| W-M2-SW6 SFP-8 Serving Integrity | ✅ SEALED | `W_M2_SW6_SFP_8_SERVING_INTEGRITY_close.md` |
| W-M2-SW7..SW15 Doc-0 Attributes 1/2/3/6/7/8/10/11/12 batch | ✅ SEALED (batched close) | `W_M2_SW7_SW15_DOC0_ATTRIBUTES_BATCH_close.md` |
| **W-PULL-SEAM-RECEIPT-UNIFY** — universal Pull-Seam P036 receipt-before-result across every operation surface (D9 drift resolution) | 🟡 CANDIDATE · **RE-HOMED IN M2 (Attr-8 AU-3 remainder)** · **BLOCKED-on-D9 owner ratification** | Home justification: Pull-Seam P036 receipt IS an AU-3-shaped record per Doc-0 §8 (see delta doc verbatim: *"certificate records are AU-3 subjects (Doc-0 §8); additive AU-3 subject class in the linter"*). M2 W-DOC0-ATTR8-AUDIT-AU3 already landed the AU-3 linter; the universal-receipt invariant is its natural extension. |
| **M2 openings:** Rules-Service R-2 (second-signatory named role) · DPO-S2 (reflection contract candidate selection) · Doc-0 G-8 fix (Reliable-Time-Source · spec-closed) · G-3 Registry-remainder (Mtafiti asset-inventory extension) | ⛔ BLOCKED-on-owner-input | Wired tests-first with DEFAULT-PENDING-OVERRIDE |

---

### 🟢 M3 · Watch + Registry CP10 + Pruning + Agent-Containment · **✅ SEALED with named open remainders**

**Discharges (§END):** 1 composite + 23 S + 3 partial-S + 16 AC + 2 RBM + 1 CP-close + 1 doctrine.
**% complete:** 100% (close-notes+seal-files/chartered = 14/14) · headline honesty note: several sub-rows are **spec-closed / not-built** by design per M3 binding.

| Sub-wave / promise row | State | Close-note / seal |
|---|---|---|
| W-REGISTRY-FULL-BUILD CP10 (real-Chromium DOM proof) | ✅ SEALED | `wregistry_cp10.seal.txt` |
| W-G3-REMAINDER (Registry remainder wave) | ✅ SEALED | `wg3_remainder.seal.txt` |
| W-M3-SW1 FLAG2 Tight Budget | ✅ SEALED | close-note |
| W-M3-SW2 Watch Stack Core | ✅ SEALED | close-note |
| W-M3-SW3..SW6 Watch Learning Certificate-Library + Mirage-Provocation + Research-Queue + Capability-Admission | ✅ SEALED | 4 close-notes |
| W-M3-SW7 Agent Containment (AC-1..AC-12) | ✅ SEALED | close-note |
| W-M3-SW8 Pruning + Unlearning | ✅ SEALED | close-note |
| W-M3-SW9 V3 AC-13 + AC-14 addendum | ✅ SEALED | close-note |
| W-M3-SW10 BCA S-10 + S-11 + BC-1 + BC-2 | ✅ SEALED | close-note |
| W-M3-SW11 DAP-33/34/35 remainders | ✅ SEALED | close-note |
| W-M3-SW12 M3 Block Completion | ✅ SEALED | close-note |
| **M3 spec-closed, not-built (M3 §Δ delta):** S-24 raiser-conformance · S-27 Voice · S-28 verdict-certificate · S-29 capability-admission-ceremony | ✅ SEALED at spec-level · ⛔ BLOCKED-on-owner-ratification-for-build (Watch-Learning R-15(b)/R-16(b)/R-17(b) still OPEN 2026-09-15T~03:55Z per owner: *"do not conflate"*) | Production build follows R-15(b)/R-16(b)/R-17(b) ratifications; RULING_LEDGER OPEN rows 9/10/11 |
| **`W-BC-DYNAMIC-RECOVERY-BUILD`** — 4-tier BC packet build (BC-3/BC-4 discharge post-packet-ratification) | 🟡 CANDIDATE · **RE-HOMED IN M3 (BCA §3 BC-3/BC-4 discharge)** · **BLOCKED-on-BC-packet-ratification** | Home justification: BCA §3 sits inside M3 W-M3-SW10 (S-10 + S-11 + BC-1 + BC-2). BC-3 + BC-4 are the remaining Annex-§3 rulings; packet at `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` (2026-09-15T~03:55Z owner ruling verbatim: *"DO NOT SET A STATIC NUMBER · BUILD THE DYNAMIC-RECOVERY DECISION PACKET"*). Post-ratification wave lands 18 invariants across 4 tiers (GPU-DCP-Young/Daly · ledger-WAL-PITR · WORM · warm-standby+drills). |
| **M3 openings:** Watch-Learning R-15(b)/R-16(b)/R-17(b) · Amendment 8 (HOLD per owner C1) | ⛔ BLOCKED-on-owner-input | Owner explicitly said 2026-09-15T~03:55Z: *"The Watch-Learning R-15(b)/R-16(b)/R-17(b) set stays OPEN — do not conflate"* |

---

### 🟢 M4 · Assistant surfaces · **✅ SEALED**

**Discharges (§END):** 1 Promise-# + 4 canon sections + 1 doctrine.
**% complete:** 100% (close-notes/chartered = 6/6).

| Sub-wave | State | Close-note |
|---|---|---|
| W-M4-SW1 Solva Explain Surface | ✅ SEALED | close-note |
| W-M4-SW2 Never Pre-Fill | ✅ SEALED | close-note |
| W-M4-SW3 Estate-Check Chip | ✅ SEALED | close-note |
| W-M4-SW4 Three Verdicts | ✅ SEALED | close-note |
| W-M4-SW5 Handoff Contract | ✅ SEALED | close-note |
| W-M4-SW6 M4 Block Completion | ✅ SEALED | close-note |
| **W-JOURNEY-ASSISTANT** (universal wizard-chat pattern per `JOURNEY_AND_ASSISTANT_AUDIT_20260913.md:116`) | 🕰 DEFERRED-by-ruling (owner NOT-RULED-IN per `W_REGISTRY_EXTENSION_G3_grounding_brief.md:48`) | Home is M4 (matches Canon-5 §14 · Canon-6 §3/§6/§12 discharge); wave folded here as an owner-optional extension of the seal-set. |

---

### 🟢 M5 · Data-Suite-v2 lift + Audio-POC build · **▶️ IN-FLIGHT**

**Discharges (§END):** DAP-A10 remainder + Promise #12 (census-and-connection) + Audio-Plane §1.2 + doctrine §4.6.
**% complete (session-scope):** 100% (chartered-and-sealed / chartered-in-session = 3/3 · W-DATA-SUITE-V2-LIFT + W-AUDIO-POC + W-CENSUS-CANON-ALIGN); **50% by §END promise inventory** (2/4 discharged; will become 4/4 after Audio-POC end-to-end + Item-3 census both fire).

| Sub-wave / promise | State | Notes |
|---|---|---|
| **W-DATA-SUITE-V2-LIFT** (3 surfaces per §M5 LIFTING) | ✅ SEALED | `data_suite_v2_lift.seal.txt` · ratchet delta +50 |
| **W-AUDIO-POC** (first real-audio job · Promise #12 extension) | ✅ SEALED | `audio_poc_v1.seal.txt` · ratchet delta +71 |
| **W-CENSUS-CANON-ALIGN** (CP-C1..C6 · pre-census discipline-alignment · Option-α ratified) | ✅ SEALED · **RE-HOMED IN M5 (Promise #12 census-and-connection discharge)** | `census_canon_align.seal.txt` · ratchet delta +39 · Home justification: §M5 verbatim: *"Promise #12 · Census and connection — fully discharged by M5 via Audio-POC extending Mtafiti census with audio modality (Canon-1 §4.6 extension, not sibling registry)."* CP-C1..C6 land the frozen contracts (SourceCandidate · Measurement · CensusRun · SourceRecord · JobManifest · SourceStratumMeasurement + ActivationList) that Promise #12 discharge depends on. |
| **Item-3 · live read-only census run (Promise #12 fires)** | 🚧 CHARTERED · armed at W-CENSUS-CANON-ALIGN seal · **⛔ BLOCKED-on-egress-window-close** (fires at 08:00 UTC re-open) | Runs against NAS 16 channels + OBS google-transcripts + weego + ussd MySQLs. Zero PII in receipts. CPU-viable on this pod per §E.6 grounding brief. |
| **W-RELEASE-GATE-PILOT-LIFT** (5 CPs · R-7 PILOT-OPEN + R-15(a) TOKENIZED + R-16(a) DERIVATIVE_ONLY_VIA_PULL_SEAM wiring) | 🚧 CHARTERED · **RE-HOMED IN M5 (Audio-POC end-to-end / DAP-A10 remainder discharge)** · **⛔ BLOCKED-on-census-completion** (owner sequencing pin) | Home justification: §M5 verbatim: *"DAP-Spec `A10` · Artefact egress remainder from M1 → fully discharged by M5"*. Release-gate is the artefact-egress chokepoint carrying R-7 PILOT-OPEN + R-15(a) TOKENIZED + R-16(a) DERIVATIVE_ONLY verdicts (owner ruling 2026-09-15T~03:55Z). Also composes with M1 DAP-A9 (key hygiene / no-key-in-receipts) and W-AUDIO-POC transcript emission. Grounding brief at `notes/wave_release_gate_pilot_lift_grounding_brief.md`. |
| **D12 POC (whisper-tiny + faster-whisper on bounded NAS files)** | 🚧 APPROVED · **RE-HOMED IN M5 (Audio-POC end-to-end)** · **⛔ BLOCKED-on-W-RELEASE-GATE-PILOT-LIFT-completion** | Home justification: Audio-POC end-to-end includes real-transcription pipe-proof (§M5 BUILDING · Audio-POC extends Mtafiti census with audio modality). Owner ruling 2026-09-15T~03:55Z verbatim: bounded single-digit-count NAS files · GPU hosts `akki-vm`/`akki-vm-ii` · `poc_flag=POC-NOT-PRODUCTION` provenance · receipts banked. |
| **W-TRUST-SURFACE-v2** (2 surfaces per §M5 LIFTING) | 🕰 DEFERRED-by-ruling (DPO-D2 default at W-DATA-SUITE-V2-LIFT open · owner-agreed OUT-OF-SESSION-SCOPE) | Home is M5-LIFTING per binding line 408. Owner may unblock at any time. |
| **W-EXECUTIVE-SUITE-v2-LIFT** (7 surfaces per §M5 LIFTING) | 🕰 DEFERRED-by-ruling (DPO-D2 default · same context) | Home is M5-LIFTING per binding line 409. |
| **M5 openings:** R-17(a) licence-class hardening (owner: *"stays open (non-blocking)"* 2026-09-15T~03:55Z) · Six other Audio-Census open-governance chokepoints (KDPA biometric · KDPA named-individuals · cross-border §48 · purpose-limitation §51 · DAP R-6 pricing · DAP R-7 disclosure budget) | ⛔ BLOCKED-on-owner-input | R-7 already RATIFIED (PILOT-OPEN) 2026-09-15T~03:55Z — carried lineage in M5 openings for audit-trail completeness. |

---

### 🧭 M6 (PROPOSED · owner ratifies) · Audio-Plane v1.0 production build

**Justification.** Audio-Plane v1.0 spec verbatim (`AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md:8`): *"consolidated build specification. It supersedes the working drafts (Audio Capability Spec v1.0 and Addendum v1.1.2) and is the single reference for build."* §15 declares an 11-item **build sequence** with strict dependency ordering. The Audio-POC (M5) is the pipe-proof for Promise #12; the production Audio Plane is the successor scope. Owner's own example verbatim (2026-09-15T~04:05Z): *"M6 = Audio Plane production build per §15 order"* — this document follows that directive.

**Proposed scope:** all 11 items of Audio-Plane v1.0 §15 build sequence, in canon-authored dependency order.

**Sub-wave breakdown (PROPOSED):**

| # | Sub-wave (verbatim §15) | Prerequisite | Estimate class |
|---:|---|---|---|
| 1 | **W-M6-INGEST-STAGE-1** · Ingestion capture: language ID, code-switch points, condition profile, synthesis attributes (§4.1–4.4) | M5 census + release-gate lift landed | L (~1 week) |
| 2 | **W-M6-DEDUP-INSTANCE-CONDITION-MAP** · Dedup instance condition map (§4.5) | Contract change to existing machinery | S (~2 days) |
| 3 | **W-M6-CHARACTER-REGISTER** · Character Register schema + custody invariant harness (§6) | Boundary must exist before first cluster stored | L (~1 week) |
| 4 | **W-M6-CODEC-SERVICE** · Codec service (§3) · `perception/audio_codec/` | Independent of 1–3 (unsupervised pretraining parallel) | L (~1 week) |
| 5 | **W-M6-CLUSTERING-HUMAN-VALIDATION** · Clustering + sampled human validation (§5.3) | Requires 1–4 | M (~3 days) |
| 6 | **W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA** · Objective Wizard variant + Collection Schema type + registry namespace (§8, §9, §12.1) | Independent — but planner-first refuses malformed input | M (~4 days) |
| 7 | **W-M6-TARGET-OUTCOME-PLANNER** · TargetOutcome type + planner core (§10, §11.1, §11.4) | Requires 3 + 6 | L (~1 week) |
| 8 | **W-M6-SAMPLING-REFLECTION** · Sampling & Reflection machinery + milestone records (§11.2–11.3) | Requires 7 + test set | M (~4 days) |
| 9 | **W-M6-COMMISSION-VIEW** · Commission View (§13) | Requires 8 | S (~2 days) |
| 10 | **W-M6-FULL-TRAINING-RUNS** · Full training runs under the commissioned-job contract (§11.6) | Requires 7–9 | L (~1 week) |
| P2 | **W-M6-VOICE-IDENTITY-RENDERING** (Phase-2 deferred by design) · Voice identity rendering; music register (§7.5 non-foreclosure) | Non-foreclosure only this milestone | DEFERRED-BY-DESIGN |

**M6 openings (upstream to Audio-Plane build):** D10 Silero VAD INFERRED · D11 pyannote/speaker-diarization-3.1 INFERRED · D7 codec_version carrier · N1..N10 drift-audit backlog items (nine on-disk enumerated per prior book-keeping observation) all fold into M6 sub-waves per canon §15 dependency map.

**M6 status now:** 🧭 PROPOSED · 0 sealed · owner ratifies before charter.

---

### 🧭 M7 (PROPOSED · owner ratifies) · Governed Census/Harvest Platform (W0..W9)

**Justification.** `notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md` (51,814 B · dated 2026-09-13T~05:03Z) declares (`:3` verbatim): *"Task class: DESIGN REFRAME · read-only · no pipeline build, no code commits, no push, ratchet 3251 untouched. POC/build HOLD until owner ratifies this reframe."* The roadmap redraws the whole programme as a **10-plane platform** (A.1..A.10) + **case-mounted JobManifest** (A.11) + **build waves W0..W9** (W0 platform integrity · W1 platform generalisation · W2..W9 job waves). Owner's own example verbatim (2026-09-15T~04:05Z): *"M7 = Governed Census/Harvest platform W0..W9"* — this document follows that directive.

**Proposed scope:** 10-Plane Platform + W0..W9 build waves.

**Sub-wave breakdown (PROPOSED):**

**Phase M7-α · Platform (2 waves per roadmap `:530`):**
| # | Sub-wave (verbatim roadmap) | Estimate |
|---:|---|---|
| W0 | **W-M7-W0-INTEGRITY-FIX** · Integrity fix — silent-success defect (S-class · PLATFORM) | S |
| W1 | **W-M7-W1-PLATFORM-GENERALISATION** · Work-supervisor + Resource Registry + Capability Registry generalisation (M-class · PLATFORM) | M |

**Phase M7-β · Job waves (8 waves per roadmap `:709`):**
| # | Sub-wave (verbatim roadmap) | Blocker |
|---:|---|---|
| W2 | Mount + run vertical slice ONE station (L-class · JOB) | W0+W1 closed + NAS reachable + owner ratifications |
| W3 | Scale to 3 stations (M-class) | W2 closed |
| W4 | Scale to 16 stations | W3 closed |
| W5 | Character Register wave (§5-§7 invention layer) | W4 closed |
| W6 | DAP sale surface (R-6/R-7 bindings) | owner rules R-6 · R-7 already PILOT-OPEN |
| W7 | WPW Tier-2 draft-on-settle emitter | independent |
| W8 | Release-gate ADMISSIBLE lift (Ruling #5 verdicts) | R-7/R-15(a)/R-16(a) all RATIFIED 2026-09-15T~03:55Z ✅ · ready when M7-α seals |
| W9 | Owner-ruling A/B/C for audio-bytes-retention | owner rules Path A/B/C |

**10-plane state summary (per PROGRAMME_STATE_BEYOND_M5_20260915.md §B):**
| Plane | Current % (session-current) |
|---|---:|
| A.1 Resource Plane | ~20% |
| A.2 Source Plane | ~30% (SourceCandidate landed CP-C1) |
| A.3 Capability Registry | ~30% |
| A.4 Objective Plane (L1) | 50% |
| A.5 Outcome + Quality Plane (L2) | ~25% (SourceStratumMeasurement 8-dim landed CP-C6) |
| A.6 Success + QC Plane (L3) | ~35% |
| A.7 Commission + Worker Plane (L4) | ~15% |
| A.8 Supervision Plane (L5) | 0% |
| A.9 HITL Plane (L6) | 0% |
| A.10 Governance Plane | 60% |
| A.11 JobManifest | ~30% (5/13 carriers landed CP-C5) |
| A.12 Platform build waves W0+W1 | 0% (HOLD) |

**M7 status now:** 🧭 PROPOSED · 0 sealed · **BLOCKED on owner reframe-ratification** (the roadmap itself is `POC/build HOLD until owner ratifies this reframe` verbatim).

---

### 🧭 M8 (PROPOSED · owner ratifies) · Post-launch hardening + §COV/§ORPH catch-all

**Justification.** Everything from PROGRAMME_STATE_BEYOND_M5 §E (16 follow-on candidates from close reports), §F (§COV+§ORPH uncatalogued backlog), and the pre-M5 SPRINT_PLAN.md P1..P6 priority tracks that never migrated to the M0..M5 spine. Small waves each · not milestone-scale · but need a home.

**Sub-wave breakdown (PROPOSED):**

| Sub-wave | Current state | Source |
|---|---|---|
| **W-CENSUS-RUNTIME-ORCHESTRATION** (runtime wiring for CP-C5 data-only JobManifest) | 🟡 CANDIDATE | `W_CENSUS_CANON_ALIGN_close.md:70` |
| **W-EXPORT-ARTEFACT-RENDER** (render CSV/PDF export bytes behind D6 gate) | 🟡 CANDIDATE (S · high user-visible value) | `W_DATA_SUITE_V2_LIFT_close.md:93` |
| **W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL** (replace HALT skeletons · paired) | 🟡 CANDIDATE | `W_DATA_SUITE_V2_LIFT_close.md:92` |
| **W-TESTS-FIRST-GUARD-INVARIANT** (automated parse-not-paraphrase on drill-receipts) | 🟡 CANDIDATE (S · hardening · zero owner-input) | `W_DATA_SUITE_V2_LIFT_close.md:95` |
| **W-AUDIO-PROD-MODEL-SELECT** (production-model selection · not CI-fixture · §A17.11 anchor) | 🟡 CANDIDATE · **BLOCKED-on-D12-POC-completion + owner-selection-ruling** | Owner ruling 2026-09-15T~03:55Z verbatim: *"Production model selection still follows census activation per §A17.11 — the POC does not pre-empt it."* |
| **W-Watch-Foundation (Track-B open)** — audio-domain Watch surface (72 requirement rows) | 🟡 CANDIDATE | `GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md:872` |
| **W-Audio-P2 (audio-archive Phase-2 admission)** | ⛔ BLOCKED-on-archive-access + owner-provided credentials | `SPRINT_PLAN.md:84,204` |
| **W-MTAFITI-GPU-EMBEDDINGS + W-MTAFITI-DEEP-SWEEP** (Mtafiti follow-ons) | 🟡 CANDIDATE (§ORPH remainder) | `MILESTONE_PROMISE_BINDING §ORPH` |
| **Quarantine-restoration D1a-1** (19 files · 88 tests · event-loop-closed residue) | 🟡 CANDIDATE | `waveD_close_report.md:158,164,229` |
| **W-Rights-Quarantine (Canon 4 §41)** | ▶️ PARTIAL (spec-close only) | referenced in DECISIONS.md wave-cross-links |
| **W-TaskEval-v1** (task-shaped held-out eval · P1 SPRINT priority) | 🟡 CANDIDATE (M) | `SPRINT_PLAN.md:15` |
| **W-Gradient-Step-Checkpoint** (mid-epoch resume · P2 SPRINT priority) — **NOTE: partially superseded by BC packet Tier-1 GPU checkpointing** (folds into M3 W-BC-DYNAMIC-RECOVERY-BUILD) | 🟡 CANDIDATE (S-M) · **preferred re-home: M3 BC-BUILD** | `SPRINT_PLAN.md:25` |
| **W-Row-Stream-Extractor** (bounded-memory row extraction · P3 SPRINT priority · unlocks >1M-row corpora) | 🟡 CANDIDATE (M) | `SPRINT_PLAN.md:35` |
| **W-Adapter-Tensor-Persist** (adapter registry · P4 SPRINT priority) | 🟡 CANDIDATE (M) · depends on W-TaskEval-v1 | `SPRINT_PLAN.md:43` |
| **W-Queue-Watchdog** (dispatcher-level restart · P5 SPRINT priority) | 🟡 CANDIDATE (S) | `SPRINT_PLAN.md:53` |
| **W-Cross-Table-Consistency-Check** (multi-emitter cross-table PII correlation · P6 SPRINT priority) | 🟡 CANDIDATE (S) | `SPRINT_PLAN.md:61` |
| **W-WPW-v1-e Tier-3** (Whitepaper Wizard Tier-3 white-paper) | ⛔ BLOCKED-on-R1/R2/R3 (WPW-specific owner rulings) | `SPRINT_PLAN.md:80` |
| **Sysadmin follow-up on 9 SG-blocked hosts** | 🟡 CANDIDATE (§ORPH · environmental) | `MILESTONE_PROMISE_BINDING §ORPH` |
| **STATE/NEXT.md + STATE/PINS.md book-keeping refresh** (M0-deferred) | 🕰 DEFERRED-by-ruling (Q5 default) | `MILESTONE_PROMISE_BINDING §M0` |

**M8 openings (§COV uncatalogued rulings):** WPW R-2 external-release signatory · Amendment 8 scope-statement (HOLD per owner C1 2026-09-13) · DPO-S2 reflection-contract selection · LIM-1..5 (non-claims · never discharged by design).

**M8 status now:** 🧭 PROPOSED · 0 sealed · owner ratifies.

---

## §D · Zero-orphan audit (every item accounted for)

**Every item from `PROGRAMME_STATE_BEYOND_M5_20260915.md`, `PENDING_RATIFICATIONS_LEDGER_20260915.md`, §COV, §ORPH now homed:**

| Item | Homed under |
|---|---|
| R-7 (release budget) · flipped PILOT-OPEN 2026-09-15T~03:55Z | M1 openings (DAP R-3 COUPLED · re-rules at pilot end) + M5 W-RELEASE-GATE-PILOT-LIFT (mechanism) |
| R-13 (SIA validation cadence · RATIFIED) | M0 amendment fold-in |
| R-14 (candidate serving engine · OPEN) | M2-adjacent (SFP-8 · gated by appliance benchmark + TCB admission ceremony) |
| R-15(a) (named-persons · TOKENIZED) | M5 W-RELEASE-GATE-PILOT-LIFT CP-RG2 |
| R-15(b) (Watch-Learning cert-library seed · OPEN) | M3 W-WATCH-STACK-SW3 (spec-closed, awaits owner ratification) |
| R-16(a) (transfer-basis · DERIVATIVE_ONLY_VIA_PULL_SEAM) | M5 W-RELEASE-GATE-PILOT-LIFT CP-RG3+CP-RG4 |
| R-16(b) (Watch-Learning ratifier + cadence · OPEN) | M3 W-WATCH-STACK (spec-closed, awaits ratification) |
| R-17(a) (Audio-POC licence-class hardening · OPEN non-blocking) | M5 opening |
| R-17(b) (Watch-Learning capability-class granularity · OPEN) | M3 W-WATCH-STACK + W-AGENT-CONTAINMENT (spec-closed, awaits ratification) |
| BC-3 · BC-4 (DYNAMIC-RECOVERY-PACKET direction · packet authored 2026-09-15T~03:55Z) | M3 W-BC-DYNAMIC-RECOVERY-BUILD (post-packet-ratification) |
| S-24 (raiser conformance · spec-closed, not built) | M3 W-WATCH-STACK Class-D/A finding surface (spec) |
| S-27 (Voice Amendment · spec-closed, not built) | M3 W-WATCH-STACK (spec) |
| S-28 / S-29 (Watch-Learning L-1..L-5 · spec-closed) | M3 W-WATCH-STACK + W-AGENT-CONTAINMENT (spec) |
| D7 (codec_version drift · NOT-YET-IN-SCOPE for legacy) | 🧭 M6 (Audio Plane · §15 item 4 codec-service) |
| D9 (universal receipt-before-result · OPEN) | M2 W-PULL-SEAM-RECEIPT-UNIFY (Attr-8 AU-3 remainder) |
| D10 (Silero VAD INFERRED · OPEN) | 🧭 M6 (Audio Plane · §15 item 1 ingest-stage VAD) |
| D11 (pyannote INFERRED · OPEN) | 🧭 M6 (Audio Plane · §15 item 1 ingest-stage diarization) |
| D12 (whisper-tiny POC · APPROVED 2026-09-15T~03:55Z) | M5 (bounded POC · after W-RELEASE-GATE-PILOT-LIFT seal) |
| DAP R-6 (pricing) · WPW R-2 · DAP R-2 · Rules-Service R-2 · DPO-S2 | M1/M2 openings + 🧭 M8 remainder |
| 10-Plane Platform (A.1..A.11) + W0..W9 | 🧭 M7 (Governed Census/Harvest Platform) |
| Audio-Plane §15 items 1..10 + P2 (11 items) | 🧭 M6 (Audio Plane production build) |
| N1..N10 Audio Plane drift-audit backlog | 🧭 M6 (all fold into §15 dependency map) |
| W-TRUST-SURFACE-v2 (2 surfaces) | M5-LIFTING · DPO-D2 deferred |
| W-EXECUTIVE-SUITE-v2-LIFT (7 surfaces) | M5-LIFTING · DPO-D2 deferred |
| W-JOURNEY-ASSISTANT | M4-adjacent (NOT-RULED-IN by owner · optional extension) |
| W-CENSUS-RUNTIME-ORCHESTRATION | 🧭 M8 (post-launch hardening) OR 🧭 M7 (JobManifest runtime wiring) |
| W-EXPORT-ARTEFACT-RENDER · W-DATA-SUITE-ANALYZE-* REAL · W-TESTS-FIRST-GUARD | 🧭 M8 |
| W-AUDIO-PROD-MODEL-SELECT | 🧭 M8 (or M6-adjacent · post-D12-POC + post-census) |
| W-Watch-Foundation (Track-B audio-domain Watch · 72 rows) | 🧭 M8 (or M6-adjacent) |
| W-Audio-P2 (archive Phase-2 admission) | 🧭 M8 (BLOCKED on archive access) |
| W-MTAFITI-GPU-EMBEDDINGS + W-MTAFITI-DEEP-SWEEP | 🧭 M8 (§ORPH) |
| Quarantine-restoration D1a-1 (89 tests · 19 files) | 🧭 M8 |
| W-Rights-Quarantine (Canon 4 §41 · partial) | M3 remainder |
| W-TaskEval-v1 · W-Gradient-Step-Checkpoint · W-Row-Stream-Extractor · W-Adapter-Tensor-Persist · W-Queue-Watchdog · W-Cross-Table-Consistency-Check | 🧭 M8 (SPRINT_PLAN P1..P6 tracks) |
| W-WPW-v1-e Tier-3 | 🧭 M8 (BLOCKED-on-R1/R2/R3 · WPW-specific) |
| STATE/NEXT.md + STATE/PINS.md book-keeping | M0 (DEFERRED-by-ruling) |
| REUSE/BUILD supersession lineage | M0 (✅ SEALED) |
| Doc-0 G-8 reliable-time-source fix | M2 W-M2-SW5 (✅ SEALED) |
| G-3 Registry remainder (Mtafiti asset-inventory) | M2 opening (owner-scope) |
| Sysadmin 9-SG-blocked hosts | 🧭 M8 |
| Amendment 8 scope-statement (HOLD) | M3 opening |
| LIM-1..5 (non-claims by design · never discharged) | M3 (recorded, never counted per binding §COV) |

**Orphan count: 0.** Every item has a milestone home.

---

## §E · Standing at present (summary)

**Bound milestones (owner-ratified 2026-09-13 spine):**

| Milestone | State | % (session-scope) | Method |
|---|---|---:|---|
| M0 | ✅ SEALED (book-keeping) | 100% | discharged-artefacts/promised |
| M1 | ✅ SEALED | 100% | sealed-waves/chartered = 8/8 |
| M2 | ✅ SEALED (with W-PULL-SEAM-RECEIPT-UNIFY re-homed as Attr-8 remainder) | 100% (core) · Attr-8 remainder pending on D9 ratification | close-notes/chartered = 7/7 core |
| M3 | ✅ SEALED (with W-BC-DYNAMIC-RECOVERY-BUILD re-homed as BC-3/BC-4 discharge) | 100% (core) · BC-build pending packet-ratification | close-notes/chartered = 14/14 core |
| M4 | ✅ SEALED | 100% | close-notes/chartered = 6/6 |
| M5 | ▶️ IN-FLIGHT (W-CENSUS-CANON-ALIGN sealed · Item-3 armed · W-RELEASE-GATE-PILOT-LIFT chartered · D12 approved) | 100% session-scope · 50% §END promise inventory (2/4 → 4/4 post-Item-3 + Audio-POC-e2e) | chartered-and-sealed/chartered = 3/3 |

**PROPOSED post-M5 milestones (this document · not self-ratified · owner ratifies):**

| Milestone | Scope | State | Estimate class |
|---|---|---|---|
| 🧭 M6 | Audio-Plane v1.0 production build (§15 items 1..10 + P2) | PROPOSED · 0 sealed · 11 sub-waves | Long (~6-8 weeks concentrated) |
| 🧭 M7 | Governed Census/Harvest Platform (W0..W9 + 10 planes) | PROPOSED · 0 sealed · **⛔ BLOCKED on owner reframe-ratification** (POC/build HOLD per roadmap `:3`) | Very Long (~months) |
| 🧭 M8 | Post-launch hardening + §COV/§ORPH catch-all + SPRINT-P1..P6 tracks | PROPOSED · 0 sealed · ~19 sub-waves | Medium (~3-5 weeks concentrated) |

---

## §F · Sequencing pin (owner-ratified 2026-09-15T~03:55Z · UNCHANGED)

> "census at 08:00 UTC (unchanged, first priority) → W-RELEASE-GATE-PILOT-LIFT → D12 POC → BC packet authoring can happen in closed-window time as it's non-egress."

**Applied literally per this re-homing:**
1. **M5 · Item-3 · live census run** at 08:00 UTC re-open (fires Promise #12 discharge).
2. **M5 · W-RELEASE-GATE-PILOT-LIFT** · 5 CPs · tests-first · discharges DAP-A10 remainder.
3. **M5 · D12 POC** · bounded transcription-pipe-proof on GPU hosts (Audio-POC end-to-end).
4. **M3 · BC packet ratification** (owner reviews) · then **M3 · W-BC-DYNAMIC-RECOVERY-BUILD** (18 invariants).
5. **M2 · W-PULL-SEAM-RECEIPT-UNIFY** (if D9 ratifies) · Attr-8 AU-3 remainder.
6. **🧭 M6/M7/M8** · owner ratifies proposals · then chartering + sequencing.

---

## §G · Book-keeping observations preserved (from prior compile)

1. **Pull-Seam verbatim ledger is INCOMPLETE.** P1 + P7 principle bodies extracted; P2..P6 bodies missing from on-disk ledger. Recommend extension before W-PULL-SEAM-RECEIPT-UNIFY charter opens under M2.
2. **`AUDIO_PLANE_V1_DRIFT_AUDIT` numbering inconsistency** (declares 10 N-items · enumerates 9 · N7 skipped). Bank correction under 🧭 M6 grounding-brief authoring.
3. **`R-15/R-16/R-17` mnemonic conflation** — resolved 2026-09-15T~03:55Z (owner explicit: "do not conflate"). Ledger row-flips banked; (a) branch RATIFIED for release-gate; (b) branch STAYS-OPEN for Watch-Learning.

---

## §H · Position-redaction acknowledgement

Every row above:
- Cites disk-file paths and line numbers.
- Does not echo credentials, host IPs, SSH usernames, or PII.
- Preserves owner-side scrub directives verbatim (R-14 engine-name scrub 2026-09-14).
- Uses aliases only for estate hosts (`akki-vm`, `akki-vm-ii`, `synology-nas`).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
