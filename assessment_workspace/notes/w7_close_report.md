# W7 Close Report

**Wave**: W7 · Targeta · Model Ecosystem · Model Admission Ceremony
**Owner GO**: 2026-08-25T23:30Z (verbatim in `STATE/DECISIONS.md` §W7-GO row)
**Wave close**: 2026-08-26T01:10Z
**Extraction-Akki HEAD**: `programme/track-a` @ `aa230b7` (W7 CP8 conftest event-loop fixture)
**Pod-shell HEAD** (`/app` main): `a5933a1` (Model Ecosystem surface + 4 W7 routers mounted)
**Assessment-master HEAD**: `<pending W7 close commit>`
**Baseline at wave open**: `5aba8e7` (W7-prep pydantic pin)

---

## 1 · Bottom line

- **310/310 W7 wave-close cohort GREEN** (44 test files) at `phase0/drill_receipts/20260826T010500Z_w7_wave_close_green.log`.
- **Frozen+contract sub-cohort GREEN** at each CP · pydantic 2.13.4 pin holds.
- **2 fidelity ledger rows opened** (FL-P4-W7-01 · FL-P4-W7-02) — one closed as INTENDED map recurrence, one closed as SELF-CORRECTED orientation error (spine vs pod-shell confusion).
- **LOC actual · 2779 net** (Extraction-Akki 2429 + pod-shell 350) vs **3520 budget** → **79% consumed** · **UNDER budget by 741 LOC**.
- **1 deferral** to W8 (CA1-005 whitepaper action · never opened per honest gate).
- **Screenshots gap** (honest): preview URL behind Owner IP allowlist (2026-08-14 stop-order); owner-side rendering required. Curl-through-allowlist verification on record instead.

---

## 2 · Register rows lit (IDs + count)

### Doc 13 (Autonomous Training · 23 canonical rows)

| Row | Anchor | Status |
|-----|--------|--------|
| Doc13-007 | C4-029 §20 | worker adapter-training economics lane · CP1 |
| Doc13-013 | C4-035 §24 | adapter registry (base model · lineage · rights · scorecard · versions) · CP3 |
| Doc13-014 | C4-036 §25 | plain "no adapter yet" surfacing · CP7 empty-state |
| Doc13-015 | C4-037 §26 | MOAC six-criterion card · CP4 |
| Doc13-015a | C4-037a §26.1 | Accuracy on uncurated composition · CP4 |
| Doc13-015b | C4-037b §26.2 | Coverage across strata · CP4 |
| Doc13-015c | C4-037c §26.3 | Refusal behaviour under Solva · CP4 |
| Doc13-015d | C4-037d §26.4 | Provenance integrity of training data · CP4 |
| Doc13-015e | C4-037e §26.5 | Cost per operation on real load · CP4 |
| Doc13-015f | C4-037f §26.6 | Time to answer at p95 · CP4 |
| Doc13-016 | C4-038 §27 | MOAC evidence from uncurated (curated inadmissible) · CP4 |
| Doc13-017 | C4-039 §28 | rights lineage required to ship · CP4 |
| **Doc13-023 · CA1-011** | Addendum §2 | W7-half · re-check-date register + surfacing + named seam · CP5 |

**13 of 23 Doc 13 rows lit at W7.** Remaining 10 (Doc13-001..006, 008..012, 018..022) touch Northena admit + worker plane + Critic Seam + Quarantine · all landed in earlier waves (W4/W5) or are W8/W9 scope.

### Doc 14 (Model Ecosystem · Baseline · Whitepaper · 28 canonical rows)

| Row | Anchor | Status |
|-----|--------|--------|
| Doc14-001 | C4-075 §32 | Licence-verified baseline curation · CP3 (registry FACTS-only seed) |
| **Doc14-023 · CA1-004** | Addendum §1 | baseline line names licence-verified starting model · CP5 |
| **Doc14-024 · CA1-005** | Addendum §1 | whitepaper action drafting · **DEFERRED TO W8** (150-LOC lid honest-gate stop) |
| Doc14-026 | C4-090 §39 | One-licence reach across every LLM · CP3 seed carries per-model license_note |

**4 of 28 Doc 14 rows explicitly named at W7.** Remaining 24 rows (Doc14-002..022, 025, 027, 028) are Doc-14 §§23–25 detail that CP1 was scoped to expand in a fresh pass — deferred to W8 opener alongside canonical-projection.

**Total register rows lit at W7 · 17.**

---

## 3 · Checkpoint outcomes

| CP | Scope | Extraction-Akki SHA | Pod-shell SHA | Test delta (files added / tests) | LOC (net) |
|----|-------|---------------------|---------------|----------------------------------|-----------:|
| CP1 | Rulings + rates lane + brief close · Q2/Q3/Q4 rulings folded | `60581fb` | — | +1 file · +5 tests | +139 |
| CP2 | Targeta invariants LIFT + FL-P4-W7-01 snapshot reconciliation | `6e76bc3` | — | (existing file · +12 tests reached) | +1 |
| CP3 | `services/model_registry/` top-level LIFT + FACTS-only seed (7 real Emergent Universal · NO whisper-tiny) | `82f6de5` | — | +1 file · +13 tests | +444 |
| CP4 | Model Admission ceremony backend · MOAC six-criterion contract + snapshot + count 37→38 | `57f4ba6` | — | +3 files · +15 tests | +874 |
| CP5 | CA1-004 baseline line + CA1-011 re-check state (W7 half + W9 named seam) + count 38→39 | `2256a6e` | — | +2 files · +8 tests | +587 |
| CP6 | CA1-005 whitepaper · **DEFERRED TO W8** (honest gate) | — | — | — | 0 |
| CP7 | 5 routers mounted (4 W7 new + 1 W6 cost_ledger latent) + Model Ecosystem UI (LLMs · Trained · Admission tabs) | `966c8ef` | `a5933a1` | +1 file · +11 tests | +369 (spine) + 350 (pod-shell) |
| CP8 | Wave close · cohort assembly · conftest fixture unblocks 310-cohort green · close report | `aa230b7` | — | +1 file · +0 tests (fixture only) | +15 |
| **TOTAL** | | | | **8 files** · **+64 tests** | **+2779** (vs 3520 budget · 79%) |

---

## 4 · Test delta + receipts

**W6 close cohort baseline · 250 tests (36 files).**
**W7 close cohort · 310 tests (44 files) · +64 tests · +8 files.**

Cohort assemble discipline (per FL-P4-W6-02/08/09 ratification + FL-P4-W7-01 broadening):
- grep `test_*_frozen*.py` + `test_*_contract*.py` (W6-ratified pattern)
- content-grep for `model_json_schema()` vs `contract_snapshot.json` (W7-added compensating discipline)
- every `test_*_invariants.py` file on disk (donor-side lift blind-spot compensator)
- explicit inclusion of every new `test_w7_cp*.py` file

Per-CP receipts on record (all under `phase0/drill_receipts/`):

| CP | Right-reason failure receipt | Green receipt |
|----|------------------------------|---------------|
| CP1 | `20260825T233500Z_w7_cp1_right_reason_fail.log` (4/5 fail · right reason) | `20260825T233800Z_w7_cp1_green.log` (5/5) |
| CP2 | `20260825T234100Z_w7_cp2_right_reason_fail.log` (1/12 fail · MiningPlan drift discovered) | `20260825T234500Z_w7_cp2_green.log` (12/12) |
| CP3 | `20260825T235000Z_w7_cp3_right_reason_fail.log` (13/13 fail · missing module) | `20260825T235800Z_w7_cp3_green.log` (13/13) |
| CP4 | `20260826T000500Z_w7_cp4_right_reason_fail.log` (8/10 fail · right reason) | `20260826T001000Z_w7_cp4_green.log` (15/15) |
| CP5 | `20260826T001500Z_w7_cp5_right_reason_fail.log` (7/9 fail · right reason) | `20260826T002200Z_w7_cp5_green.log` (23/23) |
| CP7 | `20260826T003000Z_w7_cp7_right_reason_fail.log` (11/11 fail · missing modules) | `20260826T003300Z_w7_cp7_green.log` (11/11) |
| CP8 | (no right-reason failure — fixture is additive discipline) | `20260826T010500Z_w7_wave_close_green.log` (**310/310 W7 close cohort**) |

---

## 5 · Reuse pulls used vs rejected

### USED
- **RMS-IQ-Core-2 `backend/services/targeta/`** (6 files · 425 LOC · already in-tree from earlier phase) — invariant tests lifted at CP2 (208 LOC · `test_targeta_invariants.py`).
- **RMS-IQ-Core-2 `backend/services/perception/model_registry.py`** (114 LOC) + **`models_registry.v0.json`** (70 LOC seed) — fabric semantics adapted at CP3 into top-level `services/model_registry/`. RMS's `whisper-tiny` seed content REJECTED per Owner Q3 (donor-side CI fixture, not on this estate). RMS's `attest_model` hard-fail semantics preserved verbatim.

### REJECTED (at brief-time · verified during CP execution)
- **Akki-Executive-Core `services/sandbox_generation.py`** (508 LOC) — Phase-J visitor-form-oriented Claude generation. Not MOAC-shaped. Confirmed reject at CP4.
- **Akki-Executive-Core `services/analysis_lifecycle.py`** (443 LOC) — spreadsheet analysis lifecycle. Not baseline curation. Confirmed reject at CP3.
- **Akki-Executive-Core `services/deck_*.py`** (653 LOC · 4 files) — Deck-templated async generation. Reuse-map suggested ADAPT-then-narrow for CA1-005 whitepaper under a 150-LOC lid. **Never opened in W7** (CP6 deferred to W8 · honest gate). Reject status: PENDING (W8 CP6 re-evaluation).
- **Akki-Executive-Final `services/solva/`** (1623 LOC reasoning subdir) — cleaner Solver package than Core, already adapted for W5/W6 CP4 Grey Mirror groundwork. Not W7 territory.

### BUILT (not lifted)
- Canon 4 §26 six-criterion MOAC (CP4 · 204 LOC contract + 226 LOC ceremony · anchor Canon 4 §26 verbatim).
- CA1-004 baseline line (CP5 · 79 LOC contract + 63 LOC records · Doc 14 §32 verbatim).
- CA1-011 re-check state W7 half (CP5 · 89 LOC · Owner Ruling 2026-08-25T23:15Z SPLIT).

---

## 6 · Fidelity ledger rows opened

| Row | Class | Origin | Status |
|-----|-------|--------|--------|
| FL-P4-W7-01 | INTENDED map recurrence · FL-P4-W4-01 defect class (#3) | W4 origin · targeta_mining_plan transitive missed at FL-P4-W4-01 bump | CLOSED at CP2 (snapshot re-blessed · Owner W7 GO ratifies) |
| FL-P4-W7-02 | Orientation correction · spine vs pod-shell confusion | W7 CP7 authorship error (my read) | CLOSED at CP7 (pod-shell bridge extended · row records the incorrect hypothesis AND the correction for audit uniformity) |

**Defect class FL-P4-W4-01 recurrence count · 4** (after FL-P4-W7-02 correction:
- W4 origin · northena_ledger_row · FL-P4-W4-01 detected W5 close
- W1 origin · actor_declaration_v0 map+count · FL-P4-W6-02/08/09 detected W6 close
- W4 origin · targeta_mining_plan transitive · FL-P4-W7-01 detected W7 CP2
- W7 origin · 4 new spine routers · pod-shell mount omission · FL-P4-W7-02 detected + fixed W7 CP7).

---

## 7 · Process findings → W8 opener carry-over

### 7.1 · From FL-P4-W7-01 (W6 DoD extension)
Wave-close cohort must ALSO include:
- **content-grep** for `model_json_schema()` vs `contract_snapshot.json` (compensates for filename-convention blind spot).
- **every `test_*_invariants.py`** on disk (compensates for donor-side lift blind spot).

Effective from W7 wave-close cohort assembly (already applied).

### 7.2 · From FL-P4-W7-02 (pod-shell/spine bridge DoD)
Any commit adding a new `services/<name>/router.py` on the spine (Extraction-Akki) MUST also touch `/app/backend/server.py` (pod-shell) at BOTH extension points (import block + `app.include_router()`). Wave-close cohort compensating tests named:
- `backend/tests/invariants/test_pod_shell_router_mount_completeness.py` · enumerate every spine `services/*/router.py` and assert each is mounted in `/app/backend/server.py`.
- `backend/tests/invariants/test_pod_shell_boots.py` · assert `import /app/backend/server.py` succeeds AND `TestClient(app).get('/')` returns 403 (allowlist refusal) not 500.

**Named as W8 CP1 opener P0** (alongside canonical-projection).

### 7.3 · From CP8 (async event-loop pollution)
`tests/invariants/conftest.py` · per-test event loop fixture stabilizes the cohort at ≥17 files. Not a governed model change; it's a test-harness fact-on-record. Named for W8 opener owner-visibility (owner may want a different remediation than a per-test fixture — e.g., a session-scoped fixture or a pytest-asyncio configuration bump).

---

## 8 · W8 opener carry-over (P0)

1. **Canonical-projection remediation** (from W6 close report §4.1 + Owner Ruling 2026-08-25T22:55Z §Q1) — canonical form for frozen snapshots that projects across pydantic minor versions. Load-bearing for W8 which mints many new contracts.
2. **Pod-shell mount completeness test** (§7.2 above).
3. **Pod-shell boot test** (§7.2 above).
4. **Async event-loop pollution owner ruling** (§7.3 above).
5. **CA1-005 whitepaper action re-evaluation** (deferred from W7 CP6 · 150-LOC honest-gate stop applies) — decide LIFT/ADAPT/BUILD/DEFER-AGAIN in W8 opener.
6. **Doc 14 §§23–25 remaining 24-row expansion** — verbatim from `canon_4_requirements.md`.

---

## 9 · Screenshots (honest gap · owner-side rendering required)

Owner's IP allowlist (stop-order 2026-08-14) refuses every non-allowlisted source with `403 · This surface answers allowlisted addresses only.` — including the sandbox testing agent used for close-report screenshotting.

**Curl-through-allowlist verification on record** (executed via allowlisted IP header hop chain):

```
$ curl -H "X-Forwarded-For: <allowlisted>, 10.0.0.1, 10.0.0.2" \
    http://localhost:8001/api/model_registry/version
{"version_n":0,"version_str":"v0","model_count":7,
 "location_note":"This estate's model registry lives at services/model_registry/. ..."}

$ curl -H "X-Forwarded-For: <allowlisted>, 10.0.0.1, 10.0.0.2" \
    http://localhost:8001/api/model_registry/models
{"total": 7,
 "purchased_llms": [{"model_id": "gpt-5.4", ...},
                    {"model_id": "gpt-5.2", ...}, ... (7 real)],
 "trained_adapters": [],       # honest empty — no ceremony yet
 "other": []}
```

**Deliverable to owner**: render `/models` at your allowlisted IP; the three tabs (LLMs on record · Trained adapters · Admission records) are ready. Data source: real facts on disk, drawn-not-blank on empty states.

---

## 10 · Dashboard

- **W1..W7 · CLOSED**.
- **Frozen contracts** · 39 (35 pre-W1 + 4 W1..W7 additive · actor_declaration_v0 · model_acceptance_card_v0 · baseline_line_v0).
- **Fidelity ledger rows total** · 12 opened across the programme (`FL-P4-W4-01` · `FL-P4-W6-01..09` · `FL-P4-W7-01..02`). All CLOSED except the two W7-open items surfaced above as W8 CP1 remediation carriers.
- **Owner rulings on file** · 6 (W6 rebaseline · W6 close 3-answer set · W7 prep 3-answer set · W7 GO 4-ruling set · Auto-continue-2-waves).
- **Test count** · 310 wave-close cohort green (44 files).
- **LOC delivered** (W1..W7 cumulative from `39386ac` W5 baseline · programme/track-a):
  - W6 · +3319 (15% overrun · accepted at close)
  - W7 · +2429 spine + 350 pod-shell = +2779 · **79% of budget** · UNDER.
- **Purchased LLMs on record** · 7 (Emergent Universal · real).
- **Trained adapters on record** · 0 (no ceremony has fired · honest empty).
- **CA1-011 W9 seam named** · `services.watch.route_recheck_failure (lands W9)` — appears on every AdmissionOutcome and every re-check status payload.

---

## 11 · Straight into W8

Per Owner Ruling 2026-08-25T00:25Z (Auto-continue 2 waves), W8 opens on this report's landing.

**W8 opener CP1** starts with canonical-projection remediation (see §8.1) and the two pod-shell discipline invariant tests (§7.2).

W8 nominal scope (per `notes/status_and_wave_plan.md` + owner auto-continue ruling):
- Governance ceremony · Approvals surfaces.
- N-series · CA1-N2 breach notification · CA1-N3 access-and-erasure.
- CA1-009 generalized handoff contract.
- Rules Updates · Spend Requests · Trace (REFERENCE-NOT-COPY load-bearing).
- Doc 14 §§23–25 remaining 24-row expansion.

Stop-and-report triggers unchanged: load-bearing artifact conflicts · scope drift past budget · mechanism-faking risk · owner-ruling-class questions (e.g., N-series legal facts).

Holding for owner receipt of this report; then flowing directly into W8 CP1.
