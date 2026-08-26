# NEXT.md - Exact next actions

**Last updated:** 2026-08-26T10:00Z · **W10 RATIFIED · Standing at ready state** · Extraction-Akki HEAD `f101bd0` (programme/track-a) · master HEAD `f20ef51`.

## Cycle status (2026-08-26T10:00Z · W10 RATIFIED · no next wave booked)

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
