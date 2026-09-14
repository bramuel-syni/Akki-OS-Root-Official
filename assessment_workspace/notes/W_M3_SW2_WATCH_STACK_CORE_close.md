READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW2 · W-WATCH-STACK core — close

**Sub-wave slot:** 2 of M3 · Watch stack core.
**UTC close:** 2026-09-14T05:28Z.
**Canon anchors:** Doc-0 §7 · BR-7.1 · BR-7.4 · Ratification_Record_v1 R-3 RATIFIED.
**track-a HEAD delta:** new file `services/watch/verdict_interface.py` + test file · +6 invariants.

## Scope

Verdict interface + four-rung action ladder (annotate · shape · contain · sever) with BR-7.4 gate: Learned-source verdicts refused directly; must route through a Deterministic gate.  Composes with SW13 (Doc-0 Attr-10 · Determinism classifier).

## Ratchet

- Before: **3719**
- After:  **3725** (+6)

## Files landed

- `backend/services/watch/verdict_interface.py`
- `backend/tests/invariants/test_wm3_sw2_watch_stack_core.py` (6 invariants)

## Discipline

- RED `20260914T052400Z_M3_SW2_RED.log` (6 fails · right-reason `AttributeError`).
- GREEN #1 `20260914T052600Z_M3_SW2_GREEN1.log` — 3725 passed.
- GREEN #2 `20260914T052800Z_M3_SW2_GREEN2.log` — 3725 passed (byte-match).

## Two-commit local (no push)

- track-a HEAD · master this commit.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
