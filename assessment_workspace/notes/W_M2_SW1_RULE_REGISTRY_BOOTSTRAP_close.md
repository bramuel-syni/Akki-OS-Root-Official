READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M2-SW1 · W-RULE-REGISTRY-BOOTSTRAP — close

**Sub-wave slot:** 1 of the M2 block · Rules-Service stack #1 (of 4).
**UTC close:** 2026-09-13T18:43Z (EAT window IN).
**Canon anchors:** Doc-0 Attribute 4 (Controls) · Canon-3 §22 (registered controls additive) · Canon-3 §9.3 (single-writer) · `BUILD_STATUS_PERCENT_20260909 §2 row 4d`.

## Scope

The 286-rule register scaffold.  SW1 lands the **framework + seed**;
SW4 (W-286-RULE-ENUMERATION-CLASSIFY) lifts the remaining 272 rules
into it.

## Files landed

- `backend/services/rules_service/__init__.py` (package)
- `backend/services/rules_service/rule_registry.py` (mechanism)
- `backend/tests/invariants/test_wm2_sw1_rule_registry_bootstrap.py` (7 invariants)

## Invariants landed

1. Module fabric present (`RuleRecord`, `RuleRegistry`, `ENFORCEMENT_CLASSES`, `RegistryAppendOnly`, `RuleIdCollision`, `get_rule_registry`).
2. Finite enforcement-class taxonomy: `{blocking, declaratory, reporting, pending_override}`.
3. Three canonical seed rules present: `RULES_SERVICE_R_1`, `DAP_R_1_CONTROLLED_UNIT`, `SFP_8`.
4. Append-only invariant — `remove()` and `replace()` refuse (Canon-3 §22).
5. Rule-id collision refused on re-append.
6. Out-of-set `enforcement_class` value refused at construction.
7. `list_by_class` filter correctness.

## Discipline

- Mechanical RED: `phase0/m2_receipts/20260913T184100Z_M2_SW1_RED.log` (7 fails · right-reason `ModuleNotFoundError` pre-impl).
- Full-suite GREEN #1: `20260913T184300Z_M2_SW1_GREEN2.log` — `3640 passed · 1 skipped · 438 warnings · 116.92s`.
- Full-suite GREEN #2: `20260913T184300Z_M2_SW1_GREEN2.log` — `3640 passed · 1 skipped · 438 warnings · 116.44s` (byte-match).
- `BASELINE_GUARD=1` verify: `20260913T184310Z_M2_SW1_GREEN1.log` — floor honored at 3640.
- Rider 1: `20260913T184310Z_M2_SW1_PIPFREEZE.txt` (190 lines · zero delta from M2 OPEN).

## Ratchet

- Before: **3633**
- After:  **3640** (+7)
- `baseline_failures.json.counts_at_baseline.passed = 3640`
- `baseline_failures.json.invariants_enforced_when_baseline_guard_1.passed_floor = 3640`
- `ratchet_history` append: entry #.  commit SHA backfilled at M2 block close.

## Two-commit local (no push)

- **track-a** · commit `451ef2b` · title *"W-M2-SW1 · W-RULE-REGISTRY-BOOTSTRAP · Doc-0 Attr-4 rule-registry scaffold · Canon-3 §22 append-only · 3 seed rules · ratchet 3633->3640 (+7)"*.
- **master** · this commit.

## Framing / not canon

Attr-4 (Controls) and Attr-9 (Change-Control) roll INTO Rules-Service waves per `BUILD_STATUS §2 row 4d, 4i`.  SW1 lands the first slice of Attr-4.

## No marker retirement in SW1

R-C1 (`custody_class_fallback`) is NOT retired by SW1.  Retirement happens in SW2 (W-RULES-SERVICE-CEREMONY) when the Rules Service is actually invocable end-to-end.  SW1 lands only the register scaffold.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
