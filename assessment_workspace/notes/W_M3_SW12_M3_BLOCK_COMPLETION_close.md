READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW12 · M3 block-completion composite pin — close

**Sub-wave slot:** 12 of M3.  **UTC close:** 2026-09-14T09:22Z.
**Canon:** `MILESTONE_PROMISE_BINDING_20260913.md §M3 'WHEN DONE, THESE PROMISES HOLD'`.

## Scope

New surface `services/dap/m3_block_completion.py` is the M3 block-close composite invariant.  It asserts:

1. All eleven M3 sub-wave close-notes are on disk under `notes/`.
2. Every `DEFAULT-PENDING-OVERRIDE` marker across M3 is preserved: R-7 on both `disclosure_budget.DEFAULT_RELEASE_BUDGET` (per-party) and `coalition.DEFAULT_ESTATE_WIDE_BUDGET` (estate-wide); R-12 on `pruning_unlearning.PRUNING_UNLEARNING_R12_PENDING_OVERRIDE`; BC-3/BC-4 on `business_continuity.anchors`.
3. `baseline_failures.json.ratchet_history` records every `W-M3-SW*` wave from SW1 through SW11.
4. `S-24 (A5.17)` canon anchor pinned verbatim with `S_24_MECHANISM_DEFERRED == "MECHANISM-DEFERRED-BEYOND-SW11"` — honest gap, not silently swallowed.
5. Ratchet floor ≥ 3790 (SW11 close target).

## Files landed

* `backend/services/dap/m3_block_completion.py`
* `backend/tests/invariants/test_wm3_sw12_m3_block_completion.py` — 7 tests.

## Discipline

Strict tests-first held.  Mechanical RED at `phase0/m3_receipts/20260914T091918Z_M3_SW12_RED.log` (7/7 `ModuleNotFoundError`).  Double-green byte-match `3797 passed, 1 skipped, 438 warnings` on two consecutive full-suite runs (stripped-timing diff = 0).

## Ratchet

3790 → **3797** (+7)

## Notes

* Honest gap: **S-24 (A5.17 Raiser-held-to-target-conformance)** canon anchor is on record with mechanism DEFERRED beyond SW11.  If a future M3-extension wave is opened, S-24's Class-D/Class-A finding mechanism + lineage collapse lands there.
* SW12 does NOT re-verify SW1..SW11's mechanism.  Each sub-wave already owns its own mechanical RED and byte-match; SW12 verifies the M3 book-keeping is coherent.
* Composite invariants: any silent flip of any M3 PENDING-OVERRIDE marker will fire here **and** at the individual sub-wave's own pin (defence-in-depth).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
