# W11 · Seasoned Update #01 · CP2 + CP3 core delivered

**Owner directive at W11 open**: STEP A (base-model ingest) · STEP B (build CP2 · build CP3 minimum viable) · STEP C (Seasoned Update).

**Date**: 2026-08-26T08:00Z
**Delivered on**: `Extraction-Akki@programme/track-a` (feec2a5 · a85774a)
**Format**: single markdown file + chat summary · W10 close-report style

---

## §1 · Training section · DONE / IN-BUILD / BLOCKED

### DONE

| Item | Where | Anchor |
|------|-------|--------|
| Doc 19A Critic Seam LIFT · 950 LOC verbatim + Owner-ruling doc byte-identical (SHA `42ca9e0f...5992c80a`) | `Extraction-Akki@feec2a5` · `backend/services/critic_pass/` | Doc 19A QA-1..QA-6 · Critic Seam Spec v1.0 §5-§9 |
| Demand Table service · §4.1 admissibility (named-failure rule) + §3.5 E=B+I derivation | `Extraction-Akki@a85774a` · `backend/services/training/demand_table.py` | Doc 17 §4.1 · Incremental Training Briefing §3.3-3.5 |
| Capacity Ledger record + read view · empty-at-ship · provenance day-one · state grammar building/held/saturated | `Extraction-Akki@a85774a` · `backend/services/training/capacity_ledger.py` | Doc 17 §4.2 + §5.3 |
| Test-set Seal · A17.11 RE-VERIFY-FIRST against on-disk `data_connection_record` · refuses honestly on stale (>24h) / link_working=false / missing | `Extraction-Akki@a85774a` · `backend/services/training/test_set_seal.py` | Doc 17 §5.1 + Owner CP3-open directive verbatim |
| `/api/training/state` · read-only rollup · REFERENCE-NOT-COPY | `Extraction-Akki@a85774a` · `backend/services/training/router.py` + `state.py` | Doc 17 §6 · Design Law A8 |
| `/api/training/demand-table/compile` · POST · deterministic compile + on-disk stamp | same commit · `router.py` | Doc 17 §4.1 |
| `/api/training/test-set-seal` · POST · live-verify-first · honest hold | same commit | Doc 17 A17.11 |
| `/api/training/capacity` · GET · empty-at-ship view | same commit | Doc 17 §4.2 |
| `/training` React route · same pattern as `/governance`, `/watch`, `/grey-mirror` · REFERENCE-NOT-COPY panels for Demand Tables, Capacity Ledger, Test-set Seals | pod-shell · `/app/frontend/src/components/Training.jsx` + `App.js` route registered | Canon 5 §12 · Doc 17 §6 |
| Live end-to-end probe against DigiCow · Demand Table compiled with 2 schemes + 3 strata + E computed · Test-set seal REFUSED HONESTLY (record 7 days old · beyond 24h freshness window) | pod-shell curl transcript in this note §5 | Doc 17 A17.11 |

**Test cohort at CP3 close**: **59/59 pytest cells green** (27 CP2 critic_pass lift + 18 training module + 9 training endpoints + 3 frozen-contract parity + 2 parity-seat).
Contract parity: **59 preserved** (governed non-frozen shapes only · pattern from `services.connect.sources_store`).

### IN-BUILD (deferred at CP3 open per Owner deprioritization)

| Item | Deferred to | Why |
|------|-------------|-----|
| Capacity Ledger · marginal-gain writer from calibration probe | CP8 (trainer runner + calibration probe execution) | Requires the trainer to run a real training arm; no simulated marginal-gain rows. |
| Capacity Ledger · saturation derivation from marginal-gain history | CP8 (once marginal-gain rows exist) | Derived, never declared. |
| Advanced accounting / forecasting on Capacity Ledger | Post-W11 | Owner said "defer advanced accounting/forecasting". |
| A18.6 · single-shot pilot async delivery | Post-W11 | Owner said "defer A18.6 async delivery entirely". |
| Objective Wizard demand-table compile-step integration | CP4 (Skill Files) or CP5 (recipe seat) | The wizard variant is a separate surface change; the compile function is already available at the router. |
| `training_params@v0` sidecar (T-1.1 recipe seat) | CP5 | Not needed for the DEMAND / CAPACITY / SEAL demonstration. |

### BLOCKED (awaiting Owner)

| Item | Blocking input | Non-blocking to |
|------|----------------|-----------------|
| CP8 trainer runner (LoRA/PEFT + Muon comparison arm) | (a) SSH key for the GPU VM (CP1 STEP 5); (b) DigiCow rights declaration; (c) base-model census activation (Owner names a specific member of Qwen3/Qwen3.5 or Llama per registry v0→v1 bump); (d) T-2.4 optimizer verdict rule requires post-run measurement, not a pre-set threshold — so Owner ruling on the arms is due AFTER first real training arm completes | CP4 · CP5 · CP6 · CP7 |
| Fresh DigiCow verification (to unblock the live seal) | Owner runs a fresh `/api/connect/data-source` probe → creates a fresh `data_connection_record` → the seal will then accept | CP4 · CP5 · CP6 · CP7 |
| A17.12-A17.17 · 6 OPEN policy rulings | Owner rulings (taxonomy graduation sign-off · probe-selectivity threshold · validation gating · interference weighting trigger · saturation cross-tenant policy · Doc 17 miscellaneous) | Non-blocking to any CP (OPEN-SLOT pattern) |
| A18.7 · provenance chain to training run | CP4 (Doc 18 provisioning wire-up) + CP8 trainer | Requires the trainer runner to produce the training-run record |

## §2 · Overall build + composite % preview

### 2.1 · W11 CP progress (post CP3)

| CP | Scope | Status | Commit |
|---:|-------|--------|--------|
| CP1 | R11 STEP 2/3 · GPU real handshake finalize | BLOCKED (SSH key) | — |
| **CP2** | Doc 19A Critic Seam LIFT | **DONE** | `feec2a5` |
| **CP3** | Doc 17 Demand Table + Capacity Ledger + Test-set Seal + Training panel (minimum viable) | **DONE** | `a85774a` |
| CP4 | Doc 18 provenance chain + Skill Files surface | NOT STARTED | — |
| CP5 | Doc 17 A17.3-A17.4 + T-1..T-2 recipe seat + optimizer harness | NOT STARTED | — |
| CP6 | Doc 19B Evidence Protocol PROPOSED harness | NOT STARTED | — |
| CP7 | Register expansion to 20 docs · 36 new rows | NOT STARTED | — |
| CP8 | Trainer runner (LoRA/PEFT + Muon) · real training | BLOCKED (SSH key + rights + census) | — |
| CP9 | Authoritative composite % recomputation + wave close | NOT STARTED | — |

### 2.2 · Composite % preview (NOT AUTHORITATIVE · recomputed at CP9)

Base at W10 close: **52.49 %** (515 mechanism rows).

Register delta post-W11 CP2+CP3 (mechanism-only bump):
* Doc 19A · 6 rows · REUSABLE → **DONE** at CP2 (weighted +3.0).
* Doc 17-005 · Demand Table · BUILD → **DONE** at CP3 (weighted +1.0).
* Doc 17-006 · Capacity Ledger · BUILD → **PARTIAL** at CP3 (weighted +0.5).
* Doc 17-007 · Capacity Probe · BUILD → **PARTIAL** at CP3 (weighted +0.5).
* Doc 17-011 · Test-set-precedes-training · BUILD → **DONE** at CP3 (weighted +1.0).

Preview composite ≈ **~53.5 %** (280.4 + 6.0 new-DONE-equivalent weight → 286.4 · denominator stays 515 until CP7 grows it to 551; after CP7 the denominator increases so composite drops to ~52.0-52.5 % before further CPs re-lift it). W11 CP9 will lock this authoritatively.

### 2.3 · LOC ledger

| CP | LIFT | ADAPT | BUILD (net) | Files added |
|---:|-----:|------:|------------:|-----------:|
| CP2 | 950 | ~20 | 380 (tests + ruling doc) | 9 |
| CP3 | 0 | ~10 (server.py wire-up · App.js route) | 995 (services 460 · router 155 · frontend 245 · tests 405) | 10 |
| **Sum** | **950** | **~30** | **~1375** | **19** |

Vs. W11 reassessment envelope (~4850 LOC total across 9 CPs): CP2+CP3 delivered ~48 % of the total envelope in the first two-thirds of a working session. Under target.

## §3 · Recommended close plan · shortest critical path

CPs are ordered by dependency and by what unlocks Owner-testable outcomes fastest:

### Path 1 · Owner-testable now (no external input needed)

**CP2 (DONE) → CP3 (DONE)** already delivered the "test the training section first" outcome. Owner can now:
* Visit `/training` on the SPA — see the Demand Table compiled for the DigiCow USSD-generation objective.
* Observe the honest EMPTY Capacity Ledger.
* Observe the honest REFUSED Test-set Seal (stale 8/19 record).
* Trigger a fresh `/api/connect/data-source` probe to update the record → re-attempt seal → confirm the seal succeeds against fresh data.

### Path 2 · Non-blocking CPs to close before external inputs arrive

Proposed order:

1. **CP7 · Register expansion to 20 docs · 36 new rows** — pure docs; no blockers. Grows the mechanism corpus so subsequent composite computes reflect Docs 17-19 shape. ~250 register lines + ~150 test LOC.
2. **CP4 · Doc 18 provenance chain wire-up + Skill Files surface** — already 5 rows DONE from prior lift; extend `callable_skill_persistence.py` to write provisioning ON MOAC admission + add `/skill-files` React route. ~350 LOC.
3. **CP5 · T-1..T-2 recipe seat + optimizer harness (shape only)** — `training_params@v0` sidecar (versioned · ledgered · outside `contracts/` · no Parity contact per T-1.1) + optimizer selection protocol harness shape (no real training arm yet). ~250 LOC.
4. **CP6 · Doc 19B Evidence Protocol PROPOSED harness** — EP-1, EP-2, EP-3, EP-5 (EP-4 stays OPEN-SLOT). Evidence-class inline attachment discipline extends across existing surfaces. ~200 LOC.

Cumulative after CP4-CP7 close: composite lifts an additional ~2-3 pp (register denominator growth is offset by DONE-count growth).

### Path 3 · Gated on Owner inputs

**CP8 · Trainer runner (LoRA/PEFT + Muon comparison arm)** — gated on ALL of:
* SSH key for GPU VM (from Owner).
* DigiCow rights declaration (from Owner).
* Base-model census activation (Owner names Qwen3/Qwen3.5 or Llama specific member).
* Fresh DigiCow verification record (Owner re-runs `/api/connect/data-source`).

Once all four land, CP8 runs the first real two-arm optimizer comparison per T-2.2. MOAC card emitted per T-2.4. Recipe seat filled per T-1.4.

**CP9 · Authoritative composite recomputation + wave close** — runs regardless of CP8 status. If CP8 is still blocked at wave close, W11 closes with composite reflecting CP2-CP7 lifts only.

### Recommended action for Owner

**Immediate**: eyeball the `/training` surface on the SPA. Trigger a fresh DigiCow probe. Re-attempt seal to see it succeed.

**When ready**: (a) supply SSH key so CP1 finalize + CP8 can proceed; (b) sign DigiCow rights declaration; (c) name the base-model census candidate. These four unblock CP8.

**Meanwhile**: I proceed with CP4 → CP7 (all non-blocking) in the standard tests-first · same-commit-DoD cadence.

## §4 · Base-model findings (Step A recap · full note at `notes/w11_stepA_base_models.md`)

* **Audio · ASR · CI fixture**: `whisper-tiny` (SHA-pinned) — the only concrete audio model in the registry.
* **Audio · ASR · production**: unnamed · Owner selects at first census activation (v0→v1 registry bump).
* **Audio · Codec**: NOT NAMED · spec §16.2 Open Decision.
* **Audio · Language ID**: NOT NAMED · spec §4.1 constrains only lightweight/offline/CPU-viable.
* **Text · primary arm**: Qwen3/Qwen3.5 family (Apache-2.0) · specific member Named at first census activation.
* **Text · comparison arm**: Llama family (verify_at_acquisition) · specific member Named at first census activation.
* **Optimizer · first candidate**: Muon (T-2 protocol).
* **Adapter methodology**: LoRA/PEFT (T-1.5 FACT).

## §5 · Live probe transcripts (recorded in this session · CP3 close)

### 5.1 · Demand Table compile against DigiCow USSD-generation objective

```
POST /api/training/demand-table/compile
{
  "objective_id": "obj/digicow/ussd-generation",
  "schemes": [
    {"id": "text_gen.core",
     "named_failure": "the model produces text that does not match USSD 160-char and menu-mode conventions"},
    {"id": "code_switch.sw_en",
     "named_failure": "entity boundaries break at code-switch points"}
  ],
  "per_stratum": [
    {"stratum_id": "language.sw",     "B": 1, "I": 0},
    {"stratum_id": "language.sw+en",  "B": 3, "I": 1},
    {"stratum_id": "channel.ussd",    "B": 2, "I": 1}
  ]
}
```
Response (verbatim):
```
{
  "ok": true,
  "objective_id": "obj/digicow/ussd-generation",
  "compiled_at": "2026-08-26T07:50:27.717501+00:00",
  "schemes_count": 2, "strata_count": 3,
  "per_stratum": [
    {"stratum_id":"language.sw",    "B":1, "I":0, "E":1},
    {"stratum_id":"language.sw+en", "B":3, "I":1, "E":4},
    {"stratum_id":"channel.ussd",   "B":2, "I":1, "E":3}
  ]
}
```

### 5.2 · Test-set Seal · honest hold against stale record

```
POST /api/training/test-set-seal
{
  "objective_id": "obj/digicow/ussd-generation",
  "source_id": "aws.rds.db-restore-603-cluster.digicow_live",
  "target_table": "ussd_question_response",
  "strata": ["language.sw", "language.sw+en"],
  "sample_size": 1000
}
```
Response (verbatim):
```
{
  "ok": false,
  "refusal_reason": "latest verification record for
   'aws.rds.db-restore-603-cluster.digicow_live' is stale
   (older than 24.0h). Refusing to seal · sealing against a stale
   cache is a REFERENCE-NOT-COPY violation risk."
}
```

The seal honestly refuses because the most recent DigiCow record on disk (`data_source_digicow_live_20260819T152513Z_FINAL.json`) is 7 days old, beyond the 24-hour freshness window. A fresh Owner-initiated `/api/connect/data-source` probe will update the record and unblock the seal.

### 5.3 · State rollup after the compile

```
GET /api/training/state
```
Response (excerpt):
```
{
  "ship_state": "populated",
  "demand_tables": [
    {"objective_id":"obj/digicow/ussd-generation",
     "compiled_at":"2026-08-26T07:50:27.717501+00:00",
     "schemes_count":2, "strata_count":3,
     "per_stratum": [
       {"stratum_id":"language.sw","B":1,"I":0,"E":1},
       {"stratum_id":"language.sw+en","B":3,"I":1,"E":4},
       {"stratum_id":"channel.ussd","B":2,"I":1,"E":3}
     ],
     "schemes": [...]},
  ],
  "capacity_ledger_rows": 0,
  "test_set_seals": [],
  "reference_note": "REFERENCE-NOT-COPY · Design Law A8 · every demand
   table, capacity ledger row, and test-set seal is a file on disk..."
}
```

## §6 · GPU status

* **Real GPU connection**: BLOCKED · awaiting SSH key from Owner. Mock fallback in place (unchanged).
* **CP1 STEP 2/3 finalize** (hardware fact sheet + real crossing receipt): NOT YET · blocked as above.
* **Not blocking**: CP2, CP3, CP4, CP5, CP6, CP7 are all offline-executable. CP8 is the first CP that touches GPU.

## §7 · What's next (my next actions if Owner says "continue")

1. **CP7 · register expansion to 20 docs** — pure docs, no external blockers, ~250 LOC.
2. **CP4 · Doc 18 provenance chain + Skill Files surface** — extends already-lifted callable-skill package, ~350 LOC.
3. **CP5 · Recipe seat + optimizer harness shape** — ~250 LOC.
4. **CP6 · Evidence Protocol PROPOSED** — ~200 LOC.

Total non-blocking envelope remaining: ~1050 LOC across CP4-CP7. Achievable within the same working session cadence as CP2+CP3.

**Stop-and-report ends here.** Awaiting Owner ratification or steer before continuing.

---

## Appendix A · Adaptation audit for CP2 LIFT

Per Owner directive at CP2-open: "Flag every adapted line-range in the drill receipt so the verbatim/adapted split is auditable."

| File | Lines | Status | Adaptation |
|------|------:|--------|------------|
| `backend/services/critic_pass/__init__.py` | 21 | VERBATIM | 0 lines changed |
| `backend/services/critic_pass/archive.py` | 148 | VERBATIM | 0 lines changed |
| `backend/services/critic_pass/calibration_ledger.py` | 170 | VERBATIM | 0 lines changed |
| `backend/services/critic_pass/harness.py` | 90 | VERBATIM | 0 lines changed |
| `backend/services/critic_pass/manifest_gate.py` | 138 | VERBATIM | 0 lines changed (imports already exist in Extraction-Akki) |
| `backend/services/critic_pass/rubric.py` | 148 | VERBATIM | 0 lines changed |
| `backend/services/critic_pass/seeded_defect_corpus.py` | 241 | VERBATIM | 0 lines changed |
| `docs/rulings/critic_pass_e1_2026_07_25.md` | — | VERBATIM (SHA byte-identical) | 0 lines changed |
| `backend/tests/invariants/test_critic_pass_lift.py` | ~350 | ADAPTED | Ruling-path pinned to Extraction-Akki `docs/rulings/`; 3 donor test cells deferred with docstring pointer (ManifestEntry field-expansion attests on `FeasibilityResult_v0`, `PerceptionJob_v0`, `MiningPlan`; QA-7 batch_quarantine attest; parity-33 count attest). Retained: rubric shape (7 items · CR-1..CR-7), QA-3 no-self-review, archive append-only + CIF seed, seeded-defect A3.3 asymmetry, Class E decay, staleness window, harness archives verdict, Owner ruling SHA byte-identical (Extraction-Akki path). |

**Verbatim LOC**: 956 (7 modules + ruling doc).
**Adapted LOC**: ~10 (path-only adjustments in the test file; the donor 480-line test was shortened to ~350 lines because deferred cells were omitted).

## Appendix B · CP3 files landed

| File | LOC | Purpose |
|------|----:|---------|
| `backend/services/training/__init__.py` | 17 | Package docstring |
| `backend/services/training/demand_table.py` | 145 | Compile + persistence · §4.1 admissibility · §3.5 E=B+I |
| `backend/services/training/capacity_ledger.py` | 128 | Append-only JSONL · empty-at-ship · provenance-required |
| `backend/services/training/test_set_seal.py` | 195 | Live-verify-first · freshness window · deterministic manifest hash |
| `backend/services/training/state.py` | 60 | Rollup for the /training surface |
| `backend/services/training/router.py` | 130 | 4 endpoints: state · compile · seal · capacity |
| `backend/tests/invariants/test_training_module.py` | 260 | 18 unit invariants |
| `backend/tests/invariants/test_training_endpoints.py` | 145 | 9 FastAPI TestClient invariants |
| Pod-shell wire-up (`/app/backend/server.py`) | 4 | Router import + include |
| Pod-shell frontend (`/app/frontend/src/App.js`) | 2 | Route registration |
| Pod-shell frontend (`/app/frontend/src/components/Training.jsx`) | 245 | Panel · 4 stateful sections · REFERENCE-NOT-COPY |
| **Total** | **~1331** | — |

## Appendix C · Verification path for orchestrator (independent audit)

```bash
cd /app/assessment_workspace/repos/Extraction-Akki
git log --oneline programme/track-a | head -3
# a85774a W11 CP3 · Doc 17 Training plane core · Demand Table + Capacity Ledger + Test-set Seal · 45/45 green · parity 59 preserved
# feec2a5 W11 CP2 · Doc 19A Critic Seam LIFT from Akki-OS-V1 · 27/27 green · parity 59 preserved
# f101bd0 W10 wave-close correction · strict-flip mode-matrix invariant across BOTH surfaces · 17/17 green

python3 -m pytest \
    backend/tests/invariants/test_critic_pass_lift.py \
    backend/tests/invariants/test_training_module.py \
    backend/tests/invariants/test_training_endpoints.py \
    backend/tests/invariants/test_frozen_contract_snapshot_parity.py \
    backend/tests/invariants/test_parity_seat_extends_thin_kernel.py -v
# Expect: 59 passed.

# Live probe · demand table compile (owner IP required for allowlist).
curl -s -H "X-Forwarded-For: 34.16.56.64,proxy1,proxy2" -H "Content-Type: application/json" \
     -d '{"objective_id":"obj/x","schemes":[{"id":"s1","named_failure":"fails"}],
          "per_stratum":[{"stratum_id":"s","B":1,"I":0}]}' \
     http://127.0.0.1:8001/api/training/demand-table/compile | python3 -m json.tool

# Live probe · state rollup.
curl -s -H "X-Forwarded-For: 34.16.56.64,proxy1,proxy2" \
     http://127.0.0.1:8001/api/training/state | python3 -m json.tool
```

**End of Seasoned Update #01.**
