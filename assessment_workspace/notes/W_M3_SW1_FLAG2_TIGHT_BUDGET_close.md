READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW1 · FLAG-2 tight-budget defensible-write guard — close

**Sub-wave slot:** 1 of M3 · Flag-2 owner-directive (early guard).
**UTC close:** 2026-09-14T05:22Z.
**Canon anchor:** SP 800-53 AU-3(b) · Doc-0 Attr-7 unlowerable · owner directive 2026-09-13 verbatim.
**track-a commit:** `eaa0e04`.

## Scope

Landed the Flag-2 tight-budget guard on the SW5 ReliableClock: any record emitted with `au_3b_defensible=True` MUST bind a drift budget ≤ `TIGHT_DRIFT_BUDGET_MAX_MS` (5 000 ms) before it can reach a governed write.  The loose 24-hour process-local default anchor is intentionally BLOCKED from producing governed defensible writes.

## Files landed

- `backend/services/reliable_time_source/clock.py` — added `TIGHT_DRIFT_BUDGET_MAX_MS`, `LooseAnchorRefused`, `assert_defensible_for_governed_write`.
- `backend/tests/invariants/test_wm3_sw1_flag2_tight_budget_defensible_write.py` (5 invariants).

## Invariants landed

1. Fabric present (`TIGHT_DRIFT_BUDGET_MAX_MS`, `assert_defensible_for_governed_write`, `LooseAnchorRefused`).
2. Tight-budget threshold finite (0 < 5 000 ms ≤ 60 000).
3. Loose default (24 h) refused at write boundary.
4. Tight anchor (100 ms) passes the write boundary.
5. Non-defensible stamp refused independently of budget.

## R-C2 defensibility completion

Flag-2 completes R-C2 defensibility properly: the M2 opt-in mechanism could technically be reached via the loose 24 h default, which would degrade the AU-3(b) claim.  The write-boundary refuses now ensure only ratified-source-anchored tight budgets can produce governed defensible writes.  Downstream per-writer flips (Watch/containment) will bind tight anchors when they land in later M3 sub-waves.

## Ratchet

- Before: **3714**
- After:  **3719** (+5)

## Discipline

- Mechanical RED: `phase0/m3_receipts/20260914T051900Z_M3_SW1_RED.log` (5 fails · right-reason `AttributeError`).
- GREEN #1: `20260914T052000Z_M3_SW1_GREEN1.log` — `3719 passed · 1 skipped · 110.51s`.
- GREEN #2: `20260914T052200Z_M3_SW1_GREEN2.log` — `3719 passed · 1 skipped · 110.40s` (byte-match).
- Rider 1: `20260914T052200Z_M3_SW1_PIPFREEZE.txt` (190 lines · zero delta).

## Env repair note (banked before wave)

Preflight found the CP10 harness receipt >12h old (drift threshold in `test_cp10_harness_receipt_is_still_recent`).  Re-ran the harness driver (`tools/wave_g5_realchrome_verification_harness.py --label cp0a_baseline_drift_repair`) which produced a fresh receipt at `2026-09-14T05:15:51Z` with all 37 rules bound to rendered DOM.  Preflight double-green at 3714 then confirmed × 2 before opening M3 sub-wave 1.

## Two-commit local (no push)

- track-a `eaa0e04` · master this commit.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
