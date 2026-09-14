READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW3 · Watch Learning L-1/L-2 · Certificate Library — close

**Sub-wave slot:** 3 of M3 · Watch Learning fold-in #1.
**UTC close:** 2026-09-14T05:34Z.
**Canon anchors:** Watch_Learning_Amendment_v1 L-1 (A5.19) · L-2 (A5.20 + RBM-23).
**S-7 status:** chartered path begins landing at spec.

## Scope

Certificate library scaffold + A5.20 deterministic satisfaction gate.  RBM-23 tier `system_tcb` enforced at construction.  R-15 seed (5 default rows: DAP-32 canary + four AC-1 ceilings) with `CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE = "PENDING-OVERRIDE"` marker — awaits owner ratifier ruling.

## Ratchet

- Before: **3725**
- After:  **3732** (+7)

## Files landed

- `backend/services/watch/certificate_library.py`
- `backend/tests/invariants/test_wm3_sw3_watch_learning_certificate_library.py` (7 invariants)

## DEFAULT-PENDING-OVERRIDE markers

- `services.watch.certificate_library.CERTIFICATE_LIBRARY_R15_PENDING_OVERRIDE = "PENDING-OVERRIDE"` — R-15 (initial library seed) + R-16 (ratifier role) OPEN owner-input.

## Discipline

- RED `20260914T053000Z_M3_SW3_RED.log` (7 fails · right-reason `AttributeError`).
- GREEN #1 `20260914T053200Z_M3_SW3_GREEN1.log` — 3732 passed.
- GREEN #2 `20260914T053400Z_M3_SW3_GREEN2.log` — 3732 passed (byte-match).
- Rider 1 `20260914T053400Z_M3_SW3_PIPFREEZE.txt` (190 lines · zero delta).

## Two-commit local (no push)

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
