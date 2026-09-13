READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M2-SW6 · W-SFP-8-SERVING-INTEGRITY — close

**Sub-wave slot:** 6 of M2 · SFP-8 serving-integrity gate.
**UTC close:** 2026-09-13T19:39Z · IN window.
**Canon anchors:** Serving_Integrity_Amendment_v1 §B V-2 (verbatim) · Doc-0 Attr-7 · A20.15 SFP-8 serving floor.
**track-a HEAD delta:** SW6 lands `services.serving_floor.sfp_8` — the callable mechanism DAP-31+/DAP-32+ declared a dependency on at W-DAP-STACK 2H.

## What SW6 resolves

W-DAP-STACK 2H banked `DAP_31_PLUS_DEPENDS_ON_SFP_8` and `DAP_32_PLUS_DEPENDS_ON_SFP_8` as declared-dependency markers gated on M2.  SW6 provides the callable SFP-8 mechanism.  Markers stay in place as Canon-3 §22 lineage anchors.

## Ratchet

- Before: **3672** (SW5 close)
- After:  **3679** (+7)

## Files landed

- `backend/services/serving_floor/__init__.py`
- `backend/services/serving_floor/sfp_8.py`
- `backend/tests/invariants/test_wm2_sw6_sfp_8_serving_integrity.py` (7 invariants)

Full seal in `phase0/m2_receipts/20260913T193900Z_M2_SW6_seal.txt`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
