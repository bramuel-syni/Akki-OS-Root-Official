READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M2-SW3 · W-RULE-BOOK-LIBRARY — close

**Sub-wave slot:** 3 of the M2 block · Rules-Service stack #3 (of 4).
**UTC close:** 2026-09-13T19:19Z (EAT window IN).
**Canon anchors:** Doc-0 Attr-4 (Controls) · Canon-3 §22 (additive) · Canon-3 §9.3 (single-writer) · BUILD_STATUS_PERCENT_20260909 §2 row 4d.
**track-a commit:** `7637783`.

## Scope

Rule-book library — deterministic file-backed source of truth over SW1's RuleRegistry.  Loads jsonl → returns a frozen content-hashed `RuleBook`; `materialise_into_registry` appends into a registry (additive, skip-existing).  Canon-3 §22 supersession requires NEW ids; duplicates in source raise integrity error.

## Files landed

- `backend/services/rules_service/rule_book_library.py` (mechanism).
- `backend/tests/invariants/test_wm2_sw3_rule_book_library.py` (6 invariants).

## Invariants landed

1. Module fabric present (`RuleBook`, `RuleBookImmutable`, `RuleBookIntegrityError`, `load_rule_book_from_jsonl`, `materialise_into_registry`).
2. Deterministic load-from-jsonl.
3. `RuleBook` frozen (pydantic `model_config frozen=True`).
4. `materialise_into_registry` additive with `skip-existing` counted.
5. Duplicate rule ids in source refused (`RuleBookIntegrityError`).
6. `content_hash` exposed (sha256 hex of canonical JSON dump).

## Ratchet

- Before: **3651** (SW2 close)
- After:  **3657** (+6)

## Discipline

- Mechanical RED: `phase0/m2_receipts/20260913T191500Z_M2_SW3_RED.log` (6 fails · right-reason `ModuleNotFoundError`).
- Full-suite GREEN #1: `20260913T191700Z_M2_SW3_GREEN1.log` — `3657 passed · 1 skipped · 438 warnings · 116.60s`.
- Full-suite GREEN #2: `20260913T191900Z_M2_SW3_GREEN2.log` — `3657 passed · 1 skipped · 438 warnings · 116.43s` (byte-match).
- `BASELINE_GUARD=1` verify: 3657 passed at floor 3657 (116.12s).
- Rider 1: `20260913T191900Z_M2_SW3_PIPFREEZE.txt` (190 lines · zero delta).

## Two-commit local (no push)

- **track-a** · commit `7637783`.
- **master** · this commit.

## Framing / not canon

SW3 lands persistence layer only.  Actual 286-rule lift into a seed jsonl + materialisation into the singleton registry is SW4 (W-286-RULE-ENUMERATION-CLASSIFY).

## No marker retirement in SW3

No new marker retirements this sub-wave.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
