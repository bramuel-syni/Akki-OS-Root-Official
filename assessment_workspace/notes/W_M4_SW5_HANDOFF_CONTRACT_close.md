READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M4-SW5 · Promise #32 registered-handoff-contract generalisation — close

**Sub-wave slot:** 5 of M4.  **UTC close:** 2026-09-14T10:45Z.
**Canon:** Doc-0 Promise #32 · Doc-0 BR-6.1 STATUS · Doc-0 G-13.

## Scope

`services/journey_assistant/handoff_contract.py` — Promise #32 generalisation across four crossing kinds:

* `HandoffKind` enum covers `frontier`, `in_estate`, `plane_to_plane`, `gate_to_gate` — the same registration surface serves all four (G-13 gap closed).
* `HandoffContract` frozen dataclass — checkpoint_id, at_utc, payload_shape, rights_carry_forward_basis + (from_component, to_component).
* `register_handoff` write-boundary — refuses on empty `rights_carry_forward_basis` (raises `RightsCarryForwardMissing`).
* `get_handoff_ledger()` / `reset_handoff_ledger()` — read/reset surface.
* `PROMISE_32_VERBATIM` and `DOC0_BR6_1_STATUS_VERBATIM` canon anchors baked in.

## Files landed

* `backend/services/journey_assistant/handoff_contract.py`
* `backend/tests/invariants/test_wm4_sw5_handoff_contract.py` — 8 tests.

## Discipline

Strict tests-first held.  Mechanical RED banked at `phase0/m4_receipts/20260914T104035Z_M4_SW5_RED.log` (8/8 `ModuleNotFoundError`).  Double-green byte-match `3844 passed, 1 skipped, 438 warnings` (stripped-timing diff = 0).

## Ratchet

3836 → **3844** (+8)

## Notes

* One authoring-time issue caught by SW's own tests: initial `PROMISE_32_VERBATIM` string used a capital "Registered" that didn't match the lowercase test expectation.  Fixed to lowercase to match Doc-0 verbatim wording.
* The generalised surface composes on M2 W-DOC0-ATTR3-TRIAD BA-3.3 op→checkpoint mapping (per MPB §M4).  The op→checkpoint mapping side lives in `services/doc0_attributes/`; SW5 does not touch it — it registers the crossing at the checkpoint boundary.
* Doc-0 BR-6.1 STATUS was "Partial" per Doc-0; SW5 closes the "no generalised registered handoff contract per crossing" gap G-13.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
