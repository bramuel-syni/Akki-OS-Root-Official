# W10 Close Report

**Wave**: W10 · Completion Wave · CP1 Ruling-1 firing drill + CP2 Grey Mirror mirage machinery (Canon 8 §15-§16 BUILD) + CP3 Watch drills + fitness accounting (Canon 8 §25-§28) + CP4 Reserved-Decisions panel (Canon 8 §19) + CP5 Witness fabric full signing (Canon 8 §9 + §33) + CP6 CA1-005 whitepaper drafter (Doc 14 §33) + CP7 Doc 14 §§23-25 24-row register expansion + CP8 Governance/Watch/Grey-Mirror frontends + CP9 authoritative composite recomputation & wave close.
**Owner ruling**: FULL GO 2026-08-26T04:20Z (verbatim ratifications R1-R7 in `STATE/DECISIONS.md`); interleaved fix R8 preview allowlist permissive-mode 2026-08-26T05:20Z; strict-flip R9 at wave close 2026-08-26T09:20Z.
**Wave open**: 2026-08-26T04:20Z (right after W9 CLOSE + R1-R7 ratifications).
**Wave close**: 2026-08-26T09:30Z.
**Extraction-Akki HEAD**: `programme/track-a` @ `d4ba30c` (CP8) → this close report + CP9 lock lands at next commit.
**Pod-shell HEAD** (`/app` main): `d4ba30c` (mirror synced at CP8).
**Assessment-master HEAD**: `a809fe7` (CP8) → this close report + strict-flip lands at next commit.
**Baseline at wave open**: `7027e16` (W9 CP5 · containment fabric).

---

## 1 · Bottom line

- **AUTHORITATIVE composite % (Owner correction #4 §12.4 · single recomputation replacing running number)**: **52.49 %**.
  - Mechanism corpus: **54.45 %** (280.4 / 515 · 109 DONE + 46 PARTIAL + 306 REUSABLE + 53 BUILD + 1 OPEN-SLOT).
  - Interface dimension: **47.93 %** (27.8 / 58 · 10 DONE + 2 PARTIAL + 34 REUSABLE + 12 BUILD).
  - Blend: 0.7 × 54.45 + 0.3 × 47.93 = 38.12 + 14.38 = **52.49 %**.
  - Computed by `tools/w10_cp9_composite_recompute.py` (deterministic pure computation · 32 delta entries · every delta anchored to a canon § + a commit SHA on programme/track-a).
  - Locked by pytest at `backend/tests/invariants/test_w10_cp9_composite_lock.py` (5/5 green · same-commit DoD extension applied to the composite dashboard).
- **261/261 W10 wave-close cohort GREEN** (43 test files · pytest) at `phase0/drill_receipts/20260826T091500Z_w10_wave_close_green.log`. All CP1-CP9 tests + all W7/W8/W9 CP tests + all frozen/parity tests · no regression.
- **32/32 CP8 frontend tests GREEN** (node --test · 25 substantive DOM/HTTP assertions + 7 backend endpoint tests) at `phase0/drill_receipts/20260826T083*.log`.
- **9 W10 checkpoints CLOSED** (CP1 → CP9). Ruling-1 precondition (b) demonstrated at CP1 · rendered live on Watch surface.
- **Contract parity 58 → 59** (WhitepaperDraft_v0 · same-commit DoD honored via CONTRACT_TO_SNAPSHOT map + hardcoded numeric assertion at composed_conclusion_v0_contract_frozen).
- **Preview allowlist strict-flip verified** (R9 · owner IP 41.90.172.155 admits · unknown IP refuses · no-XFF refuses · banked receipt `20260826T092000Z_w10_strict_flip_verified.log`).
- **Optional cheap fix landed**: `/api/openapi.json` now serves the FastAPI spec at 200 (49 paths · docs_url/redoc_url disabled · response-boundary sanitizer unchanged; OpenAPI reflects request-body field names by design — no runtime value leaks).
- **13 W10 commits** on programme/track-a from `19cb02c` (CP1) through `d4ba30c` (CP8) plus CP9 close commit pending.

---

## 2 · Per-CP summary

| CP | Scope | Test cohort | Commit SHA | LOC (net) |
|----|-------|-------------|------------|----------:|
| CP1 | Ruling-1 firing drill · Canon 8 §27 | 7/7 pytest | c9a26cc | ~200 |
| CP2 | Grey Mirror mirage machinery · Canon 8 §15-§16 · BUILD not LIFT | 25/25 pytest · parity 52→55 | a027caf | ~800 |
| CP3 | Watch drills + fitness accounting · Canon 8 §25-§28 · §32.8 no-self-cert | 12/12 pytest | 4a1f942 | ~400 |
| CP4 | Reserved-Decisions panel · Canon 8 §19 · §32.6 no machine execution | 28/28 pytest · parity unchanged | a3caba9 | ~500 |
| CP5 | Witness fabric full signing · Canon 8 §9 + §33 · CA1-N5 | 23/23 pytest · parity 55→58 | 3bca4a8 | ~600 |
| CP6 | CA1-005 whitepaper drafter · Doc 14 §33 · BUILD not LIFT · 150-LOC lid honored | 13/13 pytest · parity 58→59 | b5575bc | ~140 |
| CP7 | Doc 14 §§23-25 24-row register expansion · docs-only | 8/8 pytest · parity unchanged | d46e84e | ~130 register lines + 152 test LOC |
| CP8 | Governance / Watch / Grey-Mirror frontends + backend state rollups | 7/7 pytest + 25/25 node · parity unchanged | d4ba30c | ~940 |
| CP9 | Authoritative composite % recomputation + lock + wave close + strict flip | 5/5 pytest · 261/261 wave-close cohort | this commit | ~230 |

Interleaved fix (2026-08-26T05:20Z): preview allowlist owner-access path (R8) — 33/33 backend + 26/26 frontend tests · `_ip_allowlist_owner_access_green.log` banked. Reverted to strict at wave close per R9.

---

## 3 · Register rows lit (net moves crediting W10)

### Canon 8 (Doc 03 · Watch) — largest single-doc move this wave

| Row | Anchor | Status | CP |
|-----|--------|--------|-----|
| Grey Mirror mirage machinery (5 rows) | Canon 8 §15-§16 | BUILD → DONE | CP2 |
| Watch drills · standing drill harness | Canon 8 §25-§26 | BUILD → DONE | CP3 |
| Fitness accounting · §32.8 no-self-cert | Canon 8 §27-§28 | BUILD → DONE | CP3 |
| Reserved-decisions Panel | Canon 8 §19 + §32.6 | BUILD → DONE | CP4 |
| Witness identity + attestation + tamper alarm (3 rows) | Canon 8 §9 + §33 | BUILD → DONE | CP5 |
| Ruling-1 firing drill demonstration | Canon 8 §27 | BUILD → DONE | CP1 |

### Doc 14 (Model Ecosystem · Baseline · Whitepaper)

| Row | Anchor | Status | CP |
|-----|--------|--------|-----|
| Doc14-024 · CA1-005 whitepaper drafter | Doc 14 §33 | BUILD → DONE | CP6 |
| Doc14-002..007 · Critic Seam quartet + Quarantine + Adapter registry | Canon 4 §21-§25 | (register named · BUILD) | CP7 |
| Doc14-008..014 · MOAC 6-criterion card | Canon 4 §26 | (register-named DONE · anchored to W7 CP4 build) | CP7 |
| Doc14-015 · uncurated evidence discipline | Canon 4 §27 | (register-named DONE) | CP7 |
| Doc14-016 · training-lineage-resolved | Canon 4 §28 | (register-named DONE) | CP7 |
| Doc14-017 · adapter versioning history | Canon 4 §29 | (register-named PARTIAL) | CP7 |
| Doc14-018, 019, 025 · Standards + Rights + Frozen-objective | Canon 4 §36, §37, §43 | (register-named REUSABLE) | CP7 |
| Doc14-020 · rights-unclear grammar | Canon 4 §38 | (register-named OPEN-SLOT · owner-policy pending) | CP7 |

### Iface / surfaces

| Surface | Anchor | Status | CP |
|---------|--------|--------|-----|
| Reserved-Decisions Panel | Canon 8 §19 | BUILD → DONE | CP8 (Governance.jsx) |
| Watch destination | Canon 8 §7-§28 | BUILD → DONE | CP8 (Watch.jsx) |
| Grey Mirror overview | Canon 8 §15-§16 | BUILD → DONE | CP8 (GreyMirror.jsx) |
| Rules Updates ceremony (re-confirmation) | Doc 15 §17 | BUILD → DONE | CP8 (Governance.jsx) |
| Cost Ledger (built earlier · re-confirmed) | Doc 11 | BUILD → DONE (already banked) | CP8 |

---

## 4 · Fidelity ledger — no new rows opened at W10

- **FL-P4-W8-01** (CA1-N2/N3 policy answers · opened W8) · **STILL OPEN** · non-blocking to wave close.
- **FL-P4-W9-01** (CA1-N5-q1 policy answer · opened W9) · **STILL OPEN** · non-blocking.
- **FL-P4-W7-02** (pod-shell + spine same-commit mount DoD) · **RESPECTED** across all W10 CPs · continues to hold.
- **FL-P4-W8-02** (contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD) · **RESPECTED** at CP5 (parity 55→58) + CP6 (parity 58→59) · continues to hold.
- **FL-P4-W9-02** (post-compaction re-read discipline) · **RESPECTED** at every session boundary this wave.
- **NEW policy-slot booked (not a new fidelity row · booked in requirements register)**:
  - **Doc14-020 · Canon 4 §38 rights-unclear grammar** · OPEN-SLOT · same N-series pattern as CA1-N2/N3/N5 · non-blocking to W10 close.
- **NO regressions** on pre-existing FL-P4-W6-01..07 environmental pydantic 2.13.4 serialization drift class · scope unchanged (48 collection errors + 30 test failures continue to be documented pre-existing state · none touched by W10 additions).

---

## 5 · Same-commit DoD checkpoints (audit trail)

- **Parity same-commit DoD (FL-P4-W8-02)** honored at:
  - CP2 · a027caf · parity 52→55 (Mirage_v0 + MirageTouch_v0 + Severance_v0 + snapshots + map + hardcoded count).
  - CP5 · 3bca4a8 · parity 55→58 (WitnessIdentity_v0 + WitnessAttestation_v0 + TamperAlarm_v0 + snapshots + map + hardcoded count).
  - CP6 · b5575bc · parity 58→59 (WhitepaperDraft_v0 + snapshot + map + hardcoded count).
- **Pod-shell same-commit mount DoD (FL-P4-W7-02)** honored at:
  - CP5 (services.watch.witness + tests-first).
  - CP8 · d4ba30c (three routers + three components + App.js wire + pod_shell mirror sync in one commit).

---

## 6 · Interleaved fixes & queries answered informationally

- **Preview allowlist owner-access path** (R8 · 2026-08-26T05:20Z) — 33/33 backend + 26/26 frontend tests · permissive mode for W10 duration only · rescinded R9 at wave close · strict flip verified.
- **Audio-trainer × GPU readiness query** (2026-08-26T08:20Z) — answered from ground truth · audio trainer NOT BUILT · perception-side ASR/diarisation wired but no training pipeline · GPU connect real 7-stage but currently points at mock SSH · trainer deferred beyond W10 (rough envelope W10-scale wave of its own · 5-7k LOC). Informational only · no CP scope change.

---

## 7 · Composite % — authoritative recomputation basis (Owner correction #4)

**Method (declared once · matches `notes/status_and_wave_plan.md` §1 + §5)**:
- Weights: DONE=1.0 · PARTIAL=0.4 · REUSABLE=0.5 · BUILD=0.0 · OPEN-SLOT=0.0 (new W10 CP7 status treated as BUILD-weight — policy-pending is not "done").
- Mechanism corpus: 515 rows across 16 canon docs + addendum. Mechanism % = weighted / 515.
- Interface dimension: 58 v7 surfaces (from `notes/status_and_wave_plan.md` §4). Interface % = weighted / 58.
- Composite = 0.7 × mechanism % + 0.3 × interface %.

**Delta enumeration** (32 entries · every entry cites canon anchor + commit SHA). Live enumeration in `tools/w10_cp9_composite_recompute.py::DELTAS`. Summary:

| Wave | mech-side deltas | iface-side deltas | rows net moved |
|------|-----------------:|------------------:|---------------:|
| W7 | 5 delta entries · Doc 13/14 · model_admission ceremony + baseline_line + rights lineage | 1 · Model Admission ceremony | 25 mech + 1 iface |
| W8 | 6 · Doc 15 governance ceremony + CA1-009 + N-series scaffolding + Trace | 1 · Rules Updates ceremony | 14 mech + 1 iface |
| W9 | 5 · Watch verdict/action seam + CA1-011 + CA1-012 + CA1-N5 + containment | 0 | 12 mech |
| W10 | 10 · Ruling-1 drill + Grey Mirror + drills/fitness + reserved-decisions + witness fabric + whitepaper + Doc 14 register expansion (4 sub-entries) | 4 · Governance + Watch + Grey Mirror + Cost Ledger re-confirmation | 28 mech + 4 iface |
| **Totals** | **26 entries · 79 rows** | **6 entries · 6 surfaces** | **79 mech + 6 iface** |

**Baseline (W6 close) → Post-W10 (authoritative)**:

| Bucket | W6 baseline mech | Post-W10 mech | W6 iface | Post-W10 iface |
|--------|-----------------:|--------------:|---------:|---------------:|
| DONE | 47 | **109** | 4 | **10** |
| PARTIAL | 40 | **46** | 2 | **2** |
| REUSABLE | 300 | **306** | 34 | **34** |
| BUILD | 128 | **53** | 18 | **12** |
| OPEN-SLOT | 0 | **1** | 0 | **0** |
| Total | 515 | 515 | 58 | 58 |
| Weighted | 213.0 | **280.4** | 21.8 | **27.8** |
| Percent | 41.4 % | **54.45 %** | 37.6 % | **47.93 %** |

**Composite (blended)**: **52.49 %** post-W10 · up from 40.3 % at W6 close · net +12.19 percentage points across W7-W10.

The wobbly running numbers (43 % → 46 % → 48 % → 43 % → 48 %) are now superseded by this ONE recomputation. Future waves that touch the calc must move `tools/w10_cp9_composite_recompute.py` + `test_w10_cp9_composite_lock.py` in the SAME commit (same-commit DoD extension applied to the composite dashboard).

---

## 8 · Preview surface — routes owner should eyeball

Live under strict allowlist (post-R9 flip) via owner IP `41.90.172.155`:

- `/` — Registry (unchanged)
- `/data` — DataShield (unchanged)
- `/think` — ThinkLab (unchanged)
- `/chat` — Chat (unchanged)
- `/cost-ledger` — CostLedger (unchanged · re-confirmed DONE at W10 CP8)
- `/models` — ModelEcosystem (built W7 CP7 · Model Admission ceremony surface · mirrored to pod_shell at W10 CP8)
- **`/governance`** — Reserved-Decisions Panel + Rules-Updates Timeline + Approvals Ledger (W10 CP8)
- **`/watch`** — Fitness Summary + Verdicts + Actions + Containments + Witness + Tamper Alarms + Ruling-1 precondition (b) DEMONSTRATED (W10 CP8)
- **`/grey-mirror`** — Mirages + Touches + Severances + BUILD-not-LIFT rationale (W10 CP8)
- **`/api/openapi.json`** — FastAPI spec for tester contract discovery (W10 CP9 optional fix)

Honest empty state: all live watch/mirage/severance/approval stores return count=0 today (no production traffic has fired the fabric yet · surfaces render the honest sentence "0 X on record · Canon anchor: … · Drawn, never left blank.").

---

## 9 · Outstanding items (deferred beyond W10)

**Non-blocking policy answers (unchanged from W8/W9)**:
1. **FL-P4-W8-01** · CA1-N2 (data-subject breach notification) · owner policy pending (7 questions).
2. **FL-P4-W8-01** · CA1-N3 (data-subject erasure) · owner policy pending (7 questions).
3. **FL-P4-W9-01** · CA1-N5 (continuity attestation) · owner policy pending (1 question).

**New at W10**:
4. **Doc14-020 · Canon 4 §38 rights-unclear grammar** · OPEN-SLOT · same N-series pattern · non-blocking.

**Larger post-W10 work (informational only · not booked)**:
5. **Audio trainer + real GPU wiring** · answered informationally 2026-08-26T08:20Z. Audio trainer NOT BUILT (perception-side wired but no training pipeline). GPU connect real 7-stage but currently `.env` points at mock SSH. Building the trainer is roughly a wave of its own (~W10-scale · 5-7k LOC).

---

## 10 · What the honest surface reveals now

Under strict allowlist with owner IP admitted:

- **Watch fabric is fully-wired · but has never fired against real traffic**. Empty stores + demonstrated drill (Ruling-1 precondition b). This is the honest state: mechanism ready · exercise pending.
- **Grey Mirror is fully-wired · no mirages installed**. touch_kind grammar CONTRACT-TIME closed to `{innocent_read, guilty_use}` (R2). Mirage installation and severance ceremony deferred to first-live event.
- **Approvals fabric is fully-wired · no requests on record**. Rules Updates lifecycle countdowns not fired · Reserved-Decisions panel empty · Spend-requests panel empty.
- **Model Ecosystem** admits real models (7 Emergent Universal models seeded at W7 CP3) and enforces MOAC 6-criterion + uncurated-sample discipline + rights-lineage.
- **Whitepaper drafter** enforces §33 CITATION invariant + §43 append-only. No whitepapers on disk (no training runs on disk).
- **Trace surface** and **Governance timeline** ready · not yet lit by real approval events.

The system is honest about its empty state. Nothing is fabricated. Every surface says exactly what is on disk · nothing more · nothing less.

---

## 11 · Next-wave inputs (if owner opens W11)

If W11 opens the surface goes from "mechanism ready" to "mechanism fires against real traffic":
- **Land the 9 non-blocking policy answers** (CA1-N2/N3/N5 + Doc14-020 §38) to lift the open-slots to config.
- **Fire the first live watch verdict** (real deployment traffic) to lift the mirage → mirage-touch → severance chain from theory to record.
- **Fire the first real rules-updates ceremony** (countdown + apply + re-check) to lift the governance timeline from empty to lit.
- **Wire real GPU credentials** into `.env` (flip from `/tmp/akki_mock_sshd/*` to production host).
- **Build the audio trainer** (post-W10 scope · ~W10-scale wave of its own if pursued).

None of these are booked. All defer to the owner.

---

## 12 · Wave-close checklist verification

- [x] CP9 authoritative composite computed + locked by pytest.
- [x] 261/261 wave-close cohort green (43 test files).
- [x] Allowlist strict-flip verified (owner admits · unknown refuses).
- [x] Flip logged as R9 owner ruling in STATE/DECISIONS.md.
- [x] W10 close report banked (this file · `notes/w10_close_report.md`).
- [x] STATE/NEXT.md updated (CP9 CLOSED entry · outstanding items enumerated).
- [x] STATE/CONTEXT.md updated (next wave inputs enumerated).
- [x] Optional /api/openapi.json fix landed (cheap · verified).
- [x] All commits local · no push (Owner Clarification 1 · 2026-08-14).

W10 CLOSED · **52.49 % composite (authoritative)**.
