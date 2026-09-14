READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M4-SW3 · estate-check chip inline (§14 · second half) — close

**Sub-wave slot:** 3 of M4.  **UTC close:** 2026-09-14T10:26Z.
**Canon:** Canon-5 §14 (JOURNEY_AND_ASSISTANT_AUDIT §1.2 verbatim, second half).

## Scope

`services/journey_assistant/estate_check_chip.py`:

* `EstateCheckChip` frozen dataclass · `real_estate_read_receipt_id` + `read_source ∈ {live, cached-fresh, cached-stale}` + `summary_text`.
* `__post_init__` refuses construction on empty `real_estate_read_receipt_id` OR non-permitted `read_source` — both raise `FabricatedAvailabilityForbidden`.
* `FeasibilityQuestion` · question wrapper tagged as feasibility-dependent or not.
* `build_feasibility_question_or_refuse` · constructor enforcing the inline-before-feasibility rule: `is_feasibility_dependent=True` without a chip raises `EstateCheckChipMissing`.
* Non-feasibility questions permitted without a chip (shape-only questions like "What outcome are you trying to reach?").
* `to_inline_dict()` for draft-rail render.

## Files landed

* `backend/services/journey_assistant/estate_check_chip.py`
* `backend/tests/invariants/test_wm4_sw3_estate_check_chip.py` — 8 tests.

## Discipline

Strict tests-first held.  Mechanical RED banked at `phase0/m4_receipts/20260914T102117Z_M4_SW3_RED.log` (8/8 `ModuleNotFoundError`).  Double-green byte-match `3827 passed, 1 skipped, 438 warnings` (stripped-timing diff = 0).

## Ratchet

3819 → **3827** (+8)

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
