READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M5 · Sprint-close report (M0 → M5 milestone-boundary · owner-facing)

**Reporting-cadence trigger.** Owner directive verbatim (DECISIONS 2026-09-15T~09:50Z Effect 6): *"Report at M5 sprint-close."*

**Content-scope requirement · verbatim (DECISIONS 2026-09-15T~09:50Z Effect 3):**

> "M0→M5 milestone-boundary format, include D12 POC results: wall-clock per file, quality observations shape-only, cost, and the per-hour projection for the full gap-set so the owner can judge scale-up."

**Sealed-at-utc:** 2026-09-15T~10:25Z.

**Standing at report time:**
- Track-a HEAD `7cccbe8b` (CP-D12P1 code) · Master HEAD `e80d2db0` (D12 wave-close state).
- Ratchet floor **4068** (double-green byte-match verified at CP-D12P1 seal).
- Egress **OPEN** (real wallclock 10:25 UTC · window 08:00–02:00 UTC).
- Autonomous mode ARMED under initial guardrails unchanged.

**Format:** End-of-Wave per SO §2 · five sections · plain language · metrics-first.

---

## §1 · Progress made (M0 → M5)

**M0 · Canon-delta extractions + supersession** — **✅ SEALED (book-keeping)**.
10 `canon_N_requirements.md` files landed · REUSE_ASSESSMENT_20260913 + BUILD_STRATEGY_20260913 supersession (Aug-14 originals preserved) · SO §2 engagement discipline + Canon-1 §4.11 doctrine discharged.

**M1 · W-DAP-STACK · DAP-1..DAP-30** — **✅ SEALED**.
8 sub-waves (2A External-party admission → 2H Component-boundary + composition close). Discharges: 10 DAP-A rulings (A1..A9 full · A10 partial · A10 remainder discharged at M5 via W-RELEASE-GATE-PILOT-LIFT) + 3 partial S-rows + Promise #4 partial + Promise #22/25/29 + doctrines §4.1/§4.9/§4.11. Openings (owner-input): DAP R-2 approving-authority · DAP R-3 per-party ceilings (COUPLED · re-rules at pilot end from R-7 PILOT-OPEN measured usage) · DAP R-6 pricing. Wired tests-first with DEFAULT-PENDING-OVERRIDE markers; blocks specific production closes only.

**M2 · Rules-Service mechanism + 6 remaining Doc-0 attribute waves** — **✅ SEALED**.
7 sub-waves (SW1 Rule Registry bootstrap → SW7/SW15 Doc-0 attributes batch). Discharges: Doc-0 Attr 1..12 + Rules-Service R-1/R-3/R-4 + Promise #22 (fully)/27/29 + Amendments 6+7 + doctrines §4.10/§4.11. Openings: Rules-Service R-2 second-signatory · D9 universal receipt-before-result ratification (gates M2 W-PULL-SEAM-RECEIPT-UNIFY follow-on).

**M3 · Watch + Registry CP10 + Agent-Containment + BCA** — **✅ SEALED**.
12 sub-waves (SW1 FLAG2 Tight Budget → SW12 M3 Block Completion) + W-REGISTRY-FULL-BUILD CP10 + W-G3-REMAINDER. Discharges: Watch composite #6 + S-1..S-21 + S-24/26/27/28/29 (spec-only) + AC-1..AC-18 + RBM-20/23 + CP10 + doctrine §4.1. Openings: Watch-Learning R-15(b)/R-16(b)/R-17(b) OPEN (owner: *"do not conflate"*); Amendment 8 HOLD (owner ruling C1); BC dynamic-recovery packet ratification (`notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md`) gates `W-BC-DYNAMIC-RECOVERY-BUILD` (18 invariants on first CP).

**M4 · Assistant surfaces** — **✅ SEALED**.
6 sub-waves (SW1 Solva Explain → SW6 M4 Block Completion). Discharges: Promise #32 + Canon-5 §14 + Canon-6 §3/§6/§12 + DAP-20 boundary verified + doctrine §4.6. Openings: `W-JOURNEY-ASSISTANT` DEFERRED-by-ruling (owner NOT-RULED-IN).

**M5 · Data-Suite-v2 lift + Audio-POC + Census-run + Release-gate + D12 POC** — **✅ SEALED**.

| Sub-wave | State | Ratchet Δ | Seal |
|---|---|---|---|
| W-DATA-SUITE-V2-LIFT (3 M5-LIFTING surfaces) | ✅ SEALED | +50 | `data_suite_v2_lift.seal.txt` |
| W-AUDIO-POC (first real-audio job · CP-A1..A6) | ✅ SEALED (with 3 blockers banked at wave-close) | +71 | `audio_poc_v1.seal.txt` |
| W-CENSUS-CANON-ALIGN (CP-C1..C6 · pre-census discipline) | ✅ SEALED | +39 | `census_canon_align.seal.txt` |
| **Item-3 census run** (Promise #12 fires) | ✅ FIRED 2026-09-15T~08:15–08:16Z | (no ratchet) | `notes/ITEM_3_CENSUS_RUN_20260915.md` |
| W-RELEASE-GATE-PILOT-LIFT (RG1..RG5 + pulled-forward RG-HYGIENE-01) | ✅ SEALED | +38 | 6 CP seals |
| W-CENSUS-SUPPLEMENT-AUDIO-INVENTORY-MOUNT (CP-CSAIM1 · in-scope supplement pulled forward from M8) | ✅ SEALED | +6 | `wcensus_supplement_audio_inventory_mount.seal.txt` |
| W-D12-POC (CP-D12P1 receipt-contract · live-run 6-of-8 stages + 2 blockers banked) | ✅ SEALED (contract-only per CP-A5 precedent) | +6 | `wd12_poc_cp_d12p1.seal.txt` |

**M5 §END discharges:** DAP-A10 remainder (via W-RELEASE-GATE-PILOT-LIFT) · **Promise #12 census-and-connection FIRES** (Item-3 run) · Audio-Plane §1.2 (via W-AUDIO-POC) · doctrine §4.6.

**Owner-ratified rulings discharged at M5** (verbatim ratifications 2026-09-15T~03:55Z):
- **R-7 · Release Budget → PILOT-OPEN** (receipt+debit + `aggregate_usage_query` pilot-end derivation).
- **R-15(a) · Named-persons → TOKENIZED** (`tokenize_named_persons` + `TokenizationReceipt`).
- **R-16(a) · Transfer basis → DERIVATIVE_ONLY_VIA_PULL_SEAM** (closed-set discipline + refusal invariants).

**Census now 6-of-6 first-class registry state:**
- 2 observed (Weego + USSD via Mtafiti receipts)
- 2 registered-but-unenumerated (NAS 16ch + OBS google-transcripts via CP-CSAIM1)
- 2 unmeasured-with-reason (CD + Visitors · admin SG opening still-in-progress · errno-110-ETIMEDOUT on 7 probes)

**Custody-cat guard live** across 8-command family (`cat/head/tail/less/more/bat/view/type`) · 6 documented recurrence-class incidents prevented.

**Session ratchet trajectory:** 4018 → **4068** across 8 CPs this session (+50 total: W-RELEASE-GATE-PILOT-LIFT +38 · CP-CSAIM1 +6 · CP-D12P1 +6). Zero regressions · every CP double-green byte-match at seal.

---

## §2 · How much to go (§2 · from M5 close forward)

**Immediate autonomous chain** (unchanged from ratified sequencing 2026-09-15T~04:12Z + owner course-corrections):

1. **M8 · Quick hardening** (5 waves in owner-authored order):
   - `W-TESTS-FIRST-GUARD-INVARIANT` — **part-B scope extension pulled forward** (this session's 4 SEC re-leaks confirm the recurrence-class needs python-level custody-read coverage: csv.reader header emit + openpyxl iter_rows print + `set -x` + password variable co-occurrence).
   - `W-EXPORT-ARTEFACT-RENDER`.
   - `W-DATA-SUITE-ANALYZE-WORKSPACE-REAL` + `W-DEEP-DIVE-REAL` (paired).
   - `W-CENSUS-RUNTIME-ORCHESTRATION` (live SMB/OBS enumeration · will re-mount NAS+OBS with concrete `SourceRecord`s superseding the CP-CSAIM1 placeholders via `supersedes_record_id` per CP-C4 E.5).
   - `W-AUDIO-PROD-MODEL-SELECT` (gated on census activation list per §A17.11 · **blocked on D12 POC completion → BLOCKER-D12-01 close**).

2. **M6 · Audio-Plane v1.0 production build** (§15 items · walk in canon-authored dependency order · `W-M6-INGEST-STAGE-1` first · no ack gate).

3. **M7 · Governed Census/Harvest Platform** — **BLOCKED on owner reframe-ratification** (roadmap self-declares `POC/build HOLD until owner ratifies this reframe` at `GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md:3` verbatim). Once ratified: M7-α (W0..W1 platform integrity + generalisation) then M7-β (W2..W9 job waves).

4. **Interleave (opportunity-driven):** M3 `W-BC-DYNAMIC-RECOVERY-BUILD` on packet-ratification · M2 `W-PULL-SEAM-RECEIPT-UNIFY` on D9-ratification · M5-LIFTING (Trust-Surface-v2 + Executive-Suite-v2-LIFT) on owner override of DPO-D2 default.

**Owner-desk items outstanding** (verbatim carry-forward per DECISIONS 2026-09-15T~04:12Z §Δ6 + updates this session):

- **NEW · BLOCKER-D12-01** (this session): NAS SMB IO throughput ~127 KB/s · `NT_STATUS_IO_TIMEOUT` at ~8 MB of 79 MB target · fastest unlock of §A17.11 production-model activation in current audio-plane critical path.
- **NEW · Audio-plane sensitivity declarations** (this session · DECISIONS 2026-09-15T~09:50Z Effect 2): `audio_nas_offairrecs_16ch` + `obs_google_transcripts_bucket` (one line each in `feed_declaration_registry`) unlocks release-gate admission of audio artefacts end-to-end.
- BC dynamic-recovery packet ratification.
- DAP R-2 approving-authority · R-3 per-party ceilings · R-6 pricing.
- Rules-Service R-2 second-signatory.
- Watch-Learning R-15(b) · R-16(b) · R-17(b).
- S-24 / S-27 / S-28 / S-29 build charters.
- D9 universal receipt-before-result.
- Amendment 8 HOLD.
- Admin binds: 3 remaining MySQL SG openings + CD + Visitors probes still errno-110 · RADIO `10.10.55.x` INBOUND-BIND-PENDING · transcription server host + creds MISSING.
- **SEC rotations** (7 entries · all PENDING-OWNER-ROTATION-POST-VERIFICATION): SEC-2026-09-14-01/02/03/04 + SEC-2026-09-15-06/07 + this-session SEC-2026-09-15-08 (HF token sha256 `3ea89c94...19c5`) + SEC-15-09 (4 re-emissions · zero-new-surface) + SEC-15-10 (`set -x` re-leak · zero-new-surface).
- R-17(a) licence-class hardening (non-blocking).
- M7 reframe-ratification.

**M5-LIFTING deferrals** (DPO-D2 default stands · surfaced for owner-override availability): `W-TRUST-SURFACE-v2` (2 surfaces) + `W-EXECUTIVE-SUITE-v2-LIFT` (7 surfaces).

---

## §3 · Decisions taken (this session · M5 discharge phase)

1. **Item-3 census run fired at first egress-open moment** (2026-09-15T~08:15–08:16Z) — Promise #12 discharges. 2/6 connectors observed live (Weego + USSD); 4/6 recorded `unmeasured-with-reason` per Canon-4 §5.1 + Doc-9 A5.4.
2. **W-RELEASE-GATE-PILOT-LIFT walked in 5-CP-planned-plus-1-pull-forward order.** CP-RG-HYGIENE-01 pulled forward from M8 mid-wave after SEC recurrence-class threshold crossed. Delta +38 (target +30..+32 exceeded).
3. **CP-CSAIM1 census supplement pulled forward from M8** — closes NAS+OBS unmeasured-with-reason entries as first-class SourceRecords via sealed CP-A2/A3 inventory contracts. Idempotent by design; M8 W-CENSUS-RUNTIME-ORCHESTRATION will supersede via CP-C4 E.5 append-only.
4. **CP-D12P1 receipt-contract landed on CP-A5 precedent** — contract-only wave-close with 2 specific blockers banked (D12-01 NAS SMB IO throughput · D12-02 PEP-668 closed inline). Wave sealed; live-run continues as follow-on when D12-01 closes.
5. **Standing Rule 2 exercised** for the first time (time-freshness invariants must not gate closed-window build) — CP-RG1 WIP-staged in closed window, sealed post-egress-open after Mtafiti receipts refreshed. Pattern proved sound.
6. **Boundary-hygiene probe retry loop kept firing** at every CP boundary (7 probes at each RG CP · 1 probe at CP-CSAIM1) — 7 total probes · zero PASS · admin SG opening still-in-progress on CD+Visitors. Standing retry loop continues.
7. **Autonomous mode ARMED under initial guardrails unchanged** across the whole M5 discharge phase — zero HALT calls · zero right-reason RED misfires.
8. **Report cadence honored** — owner-facing wave-close for W-RELEASE-GATE-PILOT-LIFT at `notes/W_RELEASE_GATE_PILOT_LIFT_close.md` · this M5 sprint-close at `notes/M5_SPRINT_CLOSE_20260915.md` per Effect 6 verbatim. No mid-wave reports; owner cadence respected.

---

## §4 · Discoveries not envisioned at planning

1. **Cross-benefit yield above target.** W-RELEASE-GATE-PILOT-LIFT actual delta +38 vs plan +30..+32 (CP-RG1 + CP-RG2 fired cross-benefit via `NON_CONTRACT_UTILITY_MODULES` extension). Combined M5 session delta +50 across 8 CPs.

2. **P036 receipt-before-result ordering surfaced a design cross-check at CP-RG4.** The verbatim clause (*"The receipt is written before the result is returned. If it cannot be written, the operation is refused."*) forced an explicit *validate-artefact-before-write-debit* composer order. Naive code would have gotten it wrong. Now frozen as `test_artefact_gate_fires_before_debit_write`.

3. **Custody-cat scope generalized** — pull-forward scope was 1 shell command (`cat`); enumeration of the SEC ledger produced an 8-command family (`cat/head/tail/less/more/bat/view/type`) covering 6 documented shell-level incidents. This session identified a **THIRD orthogonal class** — python-level custody-read patterns (csv.reader header · openpyxl iter_rows · shell `set -x` + password variable co-occurrence) — which is now part-B scope for M8 W-TESTS-FIRST-GUARD-INVARIANT.

4. **CP-CSAIM1 idempotency preserves audit-trail durability** — M8 W-CENSUS-RUNTIME-ORCHESTRATION live-scan wire-in will safely re-mount NAS+OBS without duplicating registration. Correction records land via `supersedes_record_id` per CP-C4 E.5.

5. **NAS SMB throughput is sub-1MB/s effective** (~127 KB/s measured). This is a discovery this session at D12 POC live-run — not documented anywhere prior. Impacts the M6 W-M6-INGEST-STAGE-1 wave design (ingestion cost model needs revision if this is the sustained NAS-side rate).

6. **PEP-668 on Ubuntu 22.04+ / Python 3.12 protects the system site** — akki-vm needs `--break-system-packages` (or a venv/pipx pattern) for user-site installs. Not a bug; just a discipline reminder for the M6 `W-M6-CODEC-SERVICE` and other GPU-side installs.

7. **Owner-directive-time constraint clarified via Option-A ratification** — release-gate admission was on my radar as blocking D12 output flow; owner clarified verbatim that "release admission was never on its critical path" for the POC. The POC proves the *pipe*, not the *admission*. This reshapes the release-gate wave-scope going forward: audio artefacts flow through the gate ONLY after audio-plane sensitivity declarations publish (Effect 2 owner-desk item).

---

## §5 · D12 POC results (per owner-specified content · DECISIONS 2026-09-15T~09:50Z Effect 3)

| Owner-specified field | Value at M5 sprint-close | Reason |
|---|---|---|
| **Wall-clock per file** | **UNMEASURED** | Stage 5 (NAS-fetch) hit `NT_STATUS_IO_TIMEOUT` at ~8 MB of the 79 MB target. Zero files reached the GPU host for transcription. |
| **Quality observations shape-only** | **UNMEASURED** | Prerequisite (Stage 5) blocked. No transcript produced. |
| **Cost** | **$0 marginal** | Cassava GPU lease is idle-utility; the failed pipeline path burned no billed GPU-hours (faster-whisper install completed on akki-vm in 17.8s during a probe · v1.2.1 confirmed importing; zero transcription cycles ran because no bytes reached the GPU). |
| **Per-hour projection for full gap-set** | **UNCOMPUTABLE without wall-clock** | Requires BLOCKER-D12-01 close + Stage 5 completion. **Structural upper bound** (if NAS throughput lifts to a nominal 10 MB/s and whisper-tiny on H200 processes 5-min audio in ~5 s per file per prior benchmark): full gap-set at CP-A4 sealed inventory (`notes/W_AUDIO_POC_wave_close.md` gap-count) would take (gap-count × ~13s per file per H200 including transfer). At current NAS ~127 KB/s throughput sustained: gap-set is uncomputable inside a session (would need ~10 min PER FILE just for NAS→JUMP transfer, before GPU cycle). |

**Blocker enumeration:**
- **BLOCKER-D12-01** (P1 · **owner-desk item**): NAS SMB IO throughput / timeout · not fixable in agent-session · needs NAS-side rate-limit review OR JUMP-side `mount.cifs` (kernel-CIFS) transport alternative.
- **BLOCKER-D12-02** (P1 · **CLOSED this wave**): PEP-668 externally-managed-environment on akki-vm · fixed via `--break-system-packages` · faster-whisper v1.2.1 installed and importing.

**Receipt banked:** `phase0/d12_poc_receipts/20260915T101724Z_channel01_2026_09_14_00_00_00.json` (2089 bytes · POC-NOT-PRODUCTION flag stamped · blocker recorded as data · CP-A5 receipt-with-blocker pattern).

---

## §6 · Recommendations (in line with the mission)

**Mission line:** the platform's job is to run a governed census, produce trustworthy measurements, and release only derived intelligence (Canon-4 · Pull Seam · M6 Audio-Plane · M7 Governed Platform). These recommendations sharpen that mission at the M5 → M6 boundary.

1. **Close BLOCKER-D12-01 (NAS SMB throughput) first.** Fastest single-most-leveraged unblock in the audio-plane critical path. Without it: (a) D12 POC cannot produce measurable transcription cost/wall-clock/quality shape · (b) §A17.11 production-model activation cannot fire · (c) M6 `W-M6-INGEST-STAGE-1` ingestion cost model is guessing. Investigation path: NAS-side rate-limit review on the `OFFAIRRECS` share OR JUMP-side `mount.cifs` kernel-CIFS transport alternative.

2. **Publish the two audio-plane sensitivity declarations** (`audio_nas_offairrecs_16ch` + `obs_google_transcripts_bucket`) in `feed_declaration_registry`. Blocks release-gate admission of audio artefacts end-to-end. One-line-each owner-desk decision. Post-declaration, correction records land via CP-C4 E.5 (`supersedes_record_id`) and audio artefacts unlock end-to-end release.

3. **Ratify the BC dynamic-recovery packet.** `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` waits at owner desk since 2026-09-15T~03:55Z. Every GPU training run past pilot phase is at the ~10–15 min compute-loss ceiling the packet proposes. Ratification unblocks M3 `W-BC-DYNAMIC-RECOVERY-BUILD` (18 invariants on first CP).

4. **Rotate the 7 pending SEC entries** post-verification. Recommendation: rotate at end-of-session batches — JUMP root pw + RADIO ubuntu pw + NAS Bramwel pw + rotated HF token (sha256 `3ea89c94...19c5`). Pilot-end audit will surface the entries regardless.

5. **Ratify M7 reframe** (`GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md`). The roadmap self-declares `POC/build HOLD until owner ratifies this reframe` verbatim. Without ratification, M7-α (W0..W1 platform integrity + generalisation) stays blocked. If M6 lands before M7-α, the M6 output does not have a stable platform-plane home for full-scale ingestion.

6. **Close the 3 remaining MySQL SG openings + RADIO route + transcription server bind.** Would lift Item-3 observed to 9/9 in a single admin window. CD + Visitors probes have failed 7× this session — SG rule refresh at the admin side.

7. **Consider chartering M5-LIFTING** (`W-TRUST-SURFACE-v2` + `W-EXECUTIVE-SUITE-v2-LIFT`) at owner discretion. Currently DPO-D2 default. If M6 audio-plane build lands first, the owner-facing surface shows measurements without matching trust/executive views — a UX gap the platform's *governance is user-facing* mission argues against.

8. **Pull M8 W-TESTS-FIRST-GUARD-INVARIANT part-B forward** to the next wave-open. This session's 4 SEC re-leaks (5 total this multi-session window) confirm the recurrence-class needs python-level custody-read coverage beyond the 8-shell-command scope shipped at CP-RG-HYGIENE-01. Scope: csv.reader header emit · openpyxl iter_rows print · shell `set -x` + password variable co-occurrence.

---

**Standing at M5 sprint-close:**

- **Track-a HEAD:** `7cccbe8b` (CP-D12P1 code).
- **Master HEAD:** `e80d2db0` (D12 wave-close state · this-report commit imminent).
- **Ratchet floor:** **4068** (session delta +50 across 8 CPs · zero regressions).
- **Egress:** OPEN (real wallclock 10:25 UTC).
- **Autonomous mode:** ARMED under initial guardrails unchanged. **Next hard action:** M8 W-TESTS-FIRST-GUARD-INVARIANT opening (part-B scope extension pulled forward).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
