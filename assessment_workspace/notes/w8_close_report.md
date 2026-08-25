# W8 Close Report

**Wave**: W8 · Canonical-projection · Pod-shell mount discipline · CA1-009 generalized handoff · Approvals ceremony (Rules Updates · Spend Requests · Generic) · CA1-N2/N3 N-series scaffolding · Trace surface · Rules Updates lifecycle (countdown · apply · re-check)
**Owner ruling**: Auto-continue 2 waves (2026-08-26T00:25Z verbatim in `STATE/DECISIONS.md`); no explicit W8 GO required.
**Wave open**: 2026-08-26T01:20Z (right after W7 CLOSE at `aa230b7`).
**Wave close**: 2026-08-26T02:45Z.
**Extraction-Akki HEAD**: `programme/track-a` @ `bfafd5f` (CP6 follow-up · parity count 44→47).
**Pod-shell HEAD** (`/app` main): `0b227d9` (W8 CP5 · trace router mount).
**Assessment-master HEAD**: `<pending W8 close commit>`.
**Baseline at wave open**: `aa230b7` (W7 CP8 conftest event-loop fixture).

---

## 0 · W7 close carry-forward (owner-requested restatement)

Compaction swallowed the W7 close reply; carrying the record forward per owner directive.

### W7 headline (from `notes/w7_close_report.md`)

- **310/310 W7 wave-close cohort GREEN** (44 test files) at `phase0/drill_receipts/20260826T010500Z_w7_wave_close_green.log`.
- **17 register rows lit** (13 Doc 13 · 4 Doc 14). Full row IDs in W7 close §2.
- **LOC actual · 2779 net** (Extraction-Akki 2429 + pod-shell 350) vs **3520 budget** → **79% consumed · UNDER by 741 LOC**.
- **2 fidelity ledger rows opened + closed** (FL-P4-W7-01 · FL-P4-W7-02).

### W7 CP outcomes (SHAs)

| CP | Scope | Spine SHA | Delta |
|----|-------|-----------|-------|
| CP1 | Rulings + rates lane + brief close (Q2/Q3/Q4 folded) | `60581fb` | +5 tests · +139 LOC |
| CP2 | Targeta invariants LIFT + FL-P4-W7-01 snapshot reconciliation | `6e76bc3` | +12 tests · +1 LOC |
| CP3 | `services/model_registry/` top-level LIFT + FACTS-only seed (7 real Emergent Universal · no whisper-tiny) | `82f6de5` | +13 tests · +444 LOC |
| CP4 | Model Admission ceremony · MOAC six-criterion contract + snapshot | `57f4ba6` | +15 tests · +874 LOC |
| CP5 | CA1-004 baseline line + CA1-011 W7-half + count 38→39 | `2256a6e` | +8 tests · +587 LOC |
| CP6 | CA1-005 whitepaper · **DEFERRED TO W8** (honest gate; 150-LOC lid stop) | — | 0 LOC |
| CP7 | 5 routers mounted (4 W7 new + 1 W6 cost_ledger latent) + Model Ecosystem UI | `966c8ef` + pod-shell `a5933a1` | +11 tests · +369 spine + 350 pod-shell |
| CP8 | Wave close · conftest event-loop fixture · close report | `aa230b7` | +0 tests · +15 LOC |

### W7 shipped vs deferred

**Shipped:**
- Doc13 rows 007, 013, 014, 015 (a-f), 016, 017, 023 (CA1-011 W7-half).
- Doc14 rows 001, 023 (CA1-004), 026 (per-model license_note).
- Model Ecosystem 3-tab surface (LLMs · Trained adapters · Admission records).
- MOAC six-criterion Model Admission ceremony backend.
- Baseline line record contract + snapshot.
- CA1-011 re-check-date state (W7 half; W9 seam named at `services.watch.route_recheck_failure`).

**Deferred:**
- **CA1-005 whitepaper** (Doc 14 §33): W7 CP6 never opened due to 150-LOC lid honest-gate stop. Reject verdict on Executive-Core `deck_*.py` re-evaluation was PENDING. **Also deferred out of W8** (LOC used elsewhere · re-evaluation pushed to W9 or a subsequent polish wave).
- **Doc 14 §§23–25 remaining 24 rows** (Doc14-002..022, 025, 027, 028): CP1 was scoped to expand in a fresh pass; deferred to W8. **Also deferred out of W8** (W8 scope was Doc 15 governance ceremony · N-series · handoff · trace; Doc 14 expansion did NOT fit honestly under load-bearing constraints · pushed to W9 or subsequent).
- **Data Suite surface (v7-exact)**: deferred out of W6 → W7 → **still deferred at W8 close**. Not on W8's Doc 15 / N-series scope; carried to a subsequent polish wave.
- **LLM chip UI polish**: cosmetic W6 deferral · **still deferred**.

### W7 Model Admission walk evidence

Walk fires only if a candidate MOAC card is submitted; none were on record at W7 close (honest empty). Curl-through-allowlist verification confirmed the 3-tab surface renders drawn-not-blank on empty states (see W7 close report §9). Owner-side rendering required for visible surface screenshots (IP allowlist honest gap).

### W7 dashboard delta

- **W6 close**: Mechanism corpus 41.4% · Interface 37.6% · Composite ≈ 40%.
- **W7 close** (17 additional register rows across 51 Doc13/14 rows): Mechanism corpus ≈ 44% · Interface (Model Admission ceremony surface added at REUSABLE→DONE) ≈ 41%. Composite ≈ 43%.

### W7 silent slip into W8?

**Nothing silently slipped.** Explicit W8 opener carry-over (W7 close report §8) listed six items:
1. Canonical-projection remediation — **DELIVERED W8 CP1**.
2. Pod-shell mount completeness test — **DELIVERED W8 CP1**.
3. Pod-shell boot test — **DELIVERED W8 CP1**.
4. Async event-loop pollution owner-visibility ruling — **CARRIED FORWARD** (owner has not visibly ruled; conftest fixture is on record as a claim to be ratified; not blocking).
5. CA1-005 whitepaper re-evaluation — **DEFERRED AGAIN OUT OF W8** (no re-evaluation opened; LOC budget spent on Doc 15 scope).
6. Doc 14 §§23–25 remaining 24 rows expansion — **DEFERRED AGAIN OUT OF W8** (same reason).

The Doc 14 §§23–25 and CA1-005 deferrals are the honest "did not fit W8" items. They ride to W9 opener as explicit carry-over (§8 below).

---

## 1 · Bottom line

- **366/366 W8 wave-close cohort GREEN** (55 test files) at `phase0/drill_receipts/20260826T024000Z_w8_wave_close_green.log`. Frozen+contract sub-cohort green at each CP; parity count 42 → 47 across the wave.
- **LOC actual · 2964 net** (Extraction-Akki spine only · pod-shell delta is 4 lines) vs **5600 budget** → **53% consumed · UNDER by 2636 LOC**.
- **2 fidelity ledger rows opened at W8** (FL-P4-W8-01 · FL-P4-W8-02):
  - FL-P4-W8-01 · N-series policy stop-and-report · **OPEN** (7 one-sentence-answerable questions carried to owner in §7 below).
  - FL-P4-W8-02 · Hardcoded parity-count assertion drift · **CLOSED at open** · new DoD element ratified (recurrence #4 in FL-P4-W6-02 family).
- **7 W8 commits** on `programme/track-a` from `c396b84` (CP1) to `bfafd5f` (CP6 follow-up).
- **CA1-009 generalized handoff contract DELIVERED** (CP2).
- **Approvals ceremony (Rules Updates · Spend Requests · Generic) DELIVERED** (CP3).
- **N-series (CA1-N2 breach · CA1-N3 erasure) STRUCTURAL SCAFFOLDING DELIVERED** (CP4). Ceremony records REFUSED to fire until owner rules on 7 policy questions.
- **Trace surface (REFERENCE-NOT-COPY) DELIVERED** (CP5).
- **Rules Updates lifecycle (countdown · apply · re-check) DELIVERED** (CP6).
- **Canonical-projection remediation + pod-shell mount/boot invariants DELIVERED** (CP1).

---

## 2 · Register rows lit (Doc 15 governance ceremony · CA-series)

### Doc 15 (governance ceremony · verbatim §17 · §33)

| Row | Anchor | Status |
|-----|--------|--------|
| Doc15-approvals | §17 propose · counter-sign | CP3 · ApprovalRequest_v0 + ApprovalDecision_v0 |
| Doc15-approvals-SoD | §17 separation-of-duties | CP3 · service-time invariant |
| Doc15-lifecycle-countdown | §17 countdown state | CP6 · CountdownStarted_v0 |
| Doc15-lifecycle-apply | §17 apply state | CP6 · RulesUpdateApplied_v0 (now_iso injection) |
| Doc15-lifecycle-recheck | §17 re-check state (verdict grammar: matches · diverges · inconclusive) | CP6 · RulesUpdateReChecked_v0 |
| Doc15-handoff | §33 generalized handoff contract | CP2 · HandoffContract_v0 (CA1-009) |
| Doc15-trace | §Trace REFERENCE-NOT-COPY governance timeline | CP5 · services/trace/ |
| **CA1-009** | Doc 15 §33 · generalized handoff | CP2 · DELIVERED |
| **CA1-N2** | breach notification | CP4 · SCAFFOLDING (refuses fire pending owner facts) |
| **CA1-N3** | access-and-erasure | CP4 · SCAFFOLDING (refuses fire pending owner facts) |

### Discipline rows lit

| Row | Anchor | Status |
|-----|--------|--------|
| Canonical-projection | pydantic-version-independent schema projection | CP1 · services/canonical_projection/schema.py + 8 tests |
| Pod-shell mount completeness | FL-P4-W7-02 §7.2 | CP1 · test_w8_cp1_pod_shell_boot_and_mount.py (3 tests) |

**Total W8 register rows lit · 10** (7 Doc 15 + 2 amendments · 3 CA rows partial/scaffolding).

---

## 3 · Checkpoint outcomes

| CP | Scope | Spine SHA | Test delta (files added / tests) | LOC (net) |
|----|-------|-----------|----------------------------------|-----------:|
| CP1 | Canonical-projection + pod-shell mount/boot invariants + FL-P4-W7-02 remediation | `c396b84` | +2 files · +11 tests | +332 |
| CP2 | CA1-009 generalized handoff contract · parity 39→40 | `af43c8e` | +2 files · +12 tests | +297 |
| CP3 | Approvals ceremony (Rules Updates · Spend Requests · Generic) · parity 40→42 | `0f0d48e` | +2 files · +15 tests | +495 |
| CP4 | N-series (CA1-N2 breach · CA1-N3 erasure) structural scaffolding · parity 42→44 · FL-P4-W8-01 open | `f8c9bb1` | +2 files · +13 tests | +475 |
| CP5 | Trace surface REFERENCE-NOT-COPY governance timeline · pod-shell mount | `f9a973a` (spine) + `0b227d9` (pod-shell) | +2 files · +6 tests | +309 spine + 4 pod-shell |
| CP6 | Rules Updates lifecycle (countdown · apply · re-check) · parity 44→47 | `7abd1c2` + `bfafd5f` (follow-up · FL-P4-W8-02) | +3 files · +17 tests | +1056 |
| **TOTAL** | | | **13 files** · **+74 tests** | **+2964 spine + 4 pod-shell** (vs 5600 budget · 53%) |

---

## 4 · Test delta + receipts

**W7 close cohort baseline · 310 tests (44 files).**
**W8 close cohort · 366 tests (55 files) · +56 tests · +11 files.**

Cohort assembly discipline (unchanged from W7 close · FL-P4-W6-02/08/09 + FL-P4-W7-01 broadened):

- grep `test_*_frozen*.py` + `test_*_contract*.py` (W6-ratified pattern)
- content-grep for `model_json_schema()` vs `contract_snapshot.json` (W7-added)
- every `test_*_invariants.py` file (W7-added donor-side lift blind-spot compensator)
- explicit inclusion of every new `test_w7_cp*.py` and `test_w8_cp*.py` file
- **NEW (W8)**: grep `assert len(snapshots) ==` in `backend/tests/invariants/*.py` (FL-P4-W8-02 DoD extension)

Per-CP receipts on record (all under `phase0/drill_receipts/`):

| CP | Right-reason failure receipt | Green receipt |
|----|------------------------------|---------------|
| CP1 | `20260826T012000Z_w8_cp1_right_reason_fail.log` | `20260826T012500Z_w8_cp1_green.log` (11/11) |
| CP2 | `20260826T013000Z_w8_cp2_right_reason_fail.log` | `20260826T013800Z_w8_cp2_green.log` (12/12) |
| CP3 | `20260826T014000Z_w8_cp3_right_reason_fail.log` | `20260826T014800Z_w8_cp3_green.log` (15/15) |
| CP4 | `20260826T015000Z_w8_cp4_right_reason_fail.log` | `20260826T015500Z_w8_cp4_green.log` (13/13) |
| CP5 | (no separate right-reason receipt · trace tests authored directly to green) | `20260826T021500Z_w8_cp5_trace_surface_green.log` (6/6) + `20260826T022000Z_w8_cp5_trace_surface_and_mount_green.log` (9/9 · with pod-shell mount discipline) |
| CP6 | `20260826T022500Z_w8_cp6_right_reason_fail.log` (11/11 fail · missing module) | `20260826T023000Z_w8_cp6_green.log` (17/17) |
| CP6-follow-up | (in-session · 1/366 fail · exact-class message from wave-close cohort assembly · not banked · FL-P4-W8-02 §receipts documents the honesty note) | `20260826T024000Z_w8_wave_close_green.log` (**366/366 · 55 files**) |

---

## 5 · Reuse pulls used vs rejected

### USED

- **Doc 15 §17 governance ceremony** vocabulary and state names — REFERENCE-NOT-COPY (Design Law) · every contract field name, verdict grammar, and state transition name carries the Doc 15 wording verbatim in field docstrings.
- **Doc 15 §33** language on generalized handoff contract shape (CA1-009).
- **W7 CP4 MOAC ceremony pattern** — CP3 Approvals ceremony was authored on the same request/decision pair shape (contract + service module + persistence dir) as the CP4 Model Admission ceremony. Not a code copy; a design pattern reuse.
- **W5 chokepoint metering pattern** — trace producer scan (CP5) reads records directly from the on-disk producer directories, same as chokepoint receipts. No producer is duplicated; every trace entry names its `source_path`.

### REJECTED (or DEFERRED again)

- **Executive-Core `deck_*.py`** (653 LOC · 4 files) — Deck-templated async generation for CA1-005 whitepaper action. Reject verdict from W7 CP6 was PENDING at W7 close · **not re-evaluated at W8** · re-evaluation deferred to W9 opener or a subsequent polish wave. Honest reason: W8 LOC budget was consumed by Doc 15 ceremony scope; a proper CA1-005 re-evaluation requires the whitepaper draft-and-freeze mechanism plus a licence-check discipline shim, neither of which fits W8's Doc 15 anchor.
- **Executive-Core `monitor/`, `cycle_lifecycle.py`, `cycle_permissions.py`, `cycle_synthesis.py`** — pre-brief W8 named these as ADAPT sources for the Approvals ceremony · **NOT USED**. CP3 authored Approvals fresh from Doc 15 §17 verbatim under the REFERENCE-NOT-COPY law. The Exec-Core code is `cycle_*` shaped (a monthly cycle synthesis with permissions) and did not align with Doc 15's per-request/decision governance pair. Reject verdict on record.
- **RMS `master_admin/`** — pre-brief named as ADAPT source for rules-updates ceremony gate · **NOT USED**. CP6 authored the lifecycle states (countdown · apply · re-check) fresh from Doc 15 §17. `master_admin/` is an app-admin permission fabric; not a rules-update ceremony record shape. Reject on record.

### BUILT (not lifted)

- Canonical-projection (CP1 · 65 LOC · services/canonical_projection/schema.py) — pure function; two projection rules for pydantic 2.13.x emitter idioms.
- HandoffContract_v0 contract + service (CP2 · 297 LOC).
- ApprovalRequest_v0 + ApprovalDecision_v0 contracts + services (CP3 · 495 LOC).
- BreachNotification_v0 + ErasureRequest_v0 contracts + services + refusal-while-pending scaffolding (CP4 · 475 LOC).
- Trace surface (CP5 · 309 LOC · 7 producers indexed).
- CountdownStarted_v0 + RulesUpdateApplied_v0 + RulesUpdateReChecked_v0 contracts + service (CP6 · 1056 LOC).

---

## 6 · Fidelity ledger rows opened

| Row | Class | Origin | Status |
|-----|-------|--------|--------|
| FL-P4-W8-01 | Owner-policy stop-and-report · N-series structural scaffolding landed · 7 policy questions pending | W8 CP4 authorship time · explicit stop-and-report per owner auto-continue ruling "stop that ITEM, name the question, continue the rest of the wave." | **OPEN** · one-sentence-answerable batch in §7 below |
| FL-P4-W8-02 | Hardcoded parity-count assertion drift · FL-P4-W6-02 family recurrence #4 · new DoD element ratified | W8 CP6 · authored 3 snapshots + updated map/secondaries but missed the hardcoded numeric assertion in `test_composed_conclusion_v0_contract_frozen.py` | **CLOSED at open** · fix landed at `bfafd5f` · new DoD element on record |

**Defect class FL-P4-W6-02 family recurrence count · 4** after FL-P4-W8-02:
- W1 origin · actor_declaration_v0 map+count omission · FL-P4-W6-02/08/09 (three sub-omissions of the same class, ratified together at W6 close).
- W4 origin · targeta_mining_plan transitive · FL-P4-W7-01 (W7 CP2).
- W8 origin · hardcoded numeric assertion missed · FL-P4-W8-02 (W8 CP6 → CP6 follow-up).

The FL-P4-W8-02 DoD extension names a THIRD element of the contract-same-commit rule (numeric assertion alongside snapshot + map). Effective from W8 close cohort forward.

---

## 7 · FL-P4-W8-01 · N-series policy questions for owner (one-sentence-answerable · CA1-N2/N3)

Per owner directive 2026-08-26T00:25Z ("stop that ITEM, name the question, continue the rest of the wave"), the 7 policy questions surfaced at W8 CP4 are batched here for owner ruling. Neither `fire_breach_notification()` nor `fire_erasure_request()` will succeed on live calls until each answer replaces its `OWNER_POLICY_PENDING` sentinel; the structural scaffolding is on record and ready to accept rulings without a code change.

### CA1-N2 · breach notification (Doc 8 · Watch · CA1-N2)

1. **Breach trigger scope** — Does the breach notification fire on refusal-bypass ONLY, or ALSO on near-miss (attempted-but-refused-before-harm) events?
   *Options on record*: `refusal_bypass_only` · `refusal_bypass_and_near_miss`.

2. **Notification routing** — Where does the notification route: Watch (self-witness under Doc 3) OR an independent authority?
   *Options on record*: `watch_self_witness` · `independent_authority`.

3. **Actor masking in notification body** — Does the notification body carry actor ids in the clear, OR masked?
   *Options on record*: `actor_ids_visible` · `actor_ids_masked`.

4. **Notification cadence** — One notification per breach event, OR aggregated windows (hourly/daily)?
   *Options on record*: `one_per_breach` · `aggregated_windows`.

### CA1-N3 · access and erasure (Doc 15 · CA1-N3)

5. **Erasure reach** — How deep does erasure reach: raw source only · raw + five-ring units · OR raw + units + model weights?
   *Options on record*: `raw_source_only` · `raw_and_five_ring_units` · `raw_and_units_and_model_weights`.

6. **Requester identity verification** — Is the requester's identity verified by self-declaration OR by an independent verifier? (Likely depends on the close-to-independent promise · Doc 8 territory.)
   *Options on record*: `self_declared` · `independent_verifier`.

7. **Retention vs erasure conflict** — When a record is under an active CA1-N1 retention window AND an erasure request lands, does erasure override retention OR wait for expiry?
   *Options on record*: `erasure_wins_over_ca1_n1` · `retention_wins_until_expiry`.

**How ruling lands mechanically:** owner picks one option per question (any format · email · verbal transcribed to `STATE/DECISIONS.md` · signed policy note). Operator authors the corresponding fire call with the chosen `Literal` value in place of `OWNER_POLICY_PENDING`; the service will write the record. Zero code changes required to accept the answers.

---

## 8 · Deferrals from W8 (explicit · not silent)

1. **CA1-005 whitepaper action re-evaluation** (Doc 14 §33) — W7 CP6 → W8 opener carry-over · **STILL DEFERRED**. Belongs alongside a whitepaper draft-and-freeze mechanism + licence-check shim; both are out of W8's Doc 15 scope. Named for W9 opener (or a subsequent polish wave).

2. **Doc 14 §§23–25 remaining 24 rows expansion** — W7 CP1 → W8 opener carry-over · **STILL DEFERRED**. Doc 14 mechanism-details continuation was not W8 anchor (Doc 15 was). Named for W9 opener.

3. **Governance frontends** (Rules Updates ceremony surface · Approvals group surface · Access-and-Erasure request UI · Breach Notification console · Trace surface UI) — v7 fabric exists for each; backend records are on record. Frontend surfaces are all subject to the same IP-allowlist screenshot gap (honest gap). Deferred to a subsequent polish wave; W8 delivered the mechanism half honestly.

4. **CA1-012 Watch staleness-flagging for rulebooks/baselines** — named in W8 nominal scope · **DEFERRED to W9**. Watch mechanism is W9's primary anchor; CA1-012 belongs with the Watch build, not with Doc 15 ceremony.

5. **Async event-loop pollution owner-visibility ruling** (from W7 CP8) — the per-test event loop fixture (`tests/invariants/conftest.py`) is on record as a claim-to-be-ratified. Owner has not ruled visibly; the fixture continues to hold the cohort together honestly. Named for owner-visibility.

6. **Data Suite surface (v7-exact)** — W6 → W7 → **still deferred at W8 close**. Not on W8's Doc 15 scope. Polish wave item.

7. **LLM chip UI polish** — W6 cosmetic deferral · **still deferred**. Polish wave item.

**Rationale**: Every deferral above is explicit, cited to its origin, and belongs to a named future wave. No W8 nominal scope item silently slipped.

---

## 9 · W9 opener carry-over (P0)

1. **FL-P4-W8-01 policy answers** (§7 above) — owner ruling on 7 questions unlocks N-series ceremony fire.
2. **CA1-005 whitepaper re-evaluation** (P0 · from W7 CP6 deferral).
3. **Doc 14 §§23–25 remaining 24 rows expansion** (P0 · from W7 CP1 deferral).
4. **CA1-012 Watch staleness-flagging** (P0 · alongside Watch primary build).
5. **CA1-011 enforcement half** at the named seam `services.watch.route_recheck_failure` (per Owner Ruling 2026-08-25T23:15Z SPLIT).
6. **Ledger continuity (CA1-N5)** (P0 · W9 nominal scope).
7. **Walk-this** per A8 ruling (Q1 · Q2 · Q3) (P0 · W9 nominal scope).
8. **Watch mechanism + Grey Mirror completion** (P0 · W9 primary anchor · ~6400 LOC re-baselined).

---

## 10 · Screenshots (honest gap · unchanged from W3..W7)

Owner's IP allowlist (stop-order 2026-08-14) refuses every non-allowlisted source with `403 · This surface answers allowlisted addresses only.` — including the sandbox screenshot tool. **This gap is intentional and expected behaviour.**

Curl-through-allowlist verification is on record where a surface is live behind pod-shell mount. W8 shipped mechanism-side records; frontend surfaces are deferred to a polish wave (§8.3). Owner-side rendering required when the polish wave lands.

---

## 11 · Dashboard

- **W1..W8 · CLOSED** (W7 closed 2026-08-26T01:10Z · W8 closed 2026-08-26T02:45Z).
- **Frozen contracts** · 47 (previously 39 at W7 close · +8 across W8: `handoff_contract_v0` · `approval_request_v0` · `approval_decision_v0` · `breach_notification_v0` · `erasure_request_v0` · `countdown_started_v0` · `rules_update_applied_v0` · `rules_update_rechecked_v0`).
- **Fidelity ledger rows total** · 14 opened across the programme (`FL-P4-W4-01` · `FL-P4-W6-01..09` · `FL-P4-W7-01..02` · `FL-P4-W8-01..02`). 13 CLOSED · 1 OPEN (`FL-P4-W8-01` · owner policy · non-blocking to wave close per owner directive).
- **Owner rulings on file** · 6 (unchanged since W7 close · owner auto-continue ruling covered W8 and W9).
- **Test count** · 366 wave-close cohort green (55 files) at `phase0/drill_receipts/20260826T024000Z_w8_wave_close_green.log`.
- **LOC delivered (W1..W8 cumulative)**:
  - W1..W5 · +11783 (per §7 status_and_wave_plan table).
  - W6 · +3319 (15% overrun · accepted at close).
  - W7 · +2779 (79% of 3520 budget · UNDER).
  - **W8 · +2964 spine + 4 pod-shell = +2968** · **53% of 5600 budget · UNDER by ~2632 LOC**.
  - W1..W8 total · **~20849 net**.
- **Mechanism corpus** approximate coverage post-W8: ~46% (+2 pts from Doc 15 §17 governance ceremony · CA1-009 · N-series scaffolding).
- **Composite headline** approximate: **~44%** (up from ~43% at W7 close).

---

## 12 · Straight into W9

Per Owner Ruling 2026-08-26T00:25Z (Auto-continue 2 waves), W9 opens on this report's landing.

**W9 opener CP1** starts with:
- N-series policy resolution (FL-P4-W8-01 §7 above): if owner has answered, wire the answers; else name the pending status and continue with the rest of W9 without firing.
- Watch mechanism primary build (Doc 3 · Doc 8) — includes CA1-011 enforcement half at `services.watch.route_recheck_failure` (W9 seam per Owner Ruling 2026-08-25T23:15Z SPLIT).

W9 nominal scope (per §7 status_and_wave_plan re-baselined table · confirmed by owner auto-continue):
- Watch mechanism + Grey Mirror four sub-surfaces (overview · monitor · response · people).
- Ledger continuity (CA1-N5).
- Walk-this affordance per A8 ruling.
- CA1-011 enforcement at named seam.
- Doc 14 §§23–25 remaining 24 rows expansion (carried from W7).
- CA1-005 whitepaper re-evaluation (carried from W7).
- CA1-012 Watch staleness-flagging (carried from W8).

Stop-and-report triggers unchanged: load-bearing artifact conflicts · scope drift past budget · mechanism-faking risk · owner-ruling-class questions.

**W9 stop-and-report line**: 6400 LOC per re-baselined table.

Flowing directly into W9 CP1.
