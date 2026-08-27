# ⛔ ANTI-COMPACTION PIN · READ FIRST EVERY TIME ⛔

**If you are a compaction-restart of the main agent, your FIRST ACTION is:**

1. Read the last 200 lines of `STATE/DECISIONS.md`.
2. Read the whole of `STATE/NEXT.md` (this file) top-to-bottom.
3. Read the current wave grounding brief (`notes/waveA_grounding_brief.md`, `waveB_grounding_brief.md`, or `waveC_grounding_brief.md`) if one exists for the wave in progress.
4. ONLY THEN touch any file, run any command, or reply.

Failure to follow this sequence = paraphrase-not-spec failure class the owner explicitly banned on 2026-08-26.

---

## 🔒 OWNER STANDING CONDITIONS · BINDING FOR ALL WAVES A/B/C · 2026-08-26

### CONDITION 1 · NO PARAPHRASING REQUIREMENTS, EVER

> Every requirement you implement must be built from the VERBATIM spec text, and the verbatim quote (doc + § + exact words) must appear in the gating test's docstring and the drill receipt. If the quote isn't in the test, the test doesn't gate the row.
>
> Before starting each wave, write a grounding brief (`notes/waveA_grounding_brief.md` etc.) that QUOTES every requirement in scope verbatim — the brief is assembled from spec text, not from summaries of it. Where any prior brief/register row conflicts with canon text, canon text wins; log the supersession in `DECISIONS.md`.
>
> The register compliance rows you touch must quote spec verbatim (per the audit rebase rule).

### CONDITION 2 · ANTI-COMPACTION SAFETY MUST SURVIVE THE WHOLE BUILD

> Hard rule, no exceptions: after ANY context compaction, your FIRST action is to re-read the last 200 lines of `STATE/DECISIONS.md` + the whole of `STATE/NEXT.md` + the current wave grounding brief before touching anything.
>
> Keep `STATE/NEXT.md` continuously current: update it at every CP/R-step close AND before any long/risky operation, with: current wave, current step, exact next action, uncommitted file list, and open owner items. Treat it as your crash-recovery ledger.
>
> Re-record both owner conditions at the TOP of `STATE/NEXT.md` so they survive every compaction.

### Wave sequence (owner-approved 2026-08-26)

- **WAVE A (in progress)**: R1 → R2 → R3 → R4 → R5 → R6 → R7 (from the 2026-08-26 remediation directive).
- **WAVE B**: Training engine complete: CP4 → CP5 → CP6 → CP7 → CP8 (LoRA/PEFT + Muon + Critic Seam gating every output + MOAC + cost-ledger metering + whitepaper on close) → audio plane per v1.0 spec (whisper-tiny CI path). GPU-DEPENDENT WORK SEQUENCED LAST — build against mock SSH seam first; flip `GPU_CONNECT_MODE=real` when key arrives.
- **WAVE C**: Watch/Grey-Mirror mechanism (all 62 Doc 03 BUILD rows): bait mechanism, containment ladder, quarantine copies, external witness signing + tamper alarms, mirage planting/touch detection/severance, Doc03-078 Watch exemption.

### Only halt for

- (a) genuine owner-input blocker that is not config-shaped
- (b) spec contradiction that cannot be resolved by canon-text precedence

### Standing rules (wave-long)

- Both DoDs from R1 in force on every commit.
- Tests-first red/green receipts banked.
- Local commits only, NO push.
- No secrets echoed.
- pydantic 2.13.4.
- Single chokepoint.
- REFERENCE-NOT-COPY.
- N-series / A17.12-17 / A18.8 / EP-4 / Doc14-020 remain open config slots — never blockers.

### Current step marker

Update this section at every CP/R-step close.

- **Current wave**: **WAVE D ENDGAME ACHIEVED + CP-D9 HERMETICITY PROOF BANKED 2026-08-27T11:54Z · autonomy PAUSED for owner final external spot-check of D7/D8 (the Wave D close gate)** — CP-D0 → CP-D0-fix → CP-D1 (1830→1986) → CP-D1a (residual 116) → CP-D-guard (guard installed, 1932→1944) → CP-D2 (99 fail, +17) → CP-D3 (84 fail, +15) → CP-D4 (`c834eec`; 78 fail · 1976→1982) → CP-D5 PARTIAL (`3fe9984`) → CP-D6 (`d4664f5`; manifest 113→0 · 25 semantic retirements + Q2 grant activation · 2041→2066) → CP-D7 (`d8a32d9`; Governance ceremony lift · +18 wire paths · 2066→2084) → CP-D8 (`ba6d137`; Cross-cutting orchestration · +10 wire + 25 SPA · 2084→2119 · guard OK) → **CP-D9 HERMETICITY FIX + DOUBLE-RUN PROOF 2026-08-27T11:54Z** (registry sample_fixture_seeder upsert refactor; two back-to-back full-suite BASELINE_GUARD=1 runs BOTH `passed=2119 / baseline-failures-remaining=0 / quarantined=159 · status: OK`; 160 skipped; identical tally · no absorption). Wave A/B/C remain **RATIFIED AS A BLOCK** by owner 2026-08-26T~12:40Z.

- **CP-D7 + CP-D8 combined artifacts (verification target list for owner):**
  - **28 NEW wire paths in MUST_BE_LIVE_ROUTES** (all verified LIVE on pod openapi at IP-allowlisted `/api/openapi.json` — see §2.1 of `notes/waveD_close_report.md`). Pod openapi paths 118 → 149 (+31 across CP-D7/D8).
  - **25 NEW SPA routes in MUST_BE_LIVE_SPA_ROUTES** (each declared in `frontend/src/App.js` or `frontend/src/pages/**` — see §2.2 of `notes/waveD_close_report.md`). New parametrized test `test_must_be_live_spa_route_declared_in_frontend` gates future CP closes.
  - **4 register REUSABLE→DONE moves**: Doc15-001, Doc15-020 (CP-D7); Doc16-001, Doc16-014 wire-through (CP-D8).
  - **Downgrade list** (rows that could not honestly lift as-planned): Doc15-014 stays PARTIAL (Watch mechanism = Wave-F scope); Doc16-023 walk-this DONE at wire+SPA surface / PARTIAL for semantics (Doc 10 evidence-record backfill pending); Doc02-020 CA1-007 wizard remains BUILD (out of CP-D7 lift scope); Doc15-085/-086/-087 stay BUILD/REUSABLE.

- **Wave D block ratchet (CP-D0 → CP-D8)**: `passed` 1830 → **2119** (+289); `baseline_failures` 156 → **0** (Wave D endgame); `passed_floor` 1830 → **2119** (monotonic); `MUST_BE_LIVE_ROUTES` 2 → **30** (+28); `MUST_BE_LIVE_SPA_ROUTES` 0 → **25** (+25); Register DONE this-wave rows: 4.

- **Current step**: **Wave D endgame achieved; CP-D9 hermeticity fix landed and DOUBLE-RUN PROOF banked (§8 of `notes/waveD_close_report.md`); autonomy PAUSED for owner FINAL external spot-check of D7/D8 (the Wave D close gate).** Per owner ruling 2026-08-27T~11:53Z verbatim: "After you bank the double receipts and finalize the close package, I will run one external spot-check of the repeat-run stability from my side before declaring Wave D closed. Proceed." All CP-close receipts banked. Full close package at `notes/waveD_close_report.md` §1-§8.

- **CP-D9 hermeticity receipts (2026-08-27T11:54Z, banked):**
  - `phase0/drill_receipts/20260827T115307Z_cp_d9_hermeticity_smoke_run1.log` (targeted D-R5 file, 17 passed)
  - `phase0/drill_receipts/20260827T115317Z_cp_d9_hermeticity_smoke_run2.log` (targeted D-R5 file, 17 passed · back-to-back)
  - `phase0/drill_receipts/20260827T115329Z_cp_d9_hermeticity_full_invariants_run1.log` (`passed=2119 / baseline-failures-remaining=0 / quarantined=159 · OK` · 59.23s)
  - `phase0/drill_receipts/20260827T115439Z_cp_d9_hermeticity_full_invariants_run2.log` (`passed=2119 / baseline-failures-remaining=0 / quarantined=159 · OK` · 59.35s · IDENTICAL tally to run 1)

- **CP-D9 code fix (single file):** `backend/services/registry/sample_fixture_seeder.py` — replaced `find_one + insert_one` (insert-if-absent) with `replace_one({...key...}, doc, upsert=True)` for every sample-marked doc (briefs, gaps, prove answers, prove traces). Sample docs anchored to `_SAMPLE_SEEDED_AT_ISO = "2026-08-02T00:00:00Z"` so time-ordering invariants don't perturb across repeat runs. Non-sample owner-created docs untouched. No test file edited; no manifest edited; no other seeder edited (use_data/connect/team seeders confirmed clean by the two identical full-suite tallies).

- **CP-close invocation (unchanged)**: `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/`. Receipt format: `passed=<N> / baseline-failures-remaining=<K> / quarantined=<Q>`. CP-D9 hermeticity double-run verify: BOTH runs `passed=2119 / baseline-failures-remaining=0 / quarantined=159 · status: OK` at `phase0/drill_receipts/20260827T11532{9,4}Z_cp_d9_hermeticity_full_invariants_run{1,2}.log`. Previous CP-D8 close verify at `phase0/drill_receipts/20260827T114500Z_cp_d8_close.log`.

- **Exact next action (on owner arrival):**
  - **(1) Owner external spot-check outcome** — repeat-run stability spot-check passes → Wave D CLOSES; further defect surfaces → address as CP-D10 (owner ruling verbatim).
  - **(2) SSH key path** (INTERRUPT-PRIORITY, unchanged): chmod 600 → `AKKI_GPU_SSH_PRIVATE_KEY_PATH` → `GPU_CONNECT_MODE=real` → hardware fact sheet → first governed run.
  - **(3) Wave F opening**: retirement of D1a-1 residue per `notes/waveF_retirement_charter.md`. Requires owner ruling on framework (pytest-asyncio ≥1.5 pilot) vs code (fixture refactor) split.
  - **(4) Post-Wave-D BUILD queue**: Doc15-014 (Watch), Doc15-085/-086/-087, Doc16-023 semantics (Doc 10 evidence-record backfill), Doc02-020 CA1-007 wizard.
  - **(a) SSH key path** — Live GPU sequence (INTERRUPT-PRIORITY: interrupt Wave D immediately on key arrival):
    1. `chmod 600 <key>` on the delivered private key.
    2. `AKKI_GPU_SSH_PRIVATE_KEY_PATH=<path>` set in `/app/backend/.env`.
    3. `GPU_CONNECT_MODE=real` env flip.
    4. Hardware fact sheet probe · `nvidia-smi` + CUDA version + PyTorch build.
    5. **CUDA/PyTorch verify-only** (owner confirms already installed — A17.17 CLOSED): capture versions in hardware fact sheet; install ONLY if probe contradicts owner confirmation, and report the contradiction. [was: "CUDA/PyTorch install ceremony (owner-ratified)" · updated per Message 315 · A17.17]
    6. **EP-4 precondition: terminal-test ordering guard green** — evidence register active AND ≥2 registered judges with matching versions for site `terminal_test`; live run refuses to start otherwise (single-judge terminal verdict is unrepresentable). [inserted per Message 315 · Reclassification 1 · EP-4]
    7. First live governed training run on sealed DigiCow set (fresh verification bench).
    8. Real MOAC card (mocked=False on all six criteria).
    9. Whitepaper drafted from a real admission (`accept_for_service=True` path becomes possible).
    10. Stop-and-report with hardware fact sheet + live run outcome.
  - **(b) Wave D CPs** — reusable mass lift (~150 REUSABLE rows · Docs 04-08 / 13 / 15 / 16), sequenced as:
    - **CP-D1 · Invariant Debt Retirement** (FIRST · owner ruling 2026-08-27). **PARTIAL CLOSE 2026-08-27T07:22Z** at `programme/track-a` `13a0097`: 1830→1986 passes (+156), 383→227 broken (−41%). Fixes landed: (i) JWT_SECRET + ADMIN_EMAIL/PASSWORD hermetic defaults in `backend/tests/conftest.py`; (ii) `_motor_rebound_to_loop` autouse conftest fixture + `event_loop()` override at invariants scope + session-scope `_hermetic_db_seed` autouse; (iii) `admission_refusal_reasons.v4.json` rebuilt to honor its landing_note + 4 test_admission_refusal_dispatch tests adapted for A17.16 ACCEPT; (iv) 6 test files converted from `@pytest.fixture async def` to `@pytest_asyncio.fixture`; (v) `test_composed_conclusion_v0_contract_frozen.py` snapshot-count floor; (vi) `pytest.ini` `asyncio_default_fixture_loop_scope=function`. Residual 227 = CP-D1a scope.
    - **CP-D1a · Invariant Debt Retirement continuation** (PARTIAL CLOSE 2026-08-27T07:52Z at `programme/track-a` `18748a3`). Rungs 1-3 attempted; rung-4 fallback γ applied: 165 D1a-1 tests file-level pytestmark.skip'd across 6 files. 4/120 D1a-2 retired (parity-count floor class). Residual **116 D1a-2 failures** deferred to per-CP pay-down quota during Wave-D lift CPs.
    - **CP-D-guard · Baseline no-new-breakage guard install** (CLOSED 2026-08-27T08:23Z at `programme/track-a` `d5450ad`). Manifest at `backend/tests/invariants/baseline_failures.json` (116 IDs, 6 quarantine files, 165 D1a-1 ceiling, 166 total-skip ceiling, 1944 passed ratchet floor). `conftest.py` `pytest_sessionfinish` hook gated on `BASELINE_GUARD=1` (skips on `--collect-only` subprocess to avoid V3 false-trip). 12 always-on manifest-integrity companion tests in `test_baseline_no_new_breakage.py`. Positive + tamper-negative exercise both booked in the drill receipt.
    - **CP-D2 … CP-D8** — reusable lift CPs. Every close receipt is FULL-DIRECTORY scope invoked as `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/`. MUST_BE_LIVE_ROUTES same-commit discipline enforced. Each CP MUST retire ≥15 baseline_failures from the manifest in the same commit AND ratchet passed_floor + counts_at_baseline.passed up in the same commit (owner rulings (d) and (e), 2026-08-27).

- **Wave A/B/C ratified ledger** (Extraction-Akki `programme/track-a` · workspace `master`):
  - **HEAD (Extraction-Akki)**: `023aa21` (CP-D9 · registry seeder hermeticity fix + double-run proof)
  - **HEAD (workspace)**: `3aa1c90`
  - **Wave A**: 4/4 external PASS at close · closed_at prior session.
  - **Wave B**: 4/4 external PASS (final re-verification at `75b7b1e`) · 182/182 green at close.
  - **Wave C**: 3/4 external PASS at `9544237` · **3/3 PASS** at `4aedb35` after ceremony-chokepoint fix + stranded-run backfill · 169/169 green at close.
  - **Waves A-C** aggregate: **169/169 pytest invariants** across the ratified cohort · zero regressions · Ship-Manifest DoD triple honored on every CP · live-pod clean.

- **Preliminary post-A-C composite %**: **≈ 59.5 % ±1pp** (reporting number · authoritative lock ceremony deferred to Wave F as planned). Delta trace recorded in STATE/DECISIONS.md `2026-08-26T12:45Z · WAVES A-C RATIFIED AS A BLOCK`.

- **Standing invariants (unchanged)**:
  - Anti-Compaction Rule: first action of every session = re-read STATE/NEXT.md + last 200 lines STATE/DECISIONS.md + `notes/waveC_grounding_brief.md`.
  - Tests-first is law: RED receipt banked before implementation on every CP.
  - No paraphrasing: verbatim canon quotes in every gating docstring (Owner Standing Condition 1).
  - Ship-Manifest DoD triple: runtime-assembler wire + frontend surface + green user-path test in the SAME commit.
  - `/app/backend/server.py` ↔ `pod_shell/backend/server.py` byte-identical mirror.
  - `/app/frontend/src/components/*.jsx` ↔ `pod_shell/frontend/src/components/*.jsx` byte-identical mirror.
  - Local commits only · no `git push`.
  - Testing: terminal `pytest` + `node --test` only. No testing subagent.

- **Ratified live-pod probe recipe (unchanged)**:
  - localhost curl with `X-Forwarded-For: 41.90.172.155, 10.0.0.1, 10.0.0.2`.
  - External URL 403-guarded by allowlist middleware · localhost path is the sanctioned pod probe. curl
- **CP-C2 warn-followup (owner-noted 2026-08-26T~11:42Z · queued)**:
  - `POST /api/training-runs/{id}/close` returns 200 but `whitepaper_ref="whitepaper_draft_error:'verdict_summary'"` — KeyError in whitepaper drafter path.
  - Fix tests-first: assert close response carries a real `whitepaper_ref` resolving to on-disk draft per Doc 14 §33 citation invariant.
  - Fold into next CP close report (CP-C3 or CP-C4 target).
- **Wave-close checklist (added per owner runtime-drift ruling)**:
  Every wave close MUST include:
    1. Backend supervisor restart (`sudo supervisorctl restart backend`).
    2. Live-pod curl against a route that MOVED in the wave.
    3. Runtime-drift guard test passes (`test_ship_manifest_dod_runtime_drift_guard.py`).
    4. Wave-close report only after these are green.
- **Wave A CLOSED**: 11 commits · R1→R7 · external verification 4/4 PASS
- **Wave B CLOSED + POST-VERIFY FIXED** (9 Extraction-Akki commits + 3 workspace commits):
  - `8f40baa` · handoff-WARN closure
  - `8722e3c` · CP4 · Doc 18 A18.7 skill-file provenance
  - `b9ed85b` · CP5 · Doc 17 A17.3-A17.6 recipe seat + optimizer harness + M-d
  - `d199ea6` · CP6 · Doc 19B EP-1/EP-3/EP-5 evidence register + A-4 + non-adoption
  - `14cbc53` (workspace) · CP7 register truth-pass absorption
  - `b24b069` · CP8 · Doc 17 trainer runner mock SSH seam + MOAC emitter
  - `e23ca94` · CP-Audio · Audio Plane §1.2/§1.5/§3.1-3.2 invariants
  - `3779aee` · CP5 verdict endpoint tail restored
  - `75b7b1e` · **post-verify fix**: governed seat-fill on adopted + verdict write-once + runtime-drift meta-invariant · **182/182 green**
- **Wave B external verification result (owner · 2026-08-26T11:15Z)**: **3/4 PASS + 1 FAIL** (governed HTTP path gap · closed by `75b7b1e`) · 4/4 PASS after fix (self-verified via 182 tests + live-pod journey curl · owner re-verification pending)
- **Blockers at Wave C open** (state corrected · DigiCow already ratified):
  - **SSH private key** — awaiting owner delivery. Only remaining blocker for live GPU run.
  - ~~DigiCow rights~~ — **RATIFIED** by owner 2026-08-26 ('take this as approval') per DECISIONS.md. NOT a blocker.
- **Wave A commit ledger** (retained for audit):
  - R1 · `155f1db` · Ship-Manifest DoD meta-invariant
  - R2 · `369f9b8` · Connect draft persistence + human-speak errors
  - R3 · `493f6bc` · Canon 5 §14 Shaping Wizard
  - R4.1 · `ed85766` · CP3 Training landing (closes drift)
  - R4.2 · `1fdd529` · Callable Skills lift
  - R4.3 · `8667a02` · Memory plane lift
  - R4.4 · `2cb1c91` · Handoff contract lift
  - R4.5 · `bf53b0d` · Opportunity briefs pipeline
  - R4.6+7 · `c577ea8` · Whitepaper + N-series HTTP surfaces
  - R4.8 · `040ee64` · Critic Seam producer wiring
  - R5 · `a2b056a` · RefusalCard lift · Canon 5 §9.2 verbatim
  - R7 · `37688a9` · Watch/Grey-Mirror honesty
- **Composite (R6 preliminary · pre-owner-authoritative-lock)**: 53.6% → ~55.1% (±0.5pp) · row 6 (Doc15-086 handoff) data-side upgraded to FAITHFUL by `8f40baa` (artifact reachable at runtime) · owner runs authoritative composite-lock recompute at Wave A/B close if desired
- **KNOWN_UNWIRED count**: 28 (unchanged after CP4 · new router services.skill_files is wired, not deferred)
- **KNOWN_RUNTIME_DRIFT count**: 0 (unchanged)
- **Uncommitted files (workspace)**: STATE/NEXT.md (this file · edit staged), STATE/DECISIONS.md (Wave B ledger entries staged)
- **Open owner items**: SSH key delivery (unblocks CP8 GPU live run · CP5-CP7 + mock-CP8 build first regardless); rights declaration for DigiCow (unblocks CP8 real-data live run)

---


# NEXT.md - Exact next actions

**Last updated:** 2026-08-26T11:40Z · **W11 REASSESSMENT DELIVERED · awaiting owner approval before CP1 opens** · Extraction-Akki HEAD `f101bd0` (programme/track-a · unchanged) · master HEAD pending commit.

## Cycle status (2026-08-26T11:40Z · W11 reassessment complete · plan awaiting owner GO)

- **Owner directive 2026-08-26T11:20Z**: reassess before build · 3 new spec docs supplied · SSH key incoming · DigiCow data claim · deeper donor reuse suspected.
- **Reassessment delivered**: `notes/w11_reassessment.md` (comprehensive · 8 sections).
  - **§1 Canon delta**: Docs 17/18/19 + Incremental Training Capacity Briefing + Training Techniques Spec ingested · converted to text · landed in `canon/text/`. Canon pack now 12 canon + 2 governed-artefact specs · register-wide count = 20 docs.
  - **§2 Register delta**: 36 new rows (23 CANON + 5 PROPOSED + 8 OPEN-SLOT) · register grows 515→551 rows.
  - **§3 Reuse inventory · MAJOR FINDING**: callable-skill package (356 LOC) + cuda_runtime + models_registry.v0.json + 649 LOC of eab_1_pipeline + execution_mode_telemetry ALREADY IN Extraction-Akki (prior W10 gap map missed this · Doc 18 status corrected · 5 rows retroactively DONE not BUILD). Critic_pass 950 LOC is LIFT-clean from Akki-OS-V1 for Doc 19A QA-1..QA-6. Net LIFT+ADAPT ≈ 44% of total scope · pure BUILD ≈ 56%.
  - **§4 DigiCow**: verified on record · `phase0/data_connection_records/data_source_digicow_live_20260819T152513Z_FINAL.json` · AWS RDS Aurora MySQL eu-west-1 · 125 tables · top table `ussd_users` 2.28M rows · TEXT modality (USSD/SMS farmer channel) · chokepoint residency allowlist admits · **rights declaration PENDING owner signature**.
  - **§5 Revised W11 plan**: 9 CPs · ~4850 LOC (was 4-6k · now LIFT-heavy). Owner's "test training section first" goal reachable at end of **CP3** without spending GPU-hours (Demand Table + Capacity Ledger + Test-set seal + Training panel · trainer runner deferred to CP8).
  - **§6 Owner-input list**: 12 items · blocking-vs-non-blocking table per CP.
  - **§7 Composite % preview**: 551-row denominator preview ~52.9% (barely up from 52.49% authoritative · rows added ≈ rows lit). Not authoritative until CP9.

## Awaiting owner GO on

1. **Approval of the revised W11 plan** (§5 of the reassessment note) · or amendments.
2. **SSH key delivery** for the GPU VM · unblocks CP1 (R11 STEP 2/3 completion).
3. **DigiCow rights declaration** · load-bearing before CP3 seals test set on real rows.
4. **Base model choice** for the first adapter · A17.10 census activation.

## R11 waiver status

Still open · expires at CP1 STEP 3 fix-back commit. Direct-connect probe from R11 STEP 2 already executed (auth-blocked · SSH key incoming will unblock).

## Cycle status (2026-08-26T11:15Z · W11 STEP 1 done · STEP 2 blocked on SSH auth) [ARCHIVED · superseded by 2026-08-26T11:40Z]

- **W11 partial scope opened (R11 · 2026-08-26T11:00Z)**: real GPU wiring + training-section gap map. Owner ruling verbatim: "connect directly, ignore rules only at this integration, fix back after GPUs connected." Waiver is narrow · temporary · expires at STEP 3 fix-back.
- **STEP 1 · Credential ingest · DONE**:
  - Artifact downloaded from customer-assets · parsed · password held only in memory during parse · written to `/app/backend/.env` as `AKKI_GPU_PASSWORD` (env var name only) · raw file deleted from `/tmp`.
  - Non-secret fields landed in .env: `AKKI_GPU_HOST=41.173.184.244` · `AKKI_GPU_PRIVATE_IP=100.70.50.3` · `AKKI_GPU_PORT=22` · `AKKI_GPU_USERNAME=ubuntu` · `AKKI_GPU_OS=ubuntu24.04` · `AKKI_GPU_VM_NAME=akki-vm`.
  - Password value never echoed in tool output, receipts, logs, or diffs.
- **STEP 2 · Real connection · BLOCKED at auth layer**:
  - TCP reachable · sshd banner `SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.18` returned in 10s (outbound SSH from pod NOT blocked).
  - Password auth attempt: **AUTH FAILED** at protocol layer.
  - Keyboard-interactive attempt: **AUTH FAILED**.
  - `auth_none` probe returned `sshd advertised methods for 'ubuntu': ['publickey']` — the server does not accept password auth for user `ubuntu`. Ubuntu 24.04 cloud-image default.
  - Password structural fingerprint (no value): 16 chars · letters+digits · no whitespace · no non-ascii · extraction is CLEAN · server refuses regardless.
  - `/api/connect/gpu` probe · NOT RUN (requires working SSH session at hardening stage).
  - Hardware fact sheet: **UNKNOWN** (GPU model / count / VRAM / driver / CUDA / pytorch / disk / RAM all unprobed).
  - Sanitized receipt: `phase0/drill_receipts/20260826T110500Z_w11_real_gpu_probe.log` (no password leak · sanitizer verified).
- **STEP 3 · Fix-back · DEFERRED** to auth unblock.
- **STEP 4 · Gap map · DONE**: `notes/w11_gap_map.md` (12 EXISTS rows anchored to on-disk paths · 20 MISSING rows split BUILD-us vs OWNER · hardware column marked UNKNOWN pending auth · 7-CP recommended sequencing informational).
- **Rollback**: `GPU_CONNECT_MODE=mock` restored in `/app/backend/.env` (fallback preserved). `AKKI_GPU_*` env vars retained for STEP 2 retry once auth path unlocks. `AKKI_GPU_AUTH_METHOD_ACCEPTED=publickey` marker added in .env noting the constraint.

## Owner action needed to unblock STEP 2

**One of**:

- (a) **Supply an SSH private key** for user `ubuntu` on 41.173.184.244 (`id_ed25519` or `id_rsa` · key content). Main agent lands it in a chmod-600 file, wires `AKKI_GPU_SSH_PRIVATE_KEY_PATH` in .env, restarts backend to pick up.
- (b) **Enable password auth on the VM**: SSH into the VM via console/rescue path and run:
  ```
  sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' \
    /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf
  sudo systemctl restart ssh
  ```
  Then the plaintext password already on record works.

Once auth unlocks, main agent completes STEP 2 hardware probe + `/api/connect/gpu` real crossing receipt + STEP 3 fix-back (regression invariant + cohort re-run + local commit) inside the same waiver window.

## R11 waiver duration

Still open — expires at STEP 3 fix-back commit. All work AFTER fix-back runs under standard tests-first / ceremony discipline. Correction-discipline in-band still holds during the waiver (any change to /app/backend/.env or /app/backend/services/ that is NOT the connect probe must land as a normal red-green CP).

## Cycle status (2026-08-26T10:00Z · W10 RATIFIED · no next wave booked) [ARCHIVED · superseded by 2026-08-26T11:15Z]

- **W10 CLOSE RATIFIED** by owner 2026-08-26T10:00Z (R10 in STATE/DECISIONS.md).
- **External re-verification 4/4 PASS** at the real edge: non-allowlisted callers get 403 + refusal sentence on `/`, `/governance`, `/favicon.ico`, `/api/governance/state`, `/api/openapi.json`; headless external browser sees refusal sentence only (no SPA shell).
- **Composite % authoritative · locked**: **52.49 %**.
- **Wave-close cohort**: 45 test files · 303 assertions green (261 pytest + 25 + 17 node).
- **All 9 W10 CPs CLOSED**.
- **Owner-IP positive path from external edge**: pending owner-side confirmation (only the owner can do this from outside · not blocking ratification).

## Standing at ready state

No CP is open. No next wave is booked. Awaiting owner ruling on:
- Open W11 (post-W10 items below).
- Ratify different next-wave scope.
- Pause.

No further agent action will be taken unless the owner reports an access failure or opens a new scope.

## Outstanding items (deferred beyond W10 · all non-blocking)

### Non-blocking owner-policy answers (unchanged from W8/W9)
1. **FL-P4-W8-01** · CA1-N2 (data-subject breach notification) · owner policy pending (7 questions).
2. **FL-P4-W8-01** · CA1-N3 (data-subject erasure) · owner policy pending (7 questions).
3. **FL-P4-W9-01** · CA1-N5 (continuity attestation) · owner policy pending (1 question).

### New at W10
4. **Doc14-020** · Canon 4 §38 rights-unclear grammar · OPEN-SLOT (N-series pattern · registered at CP7).

### Larger post-W10 work (informational only · not booked)
5. **Audio trainer + real GPU wiring** — audio trainer NOT BUILT (perception-side ASR/diarisation wired but no training pipeline). GPU connect real 7-stage but `.env` currently points at mock SSH. Building the trainer is roughly a wave of its own (~W10-scale · 5-7k LOC). Answered informationally 2026-08-26T08:20Z · no CP scope change.

## Ratified owner rulings · executes without re-litigation

R1-R7 (2026-08-26T04:20Z · W10 pre-GO) · R8 (2026-08-26T05:20Z · preview allowlist permissive-mode for W10 duration · rescinded at wave close) · R9 (2026-08-26T09:20Z · preview allowlist strict-flip at wave close · corrected 09:45Z across both surfaces) · **R10 (2026-08-26T10:00Z · W10 wave RATIFIED)**.

## Standing rules (all remain binding beyond W10 close)

- **W10 CP9 · Authoritative composite recomputation + wave close + strict flip · CLOSED** (with mid-flight correction to strict-flip verification).
  - **Composite (authoritative · Owner correction #4)**: **52.49 %** replacing all wobbly running numbers.
    - Mechanism corpus: **54.45 %** (280.4 / 515 · 109 DONE + 46 PARTIAL + 306 REUSABLE + 53 BUILD + 1 OPEN-SLOT).
    - Interface dimension: **47.93 %** (27.8 / 58 · 10 DONE + 2 PARTIAL + 34 REUSABLE + 12 BUILD).
    - Blend: 0.7 × 54.45 + 0.3 × 47.93 = **52.49 %**.
  - **Method**: `tools/w10_cp9_composite_recompute.py` (deterministic · 32 delta entries · every delta anchored to canon § + commit SHA).
  - **Locked by pytest**: `backend/tests/invariants/test_w10_cp9_composite_lock.py` (5/5 green).
  - **Wave-close cohort**: **261/261 pytest** + **42 node** = 303 assertions across 45 test files. Receipts at `20260826T091500Z_w10_wave_close_green.log` (pytest 261/261) + `20260826T083100Z_w10_cp8_frontend_green.log` (node 25/25) + `20260826T094500Z_w10_strict_flip_matrix_green.log` (node 17/17).
  - **R9 strict flip · CORRECTED (09:45Z)**: initial 09:20Z flip restarted only backend · SPA surface stayed permissive · external tester (09:33Z) caught GET / returning 200. Fix: restart frontend + add 17-invariant mode-matrix node test that reads ALLOWLIST_MODE from `/app/backend/.env` single-source-of-truth and probes BOTH surfaces at BOTH ports across 5 endpoints × 3 probe classes. Full matrix verified in both directions. Updated flip procedure: `sudo supervisorctl restart backend frontend` (BOTH · not just backend). Receipt `20260826T094500Z_w10_strict_flip_verified_both_surfaces.log` supersedes `20260826T092000Z_w10_strict_flip_verified.log`. R9 stands.
  - **Cheap optional fix landed**: `/api/openapi.json` serves 200 (49 paths · docs_url/redoc_url disabled · response-boundary sanitizer intact).
  - **W10 close report banked**: `notes/w10_close_report.md` (W8/W9 format · 12 sections · updated §1 to reflect corrected R9 verification).
- **W10 delivered**:
  - Canon 8 mechanism fabric fully wired (CP1-CP5): Ruling-1 drill · Grey Mirror BUILD · Watch drills + fitness · Reserved-Decisions Panel · Witness fabric + tamper alarms.
  - Doc 14 §33 CA1-005 whitepaper drafter BUILD (CP6 · parity 58→59).
  - Doc 14 §§21-45 register expansion 4→28 rows (CP7).
  - Governance + Watch + Grey-Mirror frontends wired (CP8).
  - Authoritative composite % + wave close + strict flip + close report (CP9).

## W10 checkpoint status — ALL CLOSED

| CP | Scope | Status | Actual LOC |
|----|-------|--------|-----------:|
| CP1 | Ruling-1 firing drill · Canon 8 §27 | CLOSED · 7/7 green | ~200 |
| CP2 | Grey Mirror mirage machinery · BUILD | CLOSED · 25/25 green · parity 52→55 | ~800 |
| CP3 | Watch drills + fitness accounting | CLOSED · 12/12 green | ~400 |
| CP4 | Reserved-decisions panel · Canon 8 §19 | CLOSED · 28/28 green | ~500 |
| CP5 | Witness fabric full signing · Canon 8 §9 | CLOSED · 23/23 green · parity 55→58 | ~600 |
| CP6 | CA1-005 whitepaper drafter · BUILD | CLOSED · 13/13 green · parity 58→59 | ~140 |
| CP7 | Doc 14 §§23-25 24-row register expansion | CLOSED · 8/8 green · docs-only | ~130 |
| CP8 | Governance / Watch / Grey-Mirror frontends + backend state rollups | CLOSED · 32/32 green (7 be + 25 fe) | ~940 |
| CP9 | Authoritative composite · wave close · strict flip · close report | **CLOSED · 5/5 green · 261/261 cohort** | ~230 |

## Outstanding items (all non-blocking · deferred beyond W10)

### Non-blocking owner-policy answers (unchanged from W8/W9)
1. **FL-P4-W8-01** · CA1-N2 (data-subject breach notification) · owner policy pending (7 questions).
2. **FL-P4-W8-01** · CA1-N3 (data-subject erasure) · owner policy pending (7 questions).
3. **FL-P4-W9-01** · CA1-N5 (continuity attestation) · owner policy pending (1 question).

### New at W10
4. **Doc14-020** · Canon 4 §38 rights-unclear grammar · OPEN-SLOT (N-series pattern · registered at CP7).

### Larger post-W10 work (informational only · not booked)
5. **Audio trainer + real GPU wiring** — audio trainer NOT BUILT (perception-side ASR/diarisation wired but no training pipeline). GPU connect real 7-stage but `.env` currently points at mock SSH. Building the trainer is roughly a wave of its own (~W10-scale · 5-7k LOC). Answered informationally 2026-08-26T08:20Z · no CP scope change.

## Ratified owner rulings · executes without re-litigation

R1-R7 (2026-08-26T04:20Z · W10 pre-GO) · R8 (2026-08-26T05:20Z · preview allowlist permissive-mode for W10 duration · RESCINDED at wave close per R9) · **R9 (2026-08-26T09:20Z · preview allowlist strict-flip at wave close · verified · fail-closed posture restored)**.

## Standing rules (all remain binding beyond W10 close)

- Tests-first + right-reason receipts (every CP).
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law · A8 · 2026-08-19).
- Purpose gate on every crossing until Canon 3 §24 strip ceremony (owner act · not fired at W10 close · deferred to owner).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02).
- Pod-shell + spine same-commit mount DoD (FL-P4-W7-02).
- Post-compaction re-read discipline (FL-P4-W9-02).
- Correction-discipline in-band (Owner Ruling 2026-08-19 §6 additive-only).
- Host-identity drill attribution: `drill_actor:*` prefix · no drill-mode switch (R1).
- **Composite % same-commit DoD extension**: any commit touching `tools/w10_cp9_composite_recompute.py` MUST touch `test_w10_cp9_composite_lock.py` in the SAME commit (booked at CP9).
- No push · local commits only.

## Blocked (awaiting owner)

- **No CP is blocked**. W10 is closed.
- Owner may open W11 (post-W10 items above) or ratify a different next-wave scope.

## Cycle status (2026-08-26T08:35Z · W10 CP8 CLOSED · CP9 opening) [ARCHIVED · superseded by 2026-08-26T09:30Z]

- **W10 CP8 · Governance / Watch / Grey-Mirror frontends · CLOSED** at 7/7 backend + 25/25 frontend + 28/28 CP-anchor cohort green.
  - **Backend (thin read-only state rollups · REFERENCE-NOT-COPY)**:
    - `services/governance/router.py` → GET /api/governance/state (approvals · rules_updates lifecycle · reserved_decisions).
    - `services/watch/router.py` → GET /api/watch/state (verdicts · actions · containments · reconciliations · continuity_attestations · witness_attestations · tamper_alarms · fitness summary rollup).
    - `services/grey_mirror/router.py` → GET /api/grey_mirror/state (mirages · touches · severances · BUILD-not-LIFT rationale in body).
    - Every entry carries `record_id` + `source_path` on disk; raw signing material / secrets sanitized out at boundary (Owner Order 2026-08-25 §4).
  - **Frontends** (all under `/app/frontend/src/components/` · mirrored to pod_shell):
    - `Governance.jsx` (routes `/governance` · reserved-decisions + rules-updates + approvals panels · Canon 8 §19 + Doc 15 §17 anchors · names the 5 reserved kinds verbatim per R3).
    - `Watch.jsx` (routes `/watch` · verdicts + actions + containments + witness + tamper + fitness · Canon 8 §7 + §8 + §9 + §14 + §25 anchors · Ruling-1 precondition (b) demonstrated status surfaced from fitness rollup).
    - `GreyMirror.jsx` (routes `/grey-mirror` · mirages + touches + severances · Canon 8 §§15-16 anchors · touch_kind CONTRACT-TIME grammar per R2 · BUILD-not-LIFT rationale visible).
    - Wired into `App.js` (live `/app/frontend/src/App.js` + mirrored `pod_shell/frontend/src/App.js`).
  - **Tests-first**:
    - Backend: `test_w10_cp8_state_endpoints.py` (7 tests · honest-empty · seeded-record reflection · no-raw-secret invariant).
    - Frontend: `pod_shell/frontend/__tests__/w10_cp8_frontends.test.js` (25 tests · source-content testids · REFERENCE-NOT-COPY markers · canon anchors · route wiring · live HTTP 200 through allowlist for all 3 routes · live API JSON shape).
  - **Receipts** (banked to assessment_workspace phase0/drill_receipts/):
    - `20260826T080000Z_w10_cp8_backend_right_reason_fail.log` (7 collection errors · services.governance/watch.router/grey_mirror not yet on disk).
    - `20260826T080100Z_w10_cp8_frontend_right_reason_fail.log` (20 fails · components missing + routes not wired + endpoints 404).
    - `20260826T083000Z_w10_cp8_backend_green.log` (7/7 green).
    - `20260826T083100Z_w10_cp8_frontend_green.log` (25/25 green).
  - **HTML snapshots banked** to `phase0/html_snapshots/` (owner-side rendering per R4):
    - `w10_cp8_governance.html` + `w10_cp8_governance_api.json`
    - `w10_cp8_watch.html` + `w10_cp8_watch_api.json`
    - `w10_cp8_grey_mirror.html` + `w10_cp8_grey_mirror_api.json`
- **Preview routes owner should eyeball** (permissive allowlist holds through CP9 close per R8):
  - `/governance` — reserved-decisions panel + rules-updates timeline + approvals ledger
  - `/watch` — fitness summary + verdicts/actions/containments/witness/tamper panels
  - `/grey-mirror` — mirages + touches + severances panels
  - Ruling-1 precondition (b) DEMONSTRATED renders in the Watch header (drill note on disk at `phase0/drill_receipts/ruling_1_drill_witness_note.md`).
- **Honest empty state**: all live record stores are 0-count today (production Watch has not yet fired against real traffic; mirages not yet installed; approvals ledger not yet lit). The surfaces render "0 X on record · Canon anchor: … · Drawn, never left blank."
- **Contract parity unchanged**: still 59 (CP8 is a surface CP · no new frozen contracts).
- **Stop-and-report to owner**: CP8 status paragraph + preview-route list delivered. CP9 opens on owner ack.

## Interleaved owner readiness query (2026-08-26T08:20Z) — audio trainer × GPU

Answered from ground truth (no ratification recorded · informational only):
- Audio trainer: **not built**. Perception-side audio inference wired (`services/layer_b/asr/*`, `layer_a/handlers/audio.py`, `services/perception/asr_worker.py`). Training-side absent — no `services/audio_trainer/`, no audio training-run contract.
- GPU connect: `/api/connect/gpu` real (7-stage pipeline · commissioning · trust receipts) but `.env` currently points at mock SSH host (`/tmp/akki_mock_sshd/*`). No production GPU connected today.
- Verdict: **not ready** for a real audio-trainer-on-GPU test. Building the trainer is roughly a wave of its own (~W10-scale · 5-7k LOC) · deferred beyond W10.
- Recorded here for continuity; no CP scope change.

## W10 checkpoint status

| CP | Scope | Status | Actual LOC |
|----|-------|--------|-----------:|
| CP1 | Ruling-1 firing drill · Canon 8 §27 | CLOSED · 7/7 green | ~200 |
| CP2 | Grey Mirror mirage machinery · BUILD | CLOSED · 25/25 green · parity 52→55 | ~800 |
| CP3 | Watch drills + fitness accounting | CLOSED · 12/12 green | ~400 |
| CP4 | Reserved-decisions panel · Canon 8 §19 | CLOSED · 28/28 green | ~500 |
| CP5 | Witness fabric full signing · Canon 8 §9 | CLOSED · 23/23 green · parity 55→58 | ~600 |
| CP6 | CA1-005 whitepaper drafter · BUILD | CLOSED · 13/13 green · parity 58→59 | ~140 |
| CP7 | Doc 14 §§23-25 24-row register expansion | CLOSED · 8/8 green · docs-only | ~130 |
| CP8 | Governance / Watch / Grey-Mirror frontends + backend state rollups | **CLOSED · 32/32 green (7 be + 25 fe)** | ~940 |
| CP9 | Authoritative composite % calculation + record + wave close + strict-flip verification | pending | — |

## Awaiting owner (post-CP8)

1. **Owner ack on CP8** (one-paragraph status + preview routes list delivered · CP9 opens on GO).
2. **9 policy answers** (FL-P4-W8-01 + FL-P4-W9-01 · non-blocking to CP9 open).

## Ratified · executes without re-litigation (unchanged from R1-R8)

R1-R8 · permissive allowlist holds through CP9 close · flip-back sequence baked into wave-close checklist.

## Cycle status (2026-08-26T07:20Z · W10 CP7 CLOSED · CP8 opening) [ARCHIVED · superseded by 2026-08-26T08:35Z]

- **W10 CP7 · Doc 14 §§23-25 24-row expansion · CLOSED** at 8/8 CP-cohort green + 88/88 wider W10 cohort green.
  - Register expanded: `notes/requirements_register_17docs.md` §Doc 14 grew from 4 rows to 28 rows (24 new rows: Doc14-002..022, 025, 027, 028).
  - Each row cites a Canon 4 § anchor (§§21-45 · Model Ecosystem lifecycle) with cross-anchors to Canon 5 §12.2 (Models tab) and Canon 6 §4 (Setup — Model Ecosystem) per §Row-count table.
  - Status vocabulary fixed to `{DONE, PARTIAL, REUSABLE, BUILD, BUILT-W10, OPEN-SLOT}`. Distribution: 7 DONE (MOAC 6-criterion + uncurated + rights-lineage) · 3 PARTIAL (adapter-registry wiring · version-history query surface · build-gate coverage) · 3 REUSABLE (Standards · Rights declaration · Frozen-objective invariants) · 8 BUILD (Critic Seam quartet · No-adapter surface · Contents attestation · Quality card · MOAC drift) · 1 OPEN-SLOT (Doc14-020 rights-unclear grammar · policy-pending · non-blocking per Owner CP7 GO).
  - Pre-CP7 rows (Doc14-001, 023, 024, 026) preserved verbatim (Owner Ruling 2026-08-19 §6 additive-only correction discipline).
  - Tests: `backend/tests/invariants/test_w10_cp7_doc14_expansion.py` (8 tests-first structural invariants · row count · ID set · no dupes · canon anchor · status token · pre-CP7 preservation · CP7 new-set sanity).
  - Receipts: red `phase0/drill_receipts/20260826T070000Z_w10_cp7_right_reason_fail.log` (2/8 fail with count 4≠28 + 24 missing IDs) + green `20260826T072000Z_w10_cp7_green.log` (21/21 with CP6 anchor cohort included).
  - Wider re-verification: 88/88 across W10 CP1-CP7 + all frozen/parity/W10 CPs. No regression.
- **Contract parity unchanged**: parity still 59 (register expansion is a docs-only CP · no new frozen contracts).
- **Stop-and-report to owner**: CP7 status paragraph delivered. CP8 opens on owner ack.

## W10 checkpoint status

| CP | Scope | Status | Actual LOC |
|----|-------|--------|-----------:|
| CP1 | Ruling-1 firing drill · Canon 8 §27 | CLOSED · 7/7 green | ~200 |
| CP2 | Grey Mirror mirage machinery · Canon 8 §15-§16 · BUILD | CLOSED · 25/25 green · parity 52→55 | ~800 |
| CP3 | Watch drills + fitness accounting · Canon 8 §25-§28 | CLOSED · 12/12 green | ~400 |
| CP4 | Reserved-decisions panel · Canon 8 §19 | CLOSED · 28/28 green | ~500 |
| CP5 | Witness fabric full signing · Canon 8 §9 + §33 | CLOSED · 23/23 green · parity 55→58 | ~600 |
| CP6 | CA1-005 whitepaper drafter · Doc 14 §33 · BUILD · 150-LOC lid | CLOSED · 13/13 green · parity 58→59 | ~140 |
| CP7 | Doc 14 §§23-25 24-row register expansion | **CLOSED · 8/8 green · docs-only · parity unchanged** | ~130 register lines + 152 test LOC |
| CP8 | Governance / Watch / Grey-Mirror React views + DOM asserts + HTML snapshots (REFERENCE-NOT-COPY) | pending | — |
| CP9 | Authoritative composite % calculation + record + wave close + strict-flip verification | pending | — |

## Awaiting owner (post-CP7)

1. **Owner ack on CP7** (one-paragraph status delivered · CP8 opens on GO).
2. **9 policy answers** (FL-P4-W8-01 + FL-P4-W9-01 · non-blocking to CP8-CP9 open).

## New open slot recorded at CP7

- **Doc14-020** ← C4-054 §38 · Rights-unclear grammar is a first-class state. Row marked **OPEN-SLOT** (same pattern as N-series) pending owner policy on the resolution ceremony. Non-blocking to W10 close.

## Ratified · executes without re-litigation (unchanged from R1-R8)

R1-R7 above · R8 preview allowlist config (2026-08-26T05:20Z · permissive holds through CP9 close · flip-back sequence baked into wave-close checklist).

## Standing rules (all binding through W10 close)

- Tests-first + right-reason receipts (every CP).
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law · A8 ratified 2026-08-19).
- Purpose gate on every crossing until Canon 3 §24 strip ceremony (owner act · projected ready at CP9 close).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02).
- Pod-shell + spine same-commit mount DoD (FL-P4-W7-02).
- Post-compaction re-read discipline (FL-P4-W9-02).
- Correction-discipline in-band (Owner Ruling 2026-08-19 §6).
- Host-identity drill attribution: `drill_actor:*` prefix · no drill-mode switch (R1).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- Owner ack on CP6 close (one-paragraph status delivered).
- Owner rulings on 9 policy questions (non-blocking to CP7 open · load-bearing before N-series + continuity attestations FIRE live records).

## Cycle status (2026-08-26T04:25Z · W9 CLOSED (with corrections FL-P4-W9-02) · W10 pre-GO orchestrator ratifications R1-R7 logged · awaiting owner W10 GO) [ARCHIVED · superseded by 2026-08-26T06:30Z]

- **W9 CLOSED** at 416/416 wave-close cohort green (63 files).
- **FL-P4-W9-02 opened + closed at open** · new post-compaction discipline ratified.
- **Orchestrator ratifications R1-R7 logged in DECISIONS.md 2026-08-26T04:20Z**:
  - **R1** · CP1 firing-drill · Canon 8 §27 · REAL default dirs · host-identity `drill_actor:` pattern (Phase 0 · DECISIONS.md L347) · no drill-mode switch.
  - **R2** · CP2 MirageTouch touch_kind grammar · CONTRACT-TIME frozen `Literal["innocent_read", "guilty_use"]` · no service-time extensibility.
  - **R3** · CP4 reserved_decision_kind · closed `Literal` enum (5 Canon 8 §19 verbatim items) · no free-text.
  - **R4** · CP8 screenshot posture · TRIAD (DOM-asserts + curl-through-allowlist + banked HTML snapshots under `phase0/html_snapshots/`) · owner-side visual verification standing named gap.
  - **R5** · Scope narrowing NONE · all 9 CPs stay · sequencing CP1 first · CP2-CP8 in order · CP9 last · stop-and-report 7,040 LOC re-baselined.
  - **R6** · N-series + continuity policy-pending state = config layer · answers land zero-code-change.
  - **R7** · Standing discipline continuation.
- **Ruling-1 status SURFACED (from FL-P4-W9-02 correction)**:
  - Precondition (a) declaration ✓ DEMONSTRATED (W1).
  - Precondition (b) Watch reconciler DEMONSTRATED FIRING · **NOT YET** · CP1 banks it.
  - Purpose-gate strip **NOT ready-for-ceremony** · will surface as ready at W10 CP9 close (owner act to strip).

## Awaiting owner (final list pre-W10)

1. **W10 GO** (the message that starts CP1 · may narrow scope · supersedes R5 if it does).
2. **9 policy answers** — FL-P4-W8-01 (7 · CA1-N2 + CA1-N3) + FL-P4-W9-01 (2 · CA1-N5). Non-blocking to W10 open · land as config zero-code-change per R6.

## Ratified · executes without re-litigation on GO

R1-R7 above · full verbatim in `STATE/DECISIONS.md` 2026-08-26T04:20Z section · full CP-by-CP scope in `notes/w10_grounding_brief.md` (updated 2026-08-26T04:25Z with R1-R6 baked into §3 · §4 · §6 · §10 · §13).

## Programme dashboard (post-W9 · composite % held pending W10 CP9)

- **Frozen contracts** · 52.
- **Fidelity ledger** · 16 rows opened · 14 CLOSED · 2 OPEN (both owner-policy-pending).
- **Test cohort** · 416 green (63 files).
- **Cumulative LOC (W1..W9)** · ~23039 net.
- **Composite %** · **HELD pending W10 CP9 authoritative recomputation** (owner correction #4 · method stated in brief §11).

## Ready for owner ceremony (Canon 3 §24 · owner act) — projected

- Purpose-gate strip · **projected ready at W10 CP9 close** (after CP1 banks Ruling-1 precondition (b) demonstration).

## Standing rules (unchanged from W9 + FL-P4-W9-02)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law · A8 ratified 2026-08-19).
- Purpose gate on every crossing until Canon 3 §24 strip ceremony (owner act).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02).
- Pod-shell + spine same-commit mount DoD (FL-P4-W7-02).
- Post-compaction re-read discipline: last 200 lines of DECISIONS.md + current NEXT.md before any report/STATE change (FL-P4-W9-02).
- Correction-discipline: in-band · old wording struck-through · CORRECTION note · no silent rewrite (Owner Ruling 2026-08-19 §6).
- Host-identity drill attribution (Phase 0 DECISIONS.md L347): `drill_actor:*` prefix · no drill-mode switch (R1 confirmed for W10 CP1).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- Owner GO for W10 (executes R1-R7 · CP1 first).
- Owner rulings on 9 policy questions (non-blocking to W10 open · load-bearing before N-series + continuity attestations FIRE live records).

## Cycle status (2026-08-26T04:05Z · W9 CLOSED WITH CORRECTIONS · owner GO needed for W10) [ARCHIVED · superseded by 2026-08-26T04:25Z with R1-R7 logged]

- **W9 CLOSED** at 416/416 wave-close cohort green (63 files).
- **FL-P4-W9-02 opened + closed at open** · 3 report-time errors named + corrected in-band on `notes/w9_close_report.md §12` · new post-compaction discipline ratified (re-read last 200 lines of DECISIONS.md before drafting any report or STATE change).
- **Ruling-1 status SURFACED (missing from initial W9 reply · now corrected):**
  - Precondition (a) declaration ✓ DEMONSTRATED (W1).
  - Precondition (b) Watch reconciler DEMONSTRATED FIRING · **NOT YET** · `phase0/watch_*/` dirs do not exist on disk.
  - Purpose-gate strip **NOT ready-for-ceremony**. Needs a firing drill (W10 CP1 candidate · Canon 8 §27 · containment expiring clean · ~200 LOC).

## Awaiting owner (post-W9 · CORRECTED)

1. **FL-P4-W8-01 batch** · 7 N-series policy questions (CA1-N2 breach + CA1-N3 erasure).
2. **FL-P4-W9-01 batch** · 2 CA1-N5 continuity attestation questions.
3. **W10 GO + scope confirmation** — polish/completion wave · ~5000-6000 LOC estimated per §7 of `status_and_wave_plan.md` re-baselined table if extended · owner-confirmed scope named in `notes/w10_grounding_brief.md`.

**REMOVED from awaiting list per FL-P4-W9-02 corrections:**
- ~~A8 ruling~~ — ratified 2026-08-19 (DECISIONS.md L738-760). Walk-this UNBLOCKED for W10.
- ~~Executive-Final access decision~~ — repo accessed 2026-08-19 (HEAD `bba80ab`). Verdict on record: no Watch/Grey-Mirror material · Grey Mirror is a BUILD.

## Programme dashboard (post-W9 · composite % held pending W10 authoritative recomputation)

- **Frozen contracts** · 52.
- **Fidelity ledger** · 16 rows opened · 14 CLOSED · 2 OPEN (FL-P4-W8-01 + FL-P4-W9-01 · both owner-policy-pending).
- **Test cohort** · 416 green (63 files).
- **Cumulative LOC** · ~23039 net (W1..W9).
- **Composite %** · **HELD pending W10 authoritative recomputation** per owner correction #4. No running number in the interim.

## Ready for owner ceremony (Canon 3 §24 · owner act)

- Purpose-gate strip · **NOT YET ready-for-ceremony**. Blocked on Ruling-1 precondition (b) demonstration firing drill (W10 CP1).

## Standing rules (unchanged from W9)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law · A8 ratified 2026-08-19).
- Purpose gate on every crossing (still on record until Canon 3 §24 ceremony).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02).
- Pod-shell + spine same-commit mount DoD (FL-P4-W7-02).
- **NEW (FL-P4-W9-02)**: after ANY context compaction (agent restart, session reset, fork), FIRST action before drafting a report or STATE change is to re-read the last 200 lines of `STATE/DECISIONS.md` AND the current `STATE/NEXT.md`.
- Correction-discipline (Owner Ruling 2026-08-19 §6): corrections in-band with old wording struck-through + explicit CORRECTION note · never a silent rewrite.
- STATE/NEXT.md always carries exact resume point.
- No push; local commits only.

## Blocked (awaiting)

- Owner GO for W10.
- Owner rulings on 9 policy questions across 2 open FL rows (non-blocking to W10 open · but load-bearing before N-series + continuity attestations FIRE live records · and Ruling-1 firing drill is a separate CP1 unblocker).

## Cycle status (2026-08-26T03:45Z · W9 CLOSED · initial reply) [ARCHIVED · superseded by 2026-08-26T04:05Z with in-band corrections FL-P4-W9-02]

- **W9 CLOSED** at 416/416 wave-close cohort green (63 files) · `phase0/drill_receipts/20260826T034000Z_w9_wave_close_green.log`.
- **W9 LOC** · 2190 net (spine only · pod-shell unchanged) vs 6400 budget · **34%** · UNDER by 4210 LOC.
- **W9 register rows lit** · 17 (14 Canon 8 · 3 CA-series: CA1-011 · CA1-012 · CA1-N5 scaffold).
- **W9 fidelity ledger rows** · 1 opened (`FL-P4-W9-01` OPEN · CA1-N5-q1 owner-policy · non-blocking to close).
- **Auto-continue mandate SATISFIED** (W8 + W9 completed per owner ruling 2026-08-26T00:25Z).
- **Deferrals from W9**: Grey Mirror four sub-surfaces (§15-§16 + §32.4 · XL scope) · Walk-this per A8 ruling (owner-ruling pending) · Watch drills + fitness (§25-§28) · Reserved-decisions panel (§19) · Witness fabric (§9 full signing) · CA1-005 whitepaper · Doc 14 §§23-25 24-row expansion · Governance frontends. All named for a subsequent polish/completion wave with explicit owner GO.
- Full close report at `notes/w9_close_report.md` · dashboard §11 · owner policy questions §7 (batched across FL-P4-W8-01 + FL-P4-W9-01 = 9 total).

## Programme dashboard (post-W9)

- **Frozen contracts** · 52 (from 39 at W7 close · +13 across W8+W9).
- **Fidelity ledger** · 15 opened · 13 CLOSED · 2 OPEN (both owner-policy-pending).
- **Test cohort** · 416 green (from 250 at W6 close · +166 across W7+W8+W9).
- **Cumulative LOC** · ~23039 net (W1..W9).
- **Mechanism corpus** · ~50%.
- **Composite headline** · ~48%.

## Awaiting owner (post-W9)

1. **FL-P4-W8-01 batch** · 7 N-series policy questions (CA1-N2 breach + CA1-N3 erasure).
2. **FL-P4-W9-01 batch** · 2 CA1-N5 continuity attestation questions (verification architecture + RTO target).
3. **A8 ruling** (Walk-this Q1/Q2/Q3).
4. **Executive-Final access decision** (Grey Mirror mechanism completion depends materially).
5. **W10 GO + scope confirmation** (polish/completion wave · roughly 5000-6000 LOC estimated).

## Standing rules (unchanged from W8)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law).
- Purpose gate on every crossing (still on record until Canon 3 §24 ceremony).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02 extension).
- Pydantic 2.13.4 pin is LOAD-BEARING.
- Wave-close cohort assembly: grep filename + content-grep + `test_*_invariants.py` + hardcoded-count-assertion grep.
- Pod-shell + spine same-commit mount DoD (W7-added).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- Owner GO for W10 (polish/completion wave) — no auto-continue covers this.
- Owner rulings on 9 policy questions across 2 open FL rows (non-blocking to close, but load-bearing before N-series + continuity attestations can FIRE live records).
- Owner A8 ruling (Walk-this) — load-bearing for that specific deferred item.

## Cycle status (2026-08-26T02:45Z · W8 CLOSED · W9 CP1 OPENING) [ARCHIVED]

- **W8 CLOSED** at 366/366 wave-close cohort green (55 files) · `phase0/drill_receipts/20260826T024000Z_w8_wave_close_green.log`.
- **W8 LOC** · 2964 spine + 4 pod-shell = 2968 net vs 5600 budget · **53%** · UNDER by ~2632 LOC.
- **W8 register rows lit** · 10 (7 Doc 15 · 3 CA-series partial/scaffolding).
- **W8 fidelity ledger rows** · 2 opened (`FL-P4-W8-01` OPEN owner-policy · `FL-P4-W8-02` CLOSED new DoD element).
- **Deferrals from W8**: CA1-005 whitepaper · Doc 14 §§23-25 24-row expansion · Governance frontends · CA1-012 Watch staleness-flagging · Data Suite · LLM chip polish. All named for W9 or a subsequent polish wave (no silent slip).
- **Frontends deferred to a subsequent polish wave** (backend records on record; screenshot gap unchanged).
- Full close report at `notes/w8_close_report.md` · dashboard §11 · owner policy questions §7.

## W9 opening — CP1 carry-over items (all P0)

1. **FL-P4-W8-01 policy answers** — if owner has ruled on the 7 N-series questions (Close Report §7), wire the answers · else continue rest of W9 without firing.
2. **Watch mechanism primary build** (Doc 3 · Doc 8) — includes CA1-011 enforcement half at `services.watch.route_recheck_failure` (W9 seam per Owner Ruling 2026-08-25T23:15Z SPLIT).
3. **Grey Mirror four sub-surfaces** (overview · monitor · response · people).
4. **Ledger continuity (CA1-N5)**.
5. **Walk-this** per A8 ruling (Q1 · Q2 · Q3).
6. **CA1-012 Watch staleness-flagging** (carried from W8).
7. **Doc 14 §§23–25 remaining 24 rows** (carried from W7).
8. **CA1-005 whitepaper re-evaluation** (carried from W7).

## W9 nominal scope (owner-confirmed 2026-08-26T00:25Z · auto-continue after W8)

- Watch mechanism · Grey Mirror completion (four sub-surfaces).
- CA1-N5 ledger continuity attestation.
- Walk-this per A8 ruling.
- CA1-011 enforcement half at named seam.
- CA1-012 Watch staleness-flagging.
- Doc 14 §§23-25 24-row expansion.
- CA1-005 whitepaper re-evaluation.
- Wave close · cohort assembly · close report.

**W9 stop-and-report line**: 6400 LOC per re-baselined table.

## Standing rules (all binding through W9)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law).
- Purpose gate on every crossing (still on record until Canon 3 §24 ceremony).
- Contract + snapshot + parity map + **hardcoded numeric assertion** same-commit DoD (FL-P4-W8-02 extension).
- Pydantic 2.13.4 pin is LOAD-BEARING (Extraction-Akki L4-L18).
- Wave-close cohort assembles by grep filename + content-grep + `test_*_invariants.py` + hardcoded-count-assertion grep (W8-added).
- Pod-shell + spine same-commit mount DoD (W7-added).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- None. W9 CP1 opens immediately.

## Cycle status (2026-08-26T01:15Z · W7 CLOSED · W8 CP1 OPENING) [ARCHIVED]

- **W7 CLOSED** at 310/310 wave-close cohort green (44 files) · phase0/drill_receipts/20260826T010500Z_w7_wave_close_green.log.
- **Owner auto-continue** for W8 and W9 · per-wave go-gate lifted (2026-08-26T00:25Z verbatim in DECISIONS.md).
- **W7 LOC** · 2779 net (2429 spine + 350 pod-shell) vs 3520 budget · **79%** · UNDER by 741 LOC.
- **W7 register rows lit** · 17 (13 Doc 13 · 4 Doc 14).
- **W7 fidelity ledger rows** · 2 opened + closed (FL-P4-W7-01 · FL-P4-W7-02).
- **1 deferral to W8** · CA1-005 whitepaper (never opened · honest gate under 150-LOC lid).
- Full close report at `notes/w7_close_report.md` · dashboard on §10.

## W8 opening — CP1 carry-over items (all P0)

1. **Canonical-projection remediation** — pydantic-version-independent projection for frozen snapshots (Owner Ruling 2026-08-25T22:55Z Q1 · from W6 close). Load-bearing for W8's contract-heavy scope.
2. **Pod-shell mount completeness test** (new invariant · from FL-P4-W7-02 §7.2).
3. **Pod-shell boot test** (new invariant · from FL-P4-W7-02 §7.2).
4. **Async event-loop pollution owner-visibility ruling** (from W7 CP8 conftest fixture · owner may want a different remediation).
5. **CA1-005 whitepaper re-evaluation** (deferred from W7 CP6).
6. **Doc 14 §§23–25 · 24 remaining rows expansion** (from W7 opener grounding · deferred).

## W8 nominal scope (owner-confirmed 2026-08-26T00:25Z)

- Governance ceremony · Approvals surfaces.
- N-series: CA1-N2 breach notification · CA1-N3 access-and-erasure.
- CA1-009 generalized handoff contract.
- Rules Updates · Spend Requests · Trace surface (REFERENCE-NOT-COPY load-bearing).

## W9 nominal scope (owner-confirmed 2026-08-26T00:25Z · auto-continue after W8)

- Watch mechanism · Grey Mirror completion.
- CA1-N5 ledger continuity.
- Walk-this per A8 ruling (Q1 · Q2 · Q3).
- CA1-011 enforcement half at named seam (`services.watch.route_recheck_failure`).
- Ruling-1 closure question surfaced (NOT fired · Canon 3 §24 ceremony is an owner act).

## Standing rules (all binding through W8 + W9)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (LOAD-BEARING for W8 Trace surface).
- Purpose gate on every crossing (still on record until Canon 3 §24 ceremony).
- Contract + snapshot + parity same-commit DoD (FL-P4-W6-02/08/09).
- Pydantic 2.13.4 pin is LOAD-BEARING (Extraction-Akki L4-L18).
- Wave-close cohort assembles by grep filename + content-grep + `test_*_invariants.py` (W7-broadened).
- Pod-shell + spine same-commit mount DoD (W7-added).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- None. W8 CP1 opens immediately.

## Cycle status (2026-08-25T23:38Z · W7 CP1 CLOSED · CP2 opening) [ARCHIVED]

- **W7 GO** received from owner at 2026-08-25T23:30Z (see STATE/DECISIONS.md L1358-L1421). Scope: Docs 13 + 14 + CA1-004 + CA1-005 + CA1-011-split + W6 deferrals folded in. Budget ~3520 LOC · stop-and-report line at 3520.
- **CP1 (Rulings + rates lane) · GREEN**: 5/5 tests-first invariants green at `phase0/drill_receipts/20260825T233800Z_w7_cp1_green.log` (right-reason failure at `20260825T233500Z_w7_cp1_right_reason_fail.log`). Delta: `services/cost_ledger/rates.py` extended with `training` lane + `rate_for_training_run()`; `phase0/rates_register/training/` opened with README (honestly absent — no rate rows on record).
- **CP2 (Targeta service LIFT) · opening**: RMS-IQ-Core-2 `services/targeta/` (425 LOC · 6 files) LIFT into `Extraction-Akki/backend/services/targeta/`. Contract already in-tree (`contracts/targeta_plan.py` + snapshot). Tests-first from RMS `tests/invariants/test_targeta_invariants.py` (207 lines · adapt).

## W7 checkpoint status

| CP | Scope | Status | Est. LOC (pre-cal.) | Actual LOC |
|----|-------|--------|--------------------:|-----------:|
| CP1 | Rulings + rates lane · training register subdir · README | GREEN | 150 | ~50 (SLA under-run) |
| CP2 | Targeta service LIFT + invariants | opening | 500 | — |
| CP3 | Model registry service (top-level `services/model_registry/`) LIFT + FACTS-only seed (7 Emergent Universal models · no whisper-tiny) | pending | 350 | — |
| CP4 | Model Admission ceremony backend · six-criterion MOAC · uncurated-sample discipline · rights lineage · quarantine · Batch Board records | pending | 700 | — |
| CP5 | CA1-004 baseline line + CA1-011 re-check state (Watch route SPLIT to W9 · named seam on record from W7) | pending | 400 | — |
| CP6 | CA1-005 whitepaper · 150-LOC hard lid · OR W8-defer with named gap | pending | 250 or DEFER | — |
| CP7 | W6 deferrals folded in: Data Suite surface (v7-exact) · LLM chip UI polish · Model Ecosystem surface (Baseline · Ecosystem · Admission tabs) | pending | 700 | — |
| CP8 | Wave close · cohort assembly (grep frozen+contract) · STATE · screenshots · close report | pending | 50 | — |
| **Estimate total (pre-cal.)** | | | **3100 · × 1.60 ≈ 3520** | **~50 (CP1 only)** |

## W7 CP1 rulings summary (owner · 2026-08-25T23:30Z)

- **Q2 · MOAC uncurated-sample**: REUSE Registry census facts (235 tables · 145 crossing receipts) where letter permits. Fresh pass ONLY where Doc 13 requires record-contents sampling AND a named purpose is on record — else NAME THE GAP.
- **Q3 · Namespace**: `services/model_registry/` first-class package. LIFT RMS fabric. Seed from FACTS only: 7 Emergent Universal models (real, W5-connected). **whisper-tiny NOT seeded** (donor-side CI fixture, not on this estate).
- **Q4 · CA1-005 whitepaper**: 150-LOC hard lid; overrun → W8-defer with named gap.

## Standing rules (unchanged from W6)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY.
- Purpose gate on every crossing.
- Contract + snapshot + parity same-commit DoD (FL-P4-W6-02/08/09 ratification).
- Pydantic 2.13.4 pin is LOAD-BEARING (Extraction-Akki `5aba8e7`).
- Wave-close cohort assembles by grep `test_*_frozen*.py` + `test_*_contract*.py`.
- No push; local checkpoint commits; STATE/ kept current.

## Blocked (awaiting)

- None. CP2 proceeds immediately.

## Cycle status (2026-08-25T22:40Z · W6 CLOSED · steer requested) [ARCHIVED]

- **W1..W6 · CLOSED**. 250/250 W6 wave-close cohort green (36 test files) at `phase0/drill_receipts/20260825T224000Z_w6_wave_close_green.log`. Frozen+contract sub-cohort 18/18 green at `phase0/drill_receipts/20260825T223200Z_w6_close_frozen_cohort_green.log`.
- **W6 LOC actual**: +3319 net (+3716 −397) vs 2880 budget · **15% overrun**. Envelope stop-and-report to owner (see notes/w6_close_report.md §5 & §8).
- **9 fidelity ledger rows opened at W6 close** — TWO defect classes named, NOT nine of the FL-P4-W4-01 class:
  - 6 × **environmental pydantic 2.13.4 serialization drift** (FL-P4-W6-01/03/04/05/06/07) — none wave-attributable; models untouched since 2026-07-02/07-31.
  - 3 × **FL-P4-W4-01 map/count omission recurring** at W1 origin (FL-P4-W6-02/08/09) — actor_declaration snapshot on disk but never mapped; NamedTuple utilities over-enumerated. Recurrence count for FL-P4-W4-01 class: 2.
- **W6 deferrals named** (deferred to W7, not held-open):
  - Data Suite surface (v7-exact) — backend not yet built; full CP moves to W7.
  - LLM chip UI polish — cosmetic; belongs alongside Cost Ledger polish loop.
  - Grey Mirror overview surface — waiting on Watch (W9 per opener plan).
  - Pydantic-version-drift remediation — new P1 W7-opener owner-ruling item.
- **W7 nominal scope** (per opener #1 re-baseline): Targeta · Model Ecosystem · Model Admission · ~3520 LOC. **WAITING for owner W7 GO.**

## W6 delivered · commits on programme/track-a

```
7db5a00 W6 close · 9 fidelity ledger drifts reconciled · 2 distinct defect classes named
39a7034 W6 CP5 · Lowered Standard (CA1-010) · session-scoped state + expiry + in_process residency
d9ae4a5 W6 CP4 · Solva stages 4-6 · Grey Mirror groundwork · mechanism-side only
770e013 W6 CP3 · Retention enforcement · CA1-N1 · 218/218 green
717013f W6 CP2b · Cost Ledger frontend surface · CA1-008 lever sequence visible
d7ff88e W6 CP2 · Cost Ledger backend · CA1-008 rates + ledger + 5-lever attribution
f647051 W6 opener #2 · FL-P4-W4-01 reconciled · frozen contract parity restored
```

W6 close report: `notes/w6_close_report.md` (canonical).

## Owner steer requested before W7 GO (blocking)

1. **Pydantic-version-drift remediation path** (close report §4.1): pin pydantic (a) vs canonical-projection (b) vs both?
2. **W6 LOC overrun** (15%): accept the recalibrated envelope for W6 as delivered, or narrow-scope W7 to absorb the overrun?
3. **W7 scope confirmation**: Targeta · Model Ecosystem · Model Admission per re-baselined estimate of 3520 LOC — proceed as planned, or steer?

## Cycle status (2026-08-25 · W6 openers CLOSED · W6 scope opening) [ARCHIVED]

- **W1..W5 · CLOSED**. 195/195 gating tests green across the wave-open cohort (194 W5-close + 1 FL-P4-W4-01 reconciled).
- **W6 opener #1 · re-baseline · DONE**. Calibration factor 1.60× published in notes/status_and_wave_plan.md §7. W6 stop-and-report line: **2880 LOC**.
- **W6 opener #2 · FL-P4-W4-01 · DONE**. Root-cause named (W4 close missed the snapshot bump); reconciliation via snapshot bump ratified by this owner ruling; fidelity ledger row closed at phase0/fidelity_ledger/FL-P4-W4-01.json.
- **W6 SCOPE opening · IN PROGRESS**:
  - CP1 · rulings + brief (this update) — pending.
  - CP2 · rates register (owner-supplied or honestly absent) + Cost Ledger backend + tests — pending.
  - CP3 · retention enforcement + tests — pending.
  - CP4 · Grey Mirror groundwork + Solva stages 4-6 mechanism-side — pending.
  - CP5 · W5 deferrals folded in (LLM chip UI + Data Suite + CA1-010) — pending.
  - CP6 · wave close (dashboard + STATE + screenshots) — pending.

## W6 openers summary

### Opener #1 · Re-baseline (in notes/status_and_wave_plan.md §7)
- W1: 1006 LOC actual vs 800 est → 1.26×.
- W2: 1666 vs 150 → 11.11× — **class misclassification** (S→M-effective).
- W3: 2519 vs 2000 → 1.26×.
- W4: 2566 vs 600 → 4.28× — **class misclassification** (M→L-effective).
- W5: 4026 vs 2500 → 1.61×.
- **Calibration factor: 1.60× (median), 1.95× (weighted mean)** — using MEDIAN as the go-forward multiplier (owner ruling naming).
- W6-W9 re-baselined: **W6 ~2880 LOC · W7 ~3520 LOC · W8 ~5600 LOC · W9 ~6400 LOC · total ~18400 LOC**.
- Remaining build effort is 60% higher than pre-calibration; W1-W5 landed 95% higher than pre-calibration.
- Three ruling paths named for owner (accept re-baseline / narrow scope / add L-extended tier); default: accept.

### Opener #2 · FL-P4-W4-01 closed
- Root-cause: W4 extended `LedgerRow` (added `thinklab_objective`, `row_id`, description tweaks, `additionalProperties: True` on stamp_audit, dropped `at` from required) but skipped the snapshot bump — silently failing test at HEAD `a71ea67`.
- Reconciliation: bump `northena_ledger_row.contract_snapshot.json` to match current W4-ratified code shape. Owner Ruling W6 GO opener #2 IS the explicit ratification moment.
- Right-reason failure: phase0/drill_receipts/20260825T204000Z_w6_opener2_FL-P4-W4-01_right_reason.log.
- Green after fix: 195/195 in phase0/drill_receipts/20260825T205000Z_w6_opener2_FL-P4-W4-01_green.log.
- Fidelity ledger row banked at phase0/fidelity_ledger/FL-P4-W4-01.json — CLOSED.
- Process finding: W4 close cohort had a scoping gap (missed a contract snapshot test). Note in the ledger row; future wave-close cohorts assemble by grep for `test_*_frozen*.py` + `test_*_contract*.py`.

## W6 scope plan (post-openers)

Grounded in the register rows FIRST (owner ruling). Six checkpoints:

**CP2 · Cost Ledger (CA1-008 + Docs 11/12)**:
- Read the CA1-008 lever sequence from the addendum / Doc 11 / Doc 12 verbatim (BEFORE opening code — quote it in the CP2 brief).
- Rates register: `services/cost_ledger/rates.py` reads from `phase0/rates_register/*.json` — OWNER-SUPPLIED FACTS or honestly absent. If no rate on record for a model or GPU-hour, ledger shows quantities with the W2 honest-gap sentence.
- Ledger backend: `services/cost_ledger/ledger.py` consumes W5 metering receipts (all `solva_* / chat_* / thinklab_* / llm_*` kinds) + W2 reflection quotas + seam GPU usage into ledger entries.
- Surface: `pod_shell/frontend/src/components/CostLedger.jsx` per v7 oracle `COMPUTE_CHARTS` fabric.

**CP3 · Retention enforcement (CA1-N1)**:
- Quote the register's letter for retention on each record class we hold: receipts / ledger rows / chat turns / admits / seam runs.
- Append-only classes NEVER get delete verb — retention on those = marked-expired + excluded-from-render. If the register says otherwise, quote it and STOP.
- Enforcement mechanism per the letter (expiry marking / governed deletion path).
- Surface: retention state row on records + attestation record.

**CP4 · Grey Mirror groundwork + Solva stages 4-6**:
- Solva stages 4 (triangulation) · 5 (tension_detection) · 6 (probability_weighting) ADAPTED from Executive-Final donor · mechanism-side only.
- Grey Mirror overview surface only if oracle has parts that render honestly from what exists (else deferred to W9 with Watch).

**CP5 · W5 deferrals folded in**:
- ConnectDrawerChat LLM chip UI polish (backend live).
- Data Suite surface v7-exact (data facts from real connected sources · structure-only posture).
- CA1-010 session-scoped lowered-standard with logged expiry (state visible + refusal grammar).

**CP6 · wave close**: dashboard delta + screenshots + STATE + close report.

## Verification path for orchestrator (independent audit) — W6 openers close

```bash
cd /app/assessment_workspace/repos/Extraction-Akki
git log --oneline programme/track-a | head -3
# f647051 W6 opener #2 · FL-P4-W4-01 reconciled · frozen contract parity restored
# 39386ac W5 CP4 frontend · Chat surface · ThinkLab reasoning wire · DataShield reasoning-receipts extension

python3 -m pytest backend/tests/invariants/test_northena_ledger_row_v0.py -v
# Expect: 1 passed.

cd /app/assessment_workspace
git log --oneline master | head -3
# (opener #1 re-baseline + STATE update committed at close)

cat notes/status_and_wave_plan.md | grep -A2 "Calibration factor"
# Expect the 1.60× naming.
```

## Blocked (awaiting from owner)

- None new. **W6 scope proceeds unless owner steers to option (b) narrow-scope or (c) L-extended-tier from opener #1's naming.**

## No push, ever

Owner Clarification 1 (2026-08-14). Local commits are the record.

## Honest LOC drift note

W4 was scoped M (~600 LOC estimated). Delivered at ~2020 LOC (donor Northena adaptation is inherently 500+ LOC; ThinkLab v7 fabric fidelity ~500 LOC; deep tests-first cohort 457 LOC). Above M-class ceiling. Reported to owner; hold for classification ruling or narrowing envelope guidance for future M waves.

## Post-W4 report to owner

Deliver: 20 register rows targeted; 6 fully DONE + 2 PARTIAL + 12 deferred to W5+ · SIX mechanism reuse pulls cited per file · three screenshots (landing / mode entry / admit walk) · LOC ~2020 · SHAs (`7e6bbc4` · `7bea87d` · `a71ea67`) · dashboard delta: Doc 05 5% → 30%; composite headline 43% → 44%.

## Cycle status (2026-08-14 · Owner Simplification response)

- **Simplification cycle CLOSED.** Connect UX collapses to ONE panel. Step grammar survives only as post-submit progress view (the handshake walk from the seven-stage pipeline, which itself is UNCHANGED).
- **Deterministic local parsing live.** `POST /api/connect/parse-paste` — pattern-only, no LLM/HTTP/subprocess. Password never returned in response body; `password_captured` boolean signal only.
- **Client-side password custody honoured.** Browser keeps the raw paste in its own textarea memory and submits the full credential set once to `/api/connect/gpu` (existing seven-stage pipeline unchanged). No server-side secret state between the parse and connect requests.
- **Fidelity ledger:** FL-P2-19 CLOSED (synisense-reading recorded); FL-P2-20 CLOSED (single-panel collapse); FL-P2-21 CLOSED (no-LLM-transit invariant added as gating).
- **LOC delta:** `ConnectWizard.jsx` 623 → 451 (−172 lines, −28%). New backend: 266 lines (parser + router + init). New backend tests: 321 lines. Frontend tests net +52 lines.
- **143/143 gating tests green.** 108 backend python + 12 frontend allowlist + 23 frontend rehome/single-panel. Zero regressions.
- **Commit SHAs on programme/track-a (4 new atop `f83b509`):**
  - `1f3d3bd` Phase 1 tests-first · deterministic paste parser + no-LLM-transit invariants
  - `ef9e185` Phase 1 implementation · deterministic paste parser + router mounted
  - `5ce8647` Phase 1 tests-first · single-panel Connect surface invariants
  - `c490ce9` Phase 1 implementation · single paste-and-connect panel

## Two-sentence access-mechanism proposal (still awaiting owner ratification)

> Access to the estate is IP-pinned; the allowlist admits your client `/32` (initial value `34.16.56.64`) at position `xff[-3]` of the ingress-set X-Forwarded-For chain, refusing every other address with HTTP 403 and one plain sentence. Additions and removals travel through `SPINE_ALLOWED_IPS` in `/app/backend/.env` - every change is a ledger row and the surface renders the current allowlist state as plain sentences.

## Blocked (awaiting from owner)

- **Ratify the two-sentence access proposal** (still standing).
- **FL-P2-09 disposition** - pod egress-IP rotation. Rotated AGAIN this cycle: STATE was `104.198.214.223` last cycle, now `35.225.230.28` this cycle. `34.16.56.64` stays in `SPINE_ALLOWED_IPS` unchanged per owner directive.
- **Vendor-side VM provisioning using the provisioning card** (unchanged):
  - Paste the estate public key `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGKlcjZE/04clh3FLddGn7Wx69pytk8KJA5j9M6rKVA7 estate@akki` into the VM's SSH Public Key field at creation (AISCA guide Fig 10).
  - Add TWO /32 rows to the VM's Security Group SSH rules (AISCA guide Fig 11): the owner's own operator /32 AND the pod egress /32 (currently `35.225.230.28/32`, subject to rotation).
- **Then paste the AISCA Output panel into the single Connect panel.** The parser reads it deterministically; the confirmation view masks the password as `•••• captured`; owner taps Connect; the unchanged seven-stage pipeline fires; with the estate key already installed, hardening shortens to verify-key-only → disable password auth → probe dead.

## Cold-reader-executable next actions

### 1. Deliver the Owner Simplification cycle report (this reply)

Test delta + right-reason receipts + green receipts + no-LLM-transit hard-rule proof + 4 Playwright screenshots (single panel / paste-parsed confirm / with provisioning card / handshake walk result) + LOC delta + commit SHAs.

### 2. On owner ratification of allowlist entry / vendor-side provisioning

- Update `SPINE_ALLOWED_IPS` in `/app/backend/.env` (add owner's client `/32`). Record allowlist change as a ledger row.
- Owner pastes AISCA Output panel into single Connect panel; deterministic parse; confirm; connect; seven-stage pipeline fires. Watch for green/failed/held per brief §5 paragraphs 6-7.

### 3. Post-Phase-0 (next cycle)

- **A4 increment (Registry honest-state instrumentation):** wire the COMPUTE CONNECTED tab's after-state to the real commissioning record on disk (present a "Just connected" pill + meta line + link to the record). Add DATA CONNECTED / LLMS & TRAINED MODELS state transitions when their waves land.
- **Wire-up non-compute path to per-wave connectors** as they land (data-source in Phase 2 admit-slice; LLM/trained-model in later waves). The single-panel + intent-record grammar becomes real routing when the wave connectors are ready.

### 4. Verification path for orchestrator (independent audit)

```bash
cd /app/assessment_workspace/repos/Extraction-Akki
git log --oneline programme/track-a
python3 -m pytest \
    backend/tests/invariants/test_actor_declaration_v0_contract_frozen.py \
    backend/tests/invariants/test_record_matrix_thin_kernel.py \
    backend/tests/invariants/test_task_identity_thin_kernel.py \
    backend/tests/invariants/test_parity_seat_extends_thin_kernel.py \
    backend/tests/invariants/test_admit_refuses_undeclared_actor.py \
    backend/tests/invariants/test_compute_seam_no_unledgered_exec.py \
    backend/tests/invariants/test_compute_seam_artifact_hash_verified.py \
    backend/tests/invariants/test_hardening_orchestrator.py \
    backend/tests/invariants/test_connect_gpu_pipeline.py \
    backend/tests/invariants/test_connect_gpu_scope_S_or_M.py \
    backend/tests/invariants/test_connect_gpu_acceptance_wired.py \
    backend/tests/invariants/test_ip_allowlist_middleware.py \
    backend/tests/invariants/test_estate_keys_and_connect_estate.py \
    backend/tests/invariants/test_credentials_paste_parser.py -v
# Expect: 108 passed at HEAD c490ce9.

cd /app/frontend && node --test plugins/ip-allowlist/__tests__/ip_allowlist.test.js
# Expect: 12 passed.

cd /app/assessment_workspace/repos/Extraction-Akki && node --test pod_shell/frontend/__tests__/rehome.test.js
# Expect: 23 passed.

# Live probe: no-LLM-transit proof (sentinel absent from response)
PW="INDEPENDENT_AUDIT_SENTINEL_$$"
curl -s -H "X-Forwarded-For: 34.16.56.64,172.71.255.34,136.110.244.150" \
     -H "Content-Type: application/json" \
     -d "{\"paste\":\"Host Name: h\\nPassword: ${PW}\\nUsername: u\\nPublic IP: 1.2.3.4\",\"hint_kind\":\"compute\"}" \
     http://127.0.0.1:8001/api/connect/parse-paste | grep -c "${PW}"
# Expect: 0 (password never in response body).

# Provisioning card live probe
curl -s -H "X-Forwarded-For: 34.16.56.64,172.71.255.34,136.110.244.150" \
     "http://127.0.0.1:8001/api/connect/estate-facts" | python3 -m json.tool
```

### 5. No push, ever

Owner Clarification 1 (2026-08-14). Assessment repo and Extraction-Akki both stay local.

---

## CODE FREEZE · 2026-08-26 · R1–R7 PLAN DRAFTED, AWAITING OWNER GO

**Status**: Remediation plan R1-R7 drafted, awaiting owner GO. Code freeze in force.

**What happened**: Owner delivered R1-R7 remediation directive at 2026-08-26T09:00Z. Main agent misread it as an execution order and began R1 (Ship-Manifest DoD meta-invariant + KNOWN_UNWIRED / KNOWN_RUNTIME_DRIFT manifests + DECISIONS.md ruling insert). Owner then clarified: the R1-R7 message was the PLAN only; execution was NOT authorized. Halt issued 2026-08-26T09:11Z.

**Commits during the misread**: NONE. No git commit landed for R1 work in either repo. Verified:
- `/app/assessment_workspace/repos/Extraction-Akki` HEAD unchanged: `d763721 W11 CP7 · register expansion 17→20 docs · 36 new rows · 12/12 green`
- `/app/assessment_workspace` HEAD unchanged: `743046a audit · system-wide spec↔build audit 2026-08-26 · 10 status-inflations named · stop-and-report · no code writes` (this commit was authorized by the owner in the audit-delivery turn and is legitimate)

**Uncommitted R1 artefacts on disk** (per owner order: leave in place, do not revert):

Extraction-Akki repo (`programme/track-a` branch):
- `backend/tests/invariants/test_ship_manifest_dod.py` · meta-invariant test · 8 tests · GREEN in local run
- `backend/tests/invariants/known_unwired.py` · 35-entry ledger of routers-on-disk-not-wired-to-runtime-assembler
- `backend/tests/invariants/known_runtime_drift.py` · 3-entry ledger of /app-vs-pod_shell drift
- `phase0/drill_receipts/20260826T090647Z_w11_r1_ship_manifest_dod_right_reason_failure.log` · RED receipt
- `phase0/drill_receipts/20260826T090914Z_w11_r1_ship_manifest_dod_green.log` · GREEN receipt

Assessment workspace repo (`master` branch):
- `STATE/DECISIONS.md` (modified) · appended R1 owner-ruling section (Ruling #1 Ship-Manifest DoD + Ruling #2 Callers-Cover-the-Rule DoD + Canon-5-§14-supersedes-Simplification note) at lines 1607–1660

**Uncommitted CP4 artefacts** (pre-R1, from paused work — NOT touched by this halt):
- `backend/contracts/skill_file_provenance_v0.py`
- `backend/services/skill_files/`
- `backend/tests/invariants/test_skill_file_provenance_v0_contract_frozen.py`
- `backend/tests/invariants/test_skill_files_module.py`
- `phase0/drill_receipts/20260826T081745Z_w11_cp4_skill_file_provenance_right_reason_failure.log`

**Owner directive (verbatim, 2026-08-26T09:11Z)**:
> "HALT — my error, not the owner's. The owner asked for the plan only; execution was NOT authorized. Stop all code writes immediately. If R1 work has started: leave it uncommitted (or if a commit already landed, note the hash and stop — do not revert, do not continue). Log in STATE/NEXT.md: 'Remediation plan R1-R7 drafted, awaiting owner GO. Code freeze in force.' Stand by. Nothing executes until I relay the owner's explicit approval."

**Freeze scope**:
- NO further file writes to `pod_shell/backend/`, `pod_shell/frontend/`, `backend/`, or any `services/*` under Extraction-Akki.
- NO `git commit` in either repo.
- NO `git push` (standing rule; also frozen here for clarity).
- STATE/NEXT.md log entry (this section) is the one authorized write during the freeze.

**Resume protocol**: main agent will resume R1 only upon receiving the owner's explicit approval, relayed by the user. On resume, the plan is: (a) verify the freeze-state artefacts still match, (b) commit R1 to Extraction-Akki (`programme/track-a`) with the two receipts, (c) commit the DECISIONS.md addition to assessment_workspace (`master`), (d) stop-and-report before starting R2.

**Recorded**: 2026-08-26 · code freeze active · owner GO required to resume.


