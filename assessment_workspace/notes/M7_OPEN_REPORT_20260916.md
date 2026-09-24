READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M7 OPEN · Milestone-boundary note · 2026-09-16T~03:50Z

**Milestone:** 🧭M7 · Governed Census / Harvest Platform (W0..W9 · owner's own reframe).
**Ratification anchor:** DECISIONS.md 2026-09-15T~04:12Z (M6/M7/M8 formal-milestone flip · POC-BUILD-HOLD lifted) + DECISIONS.md 2026-09-16T~03:08Z (SW-10 DEFERRED-TO-CLOSE · M7 OPENS · W-M7-UTILIZATION-72H priority interleave chartered).
**Predecessor:** 🧭M6 · Audio-Plane production build · closed 9/10 sub-waves (SW-1..SW-9 sealed · SW-10 DEFERRED-TO-CLOSE).
**Successor:** 🧭M8 · Hardening + catch-all (owner-authored order).

---

## §A · Owner ruling verbatim (2026-09-16T~03:08Z · via user relay)

> "defer to close. Open m7. as you do this i need to show utilization over the next 3 days (72 hours) can you build a job and comments a run" [read: commence a run].
>
> 1. **SW-10 DEFERRED-TO-CLOSE.** M6 banks at 9/10 sub-waves closed with the SW-10 charter held open (A.1–A.5 unruled). Record in DECISIONS + milestone ledger.
> 2. **M7 OPENS** per the ratified tree (W0 platform integrity → W1 generalisation → W2..W9). Author the M7-open milestone-boundary note + W0 grounding brief, then walk autonomously under all standing guardrails.
> 3. **PRIORITY INTERLEAVE — 72-HOUR GPU UTILIZATION JOB** (owner-facing deliverable, build FIRST, commence immediately) …
> 4. Sequence: utilization job built + launched + URL reported → M7-open note + W0 brief → W0 walk with check-ins interleaved.

**Additional owner ruling verbatim (2026-09-15T~04:12Z · re-grounding · M7 activation):**

> M7 (Governed Census/Harvest Platform W0..W9 — the owner's own reframe; this ratification lifts the roadmap's POC-BUILD-HOLD) …
> Then M7 open: same pattern — reframe-activation note + W0 platform integrity → W1 generalisation → W2+ as unblocked.

## §B · Progress made from M6-open to M7-open

**Ratchet trail (M6 sub-wave close chain):** 4105 → 4134 (SW-1) → 4150 (SW-2) → 4183 (SW-3) → 4213 (SW-4) → 4240 (SW-5) → 4282 (SW-6) → **4288** (CP-SW6-HYG-1 · Redaction Hardening Option 1) → 4318 (SW-7) → 4338 (SW-8) → **4358** (SW-9 close · CP-M6-9-2).

- **9 M6 sub-waves closed** (SW-1 Ingest Stage 1 · SW-2 Dedup Instance-Condition-Map · SW-3 Character Register + §6.3 P100 four-leakage-path lock · SW-4 Codec Service · SW-5 Clustering + Human Validation · SW-6 Objective Wizard + Collection Schema · SW-7 Target Outcome + Planner · SW-8 Calibration + Milestones · SW-9 Commission View).
- **+253 invariants added** across 25 CPs (4358 − 4105 = 253); every CP double-green byte-match at seal; §3.3 3-commit pattern honoured.
- **1 hygiene CP landed** (CP-SW6-HYG-1) discharging SEC incident `sec_incident_jump_cred_leak_20260915T222935Z` with the shape-only `read_custody_metadata` helper + STANDING_ORDERS §4.1 §E amendment.
- **Zero refactor of prior CPs** across the entire M6 walk (verified per-CP in every seal file).
- **Zero SEC re-leak** since custody hygiene close; position-redaction hard-lock preserved across all 60+ boundary probes fired or NOTE-SKIPPED.
- **W-M7-UTILIZATION-72H job LIVE** at 2026-09-16T03:41:28Z (recovery close · 4 bench iterations banked per host in first 3 minutes at ~650 TFLOPS bf16 matmul 8192 sustained per H200 GPU · 97-98% GPU util · report served at `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`).

## §C · How much to go

**Under M7 · Governed Census/Harvest Platform W0..W9:**

| Wave | Class | Status | Anchor |
|---|---|---|---|
| **W0** · Platform integrity fix (silent-success defect) | S-class · PLATFORM | **PRIOR-SEALED 2026-09-13 at ratchet 3282** (SO §3.1 "ALIVE IS NOT DONE" · `output_verified_seal` primitive + 6 code-site refactor · `test_output_verified_seal.py` gates). Under M7 open: **VERIFICATION WALK** to confirm the SO §3.1 contract still holds against current-shift state (no new seal read/write surfaces added since W0 close that bypass the primitive). | ROADMAP §A.12 · SO §3.1 |
| **W1** · Work-supervisor + Resource Registry + Capability Registry generalisation | M-class · PLATFORM | **PRIOR-SEALED 2026-09-13** at CP2b (SO §3.2 "NO RUN WITHOUT A PROGRESS SIGNAL" · `services/work_supervisor/runtime_supervisor.py` · `test_w1_cp2b_runtime_supervisor.py` gates). Under M7 open: **VERIFICATION WALK** identical shape to W0 · confirm SO §3.2 contract still holds · no new dispatch surface bypasses progress ring. | ROADMAP §A.12 · SO §3.2 |
| **W2** · Mount + run vertical slice ONE station (Inooro FM) | L-class · JOB | **BLOCKED-ON-OWNER** (NAS reachability · 3-station selection ratification · RetentionPolicy binding for `corpus-deliverable-audio-segment-bytes` per Path A/B/C · HF token · deps · owner-authorised model install). | ROADMAP §B.3 · §E.2 |
| **W3** · Scale to 3 stations | M-class · JOB | Prerequisites: W2 close + owner-ratified hybrid-ASR routing. | ROADMAP §B.3 |
| **W4** · Scale to 16 stations | L-class · JOB | Prerequisites: W3 close. | ROADMAP §B.3 |
| **W5** · Character Register wave (§5-§7 invention layer) | M-class · JOB | Composes M6 SW-3 (Character Register schema + write/read boundary) + SW-5 (Clustering + human validation) + SW-6 (Objective Wizard + Collection Schema). | ROADMAP §B.3 |
| **W6** · DAP sale surface (R-6/R-7 bindings) | M-class · JOB | Prerequisites: owner rulings on DAP R-6 pricing + R-7 disclosure budget. | ROADMAP §B.3 |
| **W7** · WPW Tier-2 draft-on-settle emitter | M-class · JOB | Prerequisites: `services/wpw/tier2_report.py` (already exists · W-WPW-v1-d) + settle-trigger binding. | ROADMAP §B.3 |
| **W8** · Release-gate ADMISSIBLE lift (Ruling #5 verdicts) | M-class · JOB | Prerequisites: Ruling #5 sub-verdicts (kdpa · named_persons · transfer_basis). CP-RG1..CP-RG5 already sealed via W-RELEASE-GATE-PILOT-LIFT (2026-09-15). | ROADMAP §B.3 |
| **W9** · Owner-ruling A/B/C for audio-bytes-retention | M-class · JOB | Prerequisites: owner ruling on Path A/B/C (see ROADMAP §C.2). Default if no ruling by W2 CP0: Path C (defer). | ROADMAP §B.3 · §C.2 |

**Concurrent priority interleave (NON-M7-numbered):**
- **W-M7-UTILIZATION-72H** · 72-hour GPU utilization deliverable · running from 2026-09-16T03:41:28Z · deadline 2026-09-19T~03:41Z · report served at owner-facing URL · check-in cadence: every M7 CP boundary + at least every few session hours.

## §D · Decisions taken this shift

1. **72h GPU utilization job re-verified from disk**: prior-shift launch was PARTIAL (samplers alive, bench workload dead). Root cause on-disk: `$!` escape bug in `tools/m7_util_72h_orchestrator.py :: launch_detached` (json.dumps-wrapped inner script had `$!` consumed by outer bash parameter expansion). **Recovery**: file-staged launcher.sh approach fixes the escape; killed stale samplers, re-staged payloads, fired fixed launcher. Both hosts now confirmed `sampler_alive`+`workload_alive` with real bench iterations landing. Full diagnosis + fix at `notes/M7_UTIL_72H_LAUNCH_RECOVERY_20260916.md`.
2. **SEC probe-halt reading amended** for the utilization job initiation per owner ruling 2026-09-16T~03:08Z verbatim; boundary probes remain NOTE-SKIPPED for CP-boundary purposes pending JUMP custody rotation.
3. **M7 W0 walk scoped as VERIFICATION WALK** (not re-build): the platform-integrity primitives (SO §3.1 `output_verified_seal` + SO §3.2 `runtime_supervisor`) were sealed 2026-09-13; M7's W0 walk verifies from-disk that no new seal read/write or dispatch surface has been added since W0 close that bypasses those primitives. If drift is discovered, CP-M7-W0-1..N author tests-first RED → mechanism → double-green → seal → §3.3 3-commit. If no drift, W0 closes as a verification receipt with no ratchet delta.

## §E · Discoveries not envisioned at planning

1. **Case-agnostic launcher escape idiom** (documented as a pattern for future SSH-detach flows): base64-decode to file + `setsid nohup bash file.sh </dev/null >/dev/null 2>&1 & disown` is preferable to `json.dumps(inner)` + `bash -c` when the inner script references shell parameters that must survive outer-shell expansion.
2. **Sampler resilience proved**: the prior-shift sampler.sh ran for ~11 minutes and wrote 14 correct telemetry rows across both hosts despite the launcher's escape bug — the `while [ $now -lt $end ]; do nvidia-smi ... sleep 300; done` pattern in `m7_util_72h_sampler.sh` is robust to launcher bugs so long as the sampler itself starts. This validates the "sampler and workload as two independent detached processes" architecture over a single monolithic wrapper.

## §F · Recommendations to make the experience better, in line with the mission

1. **W0 verification walk deliverable** (this-shift): produce a short receipt `phase0/m7_w0_verification/verification_receipt_20260916.json` cataloguing every seal read/write site currently in the codebase (from `grep -Rn "ACTIVITY_SUMMARY\.md\|_is_sealed\|_has_sealing_marker\|is_real_seal\|parse_seal\|output_verified_seal" services/`) and confirming each routes through the primitive. If any site is off-primitive, author CP-M7-W0-1 to route it through; else close W0 with a zero-delta verification seal.
2. **W1 verification walk** identical shape (SO §3.2 primitive coverage · every dispatch surface bound to progress ring).
3. **W2 mount preparation** during any owner-blocked window: pre-author the JobManifest v1 (single station: Inooro FM) as a config file so that when NAS reachability + HF token + owner-ratified 3-station selection land together, W2 CP1 (Mount) is a one-line commit.
4. **GPU utilization check-in cadence** interleaved with every M7 CP: `python3 tools/m7_util_72h_orchestrator.py check_in` at every CP open + close during the M7 walk. Owner's report URL always reflects the last sync.

---

## §G · Wave-honest limits at M7 open

- **W0/W1 platform waves were closed BEFORE the M7-formal ratification**: they carry SO §3.1 and §3.2 as their durable output. The M7 W0/W1 walks are VERIFICATION WALKS (from-disk parse-not-paraphrase) — not re-builds. If verification uncovers drift, that drift is a first-class M7 CP (tests-first, ratchet-monotonic, seal + 3-commit). If verification is clean, W0 and W1 close as zero-delta verification receipts.
- **Concurrent utilization job is NOT an M7 CP**: it's a priority interleave that runs alongside the M7 walk. Its receipts land under `phase0/gpu_utilization_72h/` and are banked at every check-in; they do not enter the ratchet unless a test invariant is added to enforce launcher-idiom safety (candidate CP for W0 if drift is discovered in the launcher).
- **Owner-desk items outstanding** (from M6-close binding · SO §2 cadence): JUMP custody rotation · CD + Visitors admin binds · Amendment 8 · Watch-Learning R-15(b)/16(b)/17(b) · BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · S-24/S-27/S-28/S-29 build charters · D9 receipt-unify · SEC rotations · R-17(a) (non-blocking) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine · SW-10 A.1–A.5 rulings (blocks W-M6-10-* if ever un-deferred).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
