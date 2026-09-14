READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M4-SW4 · three-verdict discipline (Canon-6 §12) — close

**Sub-wave slot:** 4 of M4.  **UTC close:** 2026-09-14T10:36Z.
**Canon:** Canon-6 §12 (JOURNEY_AND_ASSISTANT_AUDIT §1.4 verbatim).

## Scope

`services/journey_assistant/three_verdicts.py` — Canon-6 §12 enforcement:

* `JourneyVerdict` enum: exactly 3 values (`answered`, `held`, `refused`).
* `resolve_step` write-boundary: refuses any non-canon verdict with `FourthVerdictForbidden`.
* `held` verdict without `held_until_reason` refused (`HeldWithoutReasonForbidden`).
* `refused` verdict binds a `SolvaAction` from SW1 (Canon-4 §24 three-action envelope) — closing the loop between §12 and §24.
* `StepResolution` frozen record.

## Files landed

* `backend/services/journey_assistant/three_verdicts.py`
* `backend/tests/invariants/test_wm4_sw4_three_verdicts.py` — 9 tests.

## Discipline

Strict tests-first held.  Mechanical RED banked at `phase0/m4_receipts/20260914T103246Z_M4_SW4_RED.log` (9/9 `ModuleNotFoundError`).  Double-green byte-match `3836 passed, 1 skipped, 438 warnings` (stripped-timing diff = 0).

## Ratchet

3827 → **3836** (+9)

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
