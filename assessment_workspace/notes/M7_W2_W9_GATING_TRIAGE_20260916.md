READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M7 W2..W9 · from-disk gating triage · 2026-09-16T~08:35Z

**Authority.** Owner steer verbatim 2026-09-16T~08:35Z:

> "OWNER STEER: 'On to the nxt milestone?' — read as: advance the milestone frontier as far as existing owner law allows. Exit pure hold, run this sequence (boot ritual first if resuming): 1. W2..W9 GATING TRIAGE (from-disk, honest) ... 2. FIRE whatever is BUILDABLE-NOW or PARTIALLY-BUILDABLE, in dependency order, tests-first, case-agnostic, §3.3 seals ... 3. M6/M8 seal-readiness notes ... 4. Utilization interleave continues at every boundary. Report at triage completion with the table + what you started building."

**Standing lines the owner reasserted (verbatim):**
- No training on estate audio (SW-10 deferred).
- No biometric material.
- No enforcement hard-gate.
- No speculative shapes beyond existing owner law.

**Boot ritual re-verify (this-turn).** STANDING_ORDERS.md read prior · DECISIONS/NEXT tail current · ratchet floor 4400 stable (`baseline_failures.json` `passed_floor=4400` · `counts_at_baseline.passed=4400` · matches) · master HEAD `3a9ff2ca` · track-a HEAD `b547cd4` · egress OPEN · SEC HALT probes NOTE-SKIPPED pending JUMP rotation.

**Method.** From-disk (POST-2 discipline: check what exists before proposing any build). Every "already landed" claim cross-referenced against `services/` + master log + M8 rollup + M6 sub-wave close notes.

---

## §1 · W2..W9 triage table

| Wave | Charter scope (ROADMAP §B.3 verbatim) | Gating condition as written (§B.3 prereqs + §E.2) | From-disk status of gating condition | Verdict |
|---|---|---|---|---|
| **W2** · Mount + run vertical slice ONE station (L-class · JOB) | *"CP2.1 Mount JobManifest v1 (single station: Inooro FM). CP2.2 Instantiate the eight capability_ids ... CP2.3 NAS reachability preflight + SynologyFileStationConnector.list() + composition census. CP2.4 Stage ONE 30-min file to akki-vm via connector.stream() under the read-only guard. CP2.5 Fire capability pipeline (parallel per §1.7). CP2.6 Compose AudioAttributeStreamBundle_v0. CP2.7 L6 milestone ratification. CP2.8 Wave close."* | 1. W0/W1 platform closed. 2. NAS network path opened. 3. HF token in `backend/.env`. 4. `requirements.txt` deps added. 5. Owner-ratified 3-station selection. 6. Owner ruling on RetentionPolicy Path A/B/C. | 1. ✅ W0/W1 verified 9/9 chain (M-family). 2. ⚠ PARTIAL — OFFAIRRECS reachable via `mount.cifs vers=3.0 rsize=4M` (D12-01 breakthrough 2026-09-15) but is video-only-with-null-audio (D12-03 corpus-level finding); 5 audio-bearing shares Permission-denied for Bramwel account. 3. ⚠ HF token last used at W-AUDIO-POC CP-A5 `services/audio_poc/hf_transcribe.py`; live-probe blocker banked at `notes/W_AUDIO_POC_CP_A5_LIVE_PROBE_BLOCKER_20260914.md`. 4. ✅ deps added at M5. 5. ❌ 3-station selection NOT ratified. 6. ❌ Path A/B/C ruling NOT landed; roadmap default = **Path C** (§C.2 verbatim: *"Default if no ruling by W2 CP0: Path C."*). | **PARTIALLY-BUILDABLE** · buildable slice: (a) **CP-M7-W2-CONTRACT-1** JobManifest v1 CONTRACT SHELL for `job_class="audio-census"` — extends existing `services/work_supervisor/job_manifest.py` with an audio-census `scope` sub-carrier as a frozen dataclass with opaque strings for station identifiers · `stations_owner_ratified: bool = False` gate that refuses mount until owner ratification lands. Case-agnostic composition. Blocked remainder: CP2.3..CP2.8 (live station data). |
| **W3** · Scale to 3 stations (M-class · JOB) · *"Replicate W2 on Inooro + Ramogi + Musyi with hybrid-ASR routing."* | Same as W2 + W2 close + 3-station selection ratified. | Same as W2. | **BLOCKED-on-<W2-close + 3-station-selection>**. |
| **W4** · Scale to 16 stations (roadmap §B.3). | Same as W2 + W3 close + 16-station manifest. | Same as W2 + W3 blocked. | **BLOCKED-on-<W3-close>**. |
| **W5** · Character Register wave (§5-§7 invention layer). | *"Character Register with centroids/distributions/frequencies · voiceprint unrepresentable-by-construction · Audio Plane §6.1 §6.2 §6.3 verbatim."* | Audio-Plane §5-§7 canon. | ✅ **ALREADY LANDED IN M6** as follows (from-disk verified): `services/audio_plane_v1/character_register.py` + `register_read_boundary.py` + `register_write_boundary.py` (M6 sub-wave 6 · CP-M6-6-1..CP-M6-6-4 — sealed 2026-09-15 · +42 invariants · §6.2 unrepresentable-by-construction pattern enforced). Also `services/audio_plane_v1/clustering.py` + `cluster_stability.py` + `human_validation.py` (M6 SW5 W-M6-CLUSTERING-HUMAN-VALIDATION · sealed 2026-09-15 · +27 invariants). | **EFFECTIVELY DONE via M6** — W5 charter is satisfied by M6 sub-wave 5 + sub-wave 6 mechanism modules. No new build needed. Wave-honest limit: W5 was authored 2026-09-11 before the M6 build overtook it — the milestone spine 2026-09-15 rehomed §5-§7 into M6 Audio-Plane V1 Production Build. **Buildable slice**: a **W5 verification note** documenting the satisfying M6 CP set (analog of M7 verification walk shape) — no code · no ratchet. |
| **W6** · DAP sale surface (R-6/R-7 bindings). | R-6 pricing · R-7 disclosure budget. | Owner rulings on R-6 pricing + R-7. | R-6 pricing: ❌ owner-desk P2. R-7 PILOT_OPEN: ✅ ratified 2026-09-15 in W-RELEASE-GATE-PILOT-LIFT (verbatim owner ruling: R-7 PILOT_OPEN). Modules: `services/release_gate/release_ledger.py` (record_debit) + `services/audio_poc/release_gate.py` (admit_transcript_release_pilot_open composition wired at CP-RG4) + `services/dap/disclosure_budget.py` + `services/dap/metering.py` all extant. R-15(a) TOKENIZED + R-16(a) DERIVATIVE_ONLY: ✅ discharged same wave. | **PARTIALLY-BUILDABLE / MOSTLY-DONE** — R-7/R-15(a)/R-16(a) already discharged; R-6 pricing carrier remains blocked. **Buildable slice**: a **W6 verification note** documenting the extant R-7/R-15(a)/R-16(a) modules and pinning R-6 pricing as the single remaining owner-input. |
| **W7** · WPW Tier-2 draft-on-settle emitter. | WPW Tier-2 draft-on-settle. | WPW R1/R2/R3 (Tier-3 only) · Tier-1/Tier-2 unblocked per WPW-v1-b charter 2026-08-31. | ✅ Tier-1 + Tier-2 ALREADY LANDED: `services/wpw/tier1_notebook.py` + `services/wpw/tier2_report.py` + `services/whitepapers/{draft, router}.py` — from-disk verified. Tier-3 blocked on R1/R2/R3 (§Δ4 §COV owner-desk items). | **EFFECTIVELY DONE for Tier-1+Tier-2** via existing modules. Tier-3 remains BLOCKED-on-<R1/R2/R3>. **Buildable slice**: a **W7 verification note** documenting the Tier-1/Tier-2 emitters and pinning R1/R2/R3 as the Tier-3 gate. |
| **W8** · Release-gate ADMISSIBLE lift (Ruling #5 verdicts). | Ruling #5 sub-verdicts (kdpa_verdict / named_persons_verdict / transfer_basis · biometric_embedding / named_identity / speaker_labeled_audio tier lifts). | Ruling #5 sub-verdicts. | ❌ All three verdicts remain PENDING (banked verbatim in `notes/RULING_LEDGER.md` row 22 · reiterated in every subsequent Release-Gate seal). Standing owner-desk P2. Ratified constraint: current release-gate refuses tiers `{biometric_embedding, named_identity, speaker_labeled_audio}` by default; the LIFT requires Ruling #5. | **BLOCKED-on-<Ruling-#5 sub-verdicts>**. **Buildable slice**: a **W8 verification note** documenting the ratified refusal surface + the exact Ruling #5 sub-verdict shape the owner needs to land (kdpa / named_persons / transfer_basis triple with allowed enum values quoted verbatim from §C.2). |
| **W9** · Owner-ruling A/B/C for audio-bytes-retention (§C.2 Path A/B/C). | Path A · GOVERNED · Path B · POINTER-ONLY · Path C · DEFER (default). | Path C is the default per roadmap §C.2 verbatim: *"Default if no ruling by W2 CP0: Path C."* | ❌ No Path A/B/C ruling landed. Path C default in force. ⚠ Path C `pointer_or_bytes` schema NOT authored on-disk today. `services/governance_plane/retention_policy.py` (RetentionPolicy primitive) exists (W1b CP1) supporting the four regimes but no `corpus-deliverable-audio-segment-bytes` binding is authored. | **PARTIALLY-BUILDABLE under Path C default** · buildable slice: **CP-M7-W9-CONTRACT-1** — author the Path C `pointer_or_bytes` deliverable schema as a shape-frozen dataclass in `services/audio_plane_v1/corpus_deliverable_v1.py` per §C.2 verbatim: *"corpus is `{source-file-pointer, segment_offsets_ms, transcript}` triples. Audio bytes stay on the source estate. `regime=SOURCE_UNTOUCHED` for audio, `regime=DELIVERABLE_GOVERNED` for the manifest."*  Case-agnostic (pointer/offsets/transcript triple is a shape-agnostic carrier). Blocked remainder: Path A/B upgrades (require Ruling #5 landings). |

---

## §2 · Owner-directed buildable dependency order (this shift)

Owner said: *"FIRE whatever is BUILDABLE-NOW or PARTIALLY-BUILDABLE, in dependency order, tests-first, case-agnostic, §3.3 seals."*

**Dependency order (from-disk-honest):**

1. **W9 (Path C default) buildable slice · CP-M7-W9-CONTRACT-1** — corpus-deliverable-v1 `pointer_or_bytes` schema. **DEPENDENCY-FREE.**  This is the schema that unblocks W2 CP2.6 (bundle composition) authoring the deliverable shape without requiring the audio-bytes retention ruling; it also crystallises the Path C default per §C.2 verbatim.

2. **W2 buildable slice · CP-M7-W2-CONTRACT-1** — audio-census scope carrier + `stations_owner_ratified: bool` gate. **Depends on W9 CP-M7-W9-CONTRACT-1** (references the corpus_deliverable_v1 shape as the output_contract target).

3. **W5 verification note** · maps M6 sub-wave 5 + sub-wave 6 CPs to the W5 charter clauses (§5-§7 · Character Register invention layer). No code · no ratchet · analog of M7-verification-walk shape.

4. **W6 verification note** · documents the extant R-7 PILOT_OPEN + R-15(a) TOKENIZED + R-16(a) DERIVATIVE_ONLY discharge modules and pins R-6 pricing as the single remaining owner-input.

5. **W7 verification note** · documents the Tier-1/Tier-2 emitter modules and pins R1/R2/R3 as the Tier-3 gate.

6. **W8 verification note** · documents the ratified refusal surface + Ruling #5 sub-verdict shape.

Waves W3 · W4 remain BLOCKED-on-W2-close-plus-owner-station-selection · no buildable slice this shift.

---

## §3 · Standing-lines discipline held throughout

- **No training on estate audio** — SW-10 stays deferred. Nothing in the buildable slices touches training on estate audio.
- **No biometric material** — CP-M7-W9-CONTRACT-1 explicitly excludes speaker-embedding bytes from the deliverable schema (per §6.2 unrepresentable-by-construction pattern).
- **No enforcement hard-gate** — CP-M7-W2-CONTRACT-1 lands as contract-shell with `stations_owner_ratified: bool = False` gate; no runtime hard-gate; refuses mount only when caller invokes; matches CP-M8-CTCC-1 preventive-charter pattern.
- **No speculative shapes** — every buildable slice cites verbatim canon anchors: W9 cites ROADMAP §C.2 verbatim Path C schema; W2 cites §B.2 + §A.11 JobManifest shape; W5/W6/W7/W8 verification notes cite verbatim charter clauses.

---

## §4 · What starts building this shift (order of fire)

1. **CP-M7-W9-CONTRACT-1** — Path C default `corpus_deliverable_v1` schema (tests-first RED → mechanism → double-green → §3.3 seal · master HEAD SHA discipline). Estimated ratchet delta: +6 invariants (frozen carrier shape + refusal on biometric-bytes payload + release-gate binding + Path-C-default-verbatim-anchor + retention-policy-binding + pure-data-in-out).

2. On W9 close: **CP-M7-W2-CONTRACT-1** — audio-census `scope` sub-carrier + `stations_owner_ratified: bool` gate. Estimated ratchet delta: +6 invariants.

3. **W5/W6/W7/W8 verification notes batch** — 4 verification notes authored on master · no track-a change · no ratchet delta · matches CP-M7-W1-POST-2..POST-8 verification-walk shape.

Each CP boundary fires a GPU utilization interleave check-in per SO §5.

---

## §5 · GPU utilization at triage-completion boundary

- **Elapsed 3.44h · Remaining 68.56h** (last check-in was the batch-close boundary of the §3.3 back-compat wrap-up).
- Both hosts sampler_alive+workload_alive.
- akki-vm: 94 telemetry samples · 410 bench iters (ok=410 across 2 GPUs).
- akki-vm-ii: 88 telemetry samples · 410 bench iters (ok=410 across 2 GPUs).
- Peak GPU util 100% per H200 · peak power ~691-693W · peak temp ~70-71°C.
- 820 total bench artefacts banked.
- Report served at `https://akki-reuse-assess.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.

---

## §6 · Owner-desk items carried unchanged

**P1 (blocking specific waves):**
- JUMP root credential rotation (SEC-15) · unblocks SEC-suspended probes.
- Admin bindings for CD + Visitors (bramuel vs bramwel disambiguation).
- Owner-ratified 3-station selection for W2 · blocks W2 CP2.3..CP2.8 (live audio slice).
- HF token status verification (last known good at W-AUDIO-POC CP-A5).
- NAS credentials for NEWSCLIPS/PROMOS/COMMERCIALS/ADS/video shares · blocks real-audio corpus for D12/M6/W-AUDIO-PROD-MODEL-SELECT.
- Campaign B settlement (adapter.tar.gz + held_out_eval.json pair) · blocks W-TaskEval-v1.

**P2 (chain):** Ruling #5 sub-verdicts (blocks W8) · Path A/B ruling for audio-bytes-retention (blocks W9 upgrades; Path C default in force) · R-6 pricing (blocks W6 full seal) · Amendment 8 · Watch-Learning R-15(b)/R-16(b)/R-17(b) · BC tier selection · DAP R-2/R-3 · Rules-Service R-2 · S-24/27/28/29 · WPW R1/R2/R3 (blocks W7 Tier-3) · SW-10 A.1-A.5.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
