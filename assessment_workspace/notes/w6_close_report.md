# W6 Close Report

**Wave**: W6 · Cost Ledger + Retention + Grey Mirror groundwork + Lowered Standard
**Owner GO**: 2026-08-25 (opener #1 rebaseline ratified, opener #2 FL-P4-W4-01 reconciled)
**Wave close**: 2026-08-25T22:40Z
**Head at close**: `programme/track-a` @ `7db5a00` (W6 close reconciliation) atop `39a7034` (W6 CP5)
**Baseline at wave open**: `39386ac` (W5 close)

---

## 1 · Bottom line

- **250/250 W6 wave-close cohort green** (36 test files, `phase0/drill_receipts/20260825T224000Z_w6_wave_close_green.log`).
- **18/18 frozen+contract sub-cohort green** (`phase0/drill_receipts/20260825T223200Z_w6_close_frozen_cohort_green.log`) — assembled via the grep discipline ratified in FL-P4-W4-01.
- **9 fidelity ledger rows opened and reconciled** (FL-P4-W6-01 … FL-P4-W6-09) — under per-drift honest judgment (not blanket regeneration).
- **LOC actual: +3319 net vs 2880 budget → 15% over.** Data Suite surface and LLM chip UI polish deferred to W7 (see §5).

---

## 2 · Checkpoint outcomes

| CP | Scope | Committed | LOC (net) | Status |
|----|-------|-----------|-----------|--------|
| Openers | Rebaseline (1.60× median) + FL-P4-W4-01 reconciliation | `f647051` | +25 | DONE |
| CP2 | Cost Ledger backend (CA1-008 · rates + ledger + 5-lever attribution) | `d7ff88e` | +951 | DONE |
| CP2b | Cost Ledger frontend surface (CA1-008 lever sequence visible) | `717013f` | +430 | DONE |
| CP3 | Retention enforcement (CA1-N1 · shield extensions) | `770e013` | +798 | DONE |
| CP4 | Grey Mirror groundwork · Solva stages 4-6 mechanism-side | `d9ae4a5` | +504 | DONE (surface-side deferred to W9 per opener plan) |
| CP5 | Lowered Standard (CA1-010) · session-scoped + expiry + `in_process` residency region | `39a7034` | +582 | DONE (backend only) |
| CP6 | Wave close · 9 fidelity ledger drifts reconciled · 2 defect classes named | `7db5a00` | +29 | DONE |
| **Deferred to W7** | Data Suite surface v7-exact · LLM chip UI polish · Grey Mirror overview surface (naming) | — | — | DEFERRED (see §5) |

**Total W6 net LOC**: **+3319** (vs 2880 budget). Overrun 439 LOC (~15%).

---

## 3 · 9 fidelity ledger drifts — reconciled by per-drift judgment

Assembled via `grep test_*_frozen*.py + test_*_contract*.py` per the FL-P4-W4-01-ratified discipline. Right-reason failure banked at `phase0/drill_receipts/20260825T221600Z_w6_close_frozen_cohort_right_reason.log`.

**Not one recurring defect class — TWO distinct classes:**

### 3.1 · Environmental pydantic serialization drift class (6 of 9)

| Row | Contract | Delta |
|-----|----------|-------|
| FL-P4-W6-01 | `AdmissionRefusal_v0` | `.outcome` Literal — dropped redundant `enum` (kept `const`) |
| FL-P4-W6-03 | `NormalizedUnit` (five_rings) | `ProvenanceRing.locator`, `ReextractionHandleRing.extraction_params` Dict — added `additionalProperties: true` |
| FL-P4-W6-04 | `ObjectiveRequest` | `EstateRegionSelector.filters` Dict — same as -03 |
| FL-P4-W6-05 | `UseDataWizardSession` | `PlanPreviewCard.halt_note_verbatim` Literal + `SampleResultsCard.class_distribution` Dict — both patterns |
| FL-P4-W6-06 | `CommissionVerdict` | `.verbatim_carrier` Literal — same as -01 |
| FL-P4-W6-07 | `ObjectiveRequest_v2` | `Envelope.availability_snapshot`, `Envelope.floor_feasibility` Dict — same as -03 |

**Origin**: pydantic 2.13.4 emitter behavior change on `Literal[…]` and `Dict[str, Any]` fields. Contract file blame is 2026-07-02 to 2026-07-31 — **before any wave modified these models**. Not a wave-scope code change.

**Verdict**: `UNINTENDED_ENVIRONMENTAL`. Runtime behavior unchanged; only pydantic-emitter boilerplate drifted.

**Reconciliation**: re-bless snapshots pinned to pydantic 2.13.4 per this W6 close ratification. Alternative rejected because there is no code change to revert (the model files are untouched).

**Process finding (§6.1)**: frozen snapshots stored as raw pydantic-emitted JSON are **not stable across pydantic minor versions**. Named as a P1 W7-opener owner-ruling item — either pin pydantic in `requirements.txt` with justification, or project schemas onto a version-independent canonical form before byte-comparison.

### 3.2 · FL-P4-W4-01 map/count omission defect class recurring (3 of 9)

| Row | Meta-test | Cause |
|-----|-----------|-------|
| FL-P4-W6-02 | `test_composed_conclusion_snapshot_parity_at_18` | Count asserts `==36`; actual 37. `actor_declaration_v0` snapshot on disk since W1 (`2b08b39`); count never bumped |
| FL-P4-W6-08 | `test_every_frozen_contract_has_snapshot` | W1 added 3 modules (`actor_declaration.py`, `record_matrix.py`, `task_identity.py`); only 1 is a pydantic BaseModel; none were mapped |
| FL-P4-W6-09 | `test_every_snapshot_maps_to_a_contract` | `actor_declaration_v0.contract_snapshot.json` orphaned from map |

**Origin**: W1 thin-kernel commits `4855b35` + `2b08b39` (2026-08-14) added contracts + snapshot but did NOT update `CONTRACT_TO_SNAPSHOT` or the `parity_at_N` count. **Same shape as FL-P4-W4-01** (W4 LedgerRow extension without snapshot bump). **Recurrence count for this defect class: 2** (W1 origin, first discovered in W5; W4 origin, discovered in W5 → FL-P4-W4-01).

**Verdict**: `INTENDED_addition_UNINTENDED_map_omission` for `actor_declaration.py`. `TEST_SCOPE_FINDING` for `record_matrix.py` and `task_identity.py` — these are NamedTuple utility modules (actively imported by `services/compute_seam/seam.py` and thin-kernel tests) that never should have been enumerated by the parity test in the first place; the enumerator's docstring rule (`"frozen Pydantic model(s)"`) is narrower than its implementation.

**Reconciliation** (all in one commit, `7db5a00`):
- Added `"actor_declaration.py": "actor_declaration_v0.contract_snapshot.json"` to `CONTRACT_TO_SNAPSHOT`.
- Introduced `NON_CONTRACT_UTILITY_MODULES = {"record_matrix.py", "task_identity.py"}` and narrowed `_enumerate_contract_sources()` to exclude them — matches the docstring intent.
- Bumped `parity_at_18` count `36 → 37` and updated the docstring to name W6 close as the anchor.

---

## 4 · Process findings and definition-of-done additions

### 4.1 · Environmental pydantic drift finding (new)
Frozen snapshots stored as raw pydantic-emitted JSON are **not stable across pydantic minor versions**. Two remediations named:
- (a) Pin pydantic in `requirements.txt` with a justification comment.
- (b) Project schemas onto a version-independent canonical form (strip pydantic-idiomatic redundancy such as `enum` alongside `const`, and elide default-`additionalProperties` markers) before byte-comparison.

**Named as W7-opener owner-ruling item**. Not remediated in W6 — flagged for explicit owner steer.

### 4.2 · FL-P4-W4-01 defect class · definition-of-done ratification
**Ratified rule (effective W7 onward)**: any commit touching `contracts/*.py` that emits a pydantic BaseModel OR adding a `*.contract_snapshot.json` MUST touch:
1. The snapshot file, AND
2. `CONTRACT_TO_SNAPSHOT` in `test_frozen_contract_snapshot_parity.py`, AND
3. The `parity_at_N` count assertion in `test_composed_conclusion_v0_contract_frozen.py` (or its successor count-invariant).

All three in the SAME commit. Wave-close cohorts assemble by `grep test_*_frozen*.py + test_*_contract*.py` (this rule was already ratified at W5 close; reaffirmed here).

### 4.3 · Recurrence tracking
FL-P4-W4-01 defect class recurrence count = **2** (W1 origin discovered at W6, W4 origin discovered at W5). If it recurs again in W7+, the definition-of-done additions above are the immediate audit target.

---

## 5 · Deferrals to W7 (explicitly named)

W6 landed over budget (3319 vs 2880 = 15% over). Per owner's W6 close ruling, deferrals are named explicitly rather than holding W6 open:

| Item | Source | Rationale | Anchor |
|------|--------|-----------|--------|
| **Data Suite surface (v7-exact)** | CP5 as originally scoped | Backend Data Suite is not yet built; frontend surface without backend is fabrication. Full CP moves to W7. | v7 oracle `DATA_SUITE` fabric · notes/prototype_inventory_v7.md |
| **LLM chip UI polish** | CP5 as originally scoped | Cost Ledger chip (rates/ledger visible) is live; LLM chip refinement is cosmetic and belongs alongside the Cost Ledger polish loop. | notes/reuse_map_v7.md · ConnectDrawerChat surface |
| **Grey Mirror overview surface (naming)** | CP4 mechanism-side is done; surface-side deferred by opener plan | v7 oracle has no honest render for Grey Mirror without Watch; deferred to W9 per opener plan | notes/status_and_wave_plan.md §7 |
| **Pydantic-version-drift remediation** | §4.1 above | New P1 item from W6 close finding; needs owner ruling between (a) pin and (b) canonical-projection | This report §4.1 |

**None of these blocks W7 GO.** W7 nominal scope (Targeta · Model Ecosystem · Model Admission) is independent of the deferrals.

---

## 6 · Verification path for orchestrator (independent audit)

```bash
cd /app/assessment_workspace/repos/Extraction-Akki

git log --oneline programme/track-a | head -8
# 7db5a00 W6 close · 9 fidelity ledger drifts reconciled · 2 distinct defect classes named
# 39a7034 W6 CP5 · Lowered Standard (CA1-010) · session-scoped state + expiry + in_process residency
# d9ae4a5 W6 CP4 · Solva stages 4-6 · Grey Mirror groundwork · mechanism-side only
# 770e013 W6 CP3 · Retention enforcement · CA1-N1 · 218/218 green
# 717013f W6 CP2b · Cost Ledger frontend surface · CA1-008 lever sequence visible
# d7ff88e W6 CP2 · Cost Ledger backend · CA1-008 rates + ledger + 5-lever attribution
# f647051 W6 opener #2 · FL-P4-W4-01 reconciled · frozen contract parity restored
# 39386ac W5 CP4 frontend · Chat surface · ThinkLab reasoning wire · DataShield reasoning-receipts extension

# Frozen+contract cohort — 18 tests
cd backend
python3 -m pytest \
    tests/invariants/test_actor_declaration_v0_contract_frozen.py \
    tests/invariants/test_admission_refusal_v0_contract_frozen.py \
    tests/invariants/test_backfilled_contract_snapshots.py \
    tests/invariants/test_composed_conclusion_v0_contract_frozen.py \
    tests/invariants/test_feasibility_result_v0_contract_frozen.py \
    tests/invariants/test_frozen_contract_snapshot_parity.py \
    tests/invariants/test_invariant_contract_snapshots.py \
    tests/invariants/test_objective_request_v2_contract_frozen.py -v
# Expect: 18 passed

# Full W6 close cohort — 36 files · 250 tests
xargs -a /tmp/w6_close_cohort.txt python3 -m pytest --tb=short
# Expect: 250 passed

# Fidelity ledger rows on record (assessment repo)
ls /app/assessment_workspace/phase0/fidelity_ledger/FL-P4-W6-*.json
# Expect: 9 files (FL-P4-W6-01 through FL-P4-W6-09), plus FL-P4-W4-01
```

---

## 7 · No push, ever

Owner Clarification 1 (2026-08-14). All commits are local. Assessment repo `master` and Extraction-Akki `programme/track-a` both stay local.

---

## 8 · Owner steer requested before W7 GO

1. **Pydantic-version-drift remediation path** (§4.1): pin (a) vs canonical-projection (b) vs both?
2. **W6 LOC overrun** (15%): accept the recalibrated envelope for W6 as delivered, or narrow-scope W7 to absorb the overrun?
3. **W7 scope confirmation**: Targeta · Model Ecosystem · Model Admission per re-baselined estimate of 3520 LOC — proceed as planned, or steer?

Holding until owner replies.
