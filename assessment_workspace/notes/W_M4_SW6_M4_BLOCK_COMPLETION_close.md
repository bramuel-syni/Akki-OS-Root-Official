READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M4-SW6 · M4 block-completion composite pin — close

**Sub-wave slot:** 6 of M4 (block-close).  **UTC close:** 2026-09-14T10:56Z.
**Canon:** MPB §M4 discharge scoreboard · DAP-20 · Canon-1 §4.6 · owner directive 2026-09-14 (surface b HELD).

## Scope

`services/journey_assistant/m4_block_completion.py` is the M4 block-close composite invariant.  It asserts:

1. All five M4 sub-wave close-notes (SW1..SW5) are on disk under `notes/`.
2. `SOLVA_EXPLAIN_DAP20_BOUNDARY_MARKER` (landed at SW1) is still byte-identical to canon: contains verbatim "MUST NOT approve, widen scope after commission, or decide any gate" and ends with "It proposes; the gates decide."
3. `SURFACE_B_HELD_MARKER == "SURFACE-B-AGENT-DEPLOY-WIZARD-HELD-BEHIND-BR-15.1-AGENT-DEPLOY-SPEC"` preserved.  Owner directive verbatim `OWNER_HOLD_DIRECTIVE_VERBATIM` present.  Silent flip forbidden.
4. `baseline_failures.json.ratchet_history` records every `W-M4-SW*` wave from SW1 through SW5.
5. Ratchet floor ≥ 3844 (SW5 close target).

## Files landed

* `backend/services/journey_assistant/m4_block_completion.py`
* `backend/tests/invariants/test_wm4_sw6_m4_block_completion.py` — 7 tests.

## Discipline

Strict tests-first held.  Mechanical RED at `phase0/m4_receipts/20260914T105350Z_M4_SW6_RED.log` (7/7 `ModuleNotFoundError`).  Double-green byte-match `3851 passed, 1 skipped, 438 warnings` (stripped-timing diff = 0).

## Ratchet

3844 → **3851** (+7)

## Notes

* SW6 does NOT re-verify SW1..SW5's mechanism.  Each sub-wave already owns its own mechanical RED and byte-match; SW6 verifies the M4 book-keeping is coherent.
* Surface (b) Agent-Deploy Wizard remains HELD per owner directive.  When BR-15.1 Agent-Deploy spec is ratified, an M4-extension sub-wave can lift the HELD marker.
* MPB §M4 promises discharged: Promise #32 (SW5) · Canon-5 §14 (SW2 + SW3) · Canon-6 §3 (structural — Setup guided-sequence composed on SW2/SW3) · Canon-6 §6 (Commissioning composed on SW2/SW3/SW4) · Canon-6 §12 (SW4) · DAP-20 boundary verified (SW1) · Canon-1 §4.6 extension not proliferation (SW1..SW5 all extended `services/journey_assistant/` under one package, no sibling registry).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
