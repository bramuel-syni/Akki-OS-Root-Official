READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW11 · DAP-33/DAP-34/DAP-35 M3-remainder canon-anchor pin — close

**Sub-wave slot:** 11 of M3.  **UTC close:** 2026-09-14T09:15Z.
**Canon:** `MILESTONE_PROMISE_BINDING_20260913.md §M3 'WHEN DONE, THESE PROMISES HOLD'` · S-22 (DAP-33) · S-23 (DAP-34) · S-25 (DAP-35/36).

## Scope

New surface `services/dap/m3_remainder.py` pins the M3-remainder markers from Milestone-Promise-Binding §M3 to the mechanism-side constants that were landed at M1 (W-DAP-STACK 2E disclosure_budget · W-DAP-STACK 2G coalition) and to the owner-ruled default-class approach for R-8/R-11 (owner ruling 2026-09-08T~06:15Z verbatim: *"Security R-8/R-9/R-11 = baseline-period approach"*).

## Files landed

* `backend/services/dap/m3_remainder.py`
* `backend/tests/invariants/test_wm3_sw11_dap33_dap34_dap35_m3_remainder.py` — 8 tests.

## Pins landed

1. `S_22_M3_REMAINDER_VERBATIM` — S-22/DAP-33 M3-remainder canon-anchor string.
2. `R_8_BASELINE_PERIOD == "baseline_period"` and `assert_r8_matches_ruling()` pins `SECURITY_R8_APPROACH`.
3. `S_23_M3_REMAINDER_VERBATIM` — S-23/DAP-34 M3-remainder canon-anchor string.
4. `R_11_BASELINE_PERIOD == "baseline_period"` and `assert_r11_matches_ruling()` pins `SECURITY_R11_APPROACH`.
5. `S_25_M3_REMAINDER_VERBATIM` — S-25/DAP-35/36 M3-remainder canon anchor with BLOCKED-on-R-7 clause.
6. `R_7_BLOCKED_ON_OWNER_INPUT == "BLOCKED-PENDING-OWNER-INPUT"`.
7. `assert_r7_estate_budget_pending_override()` pins BOTH mechanism surfaces (`DEFAULT_RELEASE_BUDGET` in `services/dap/disclosure_budget.py` per-party surface AND `DEFAULT_ESTATE_WIDE_BUDGET` in `services/dap/coalition.py` estate-wide surface) as `DEFAULT-PENDING-OVERRIDE`.  Silent flip of either fires here.
8. Composite pin re-asserts all three markers together.

## Discipline

Strict tests-first held.  Mechanical RED at `phase0/m3_receipts/20260914T091324Z_M3_SW11_RED.log` (8/8 `ModuleNotFoundError` against `services.dap.m3_remainder`).  Double-green byte-match `3790 passed, 1 skipped, 438 warnings` on two consecutive full-suite runs (stripped-timing diff = 0).

## Ratchet

3782 → **3790** (+8)

## Notes

* No mechanism re-implementation.  The M3-remainder pin is a canon-anchor overlay on M1-landed mechanism.
* R-7 remains OPEN (Security estate release budget number) — owner-side input required; silent flip of either `DEFAULT_RELEASE_BUDGET` or `DEFAULT_ESTATE_WIDE_BUDGET` will fire a mechanical RED here.
* R-8 / R-11 baseline-period approach ratified 2026-09-08 (DEFAULT-class).  The pin ensures any future flip of the mechanism-side approach breaks the ratchet.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
