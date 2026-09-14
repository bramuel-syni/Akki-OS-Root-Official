READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW4 · Watch Learning L-3 + DAP-32+ minor-flag extension — close

**Sub-wave slot:** 4 of M3 · Watch Learning fold-in #2.
**UTC close:** 2026-09-14T05:40Z.
**Canon anchors:** Watch_Learning_Amendment_v1 L-3 (A5.21 · DAP-32+ · AC-15).
**Minor-flag resolution:** owner ruling 2026-09-13 · "implement the DAP-32+ per-requirement provocation-scenario extension AT BUILD TIME within M3; do NOT reopen the closed M1 wave 2H."

## Scope

- **A5.21** · `MirageCertificateGround` model with isolation check.
- **DAP-32+** · `ProvocationScenario` + `run_provocation_battery` + `get_provocation_battery_for_library` — battery grows with library; entering model producing a certified behaviour fails admission.
- **Cross-reference to M1 2H** · `MINOR_FLAG_DAP_32_PLUS_EXTENSION_HOME` dict cites `cross_ref_wave = "W-DAP-STACK 2H"` and `cross_ref_marker = "DAP_32_PLUS_DEPENDS_ON_SFP_8"`; the M1 marker stays as lineage anchor.

## Ratchet

- Before: **3732**
- After:  **3740** (+8)

## Files landed

- `backend/services/watch/mirage_provocation.py`
- `backend/tests/invariants/test_wm3_sw4_watch_learning_mirage_provocation.py` (8 invariants)

## Discipline

- RED `20260914T053600Z_M3_SW4_RED.log` (8 fails · right-reason `AttributeError`).
- GREEN #1 `20260914T053800Z_M3_SW4_GREEN1.log` — 3740 passed.
- GREEN #2 `20260914T054000Z_M3_SW4_GREEN2.log` — 3740 passed (byte-match).

## Two-commit local (no push)

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
