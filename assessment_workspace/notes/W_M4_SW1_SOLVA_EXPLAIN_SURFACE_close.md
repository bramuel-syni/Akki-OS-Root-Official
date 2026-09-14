READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M4-SW1 · Solva-explain surface (§4.5 · surface c) — close

**Sub-wave slot:** 1 of M4.  **UTC close:** 2026-09-14T10:05Z.
**Canon:** Canon-4 §24 · Canon-5 §29 · DAP-Spec DAP-20.
**Owner priority (2026-09-14):** surface (c) Solva-explain FIRST.

## Scope

New surface `services/journey_assistant/solva_explain.py` — user-facing "walk me through why the answer stopped here and what I should do" wrapper for Solva refusals.

Mechanism:

1. **CANON_4_S24_THREE_ACTIONS_VERBATIM** — canon anchor string baked verbatim; drift ⇒ RED.
2. **SOLVA_EXPLAIN_DAP20_BOUNDARY_MARKER** — DAP-20 boundary verbatim, rides on every explanation.
3. **SolvaAction** enum has exactly three values (`accept_as_stated`, `narrow_objective`, `lower_standard`).
4. **`explain_refusal`** — write-boundary constructor; refuses a fourth action with `FourthActionForbidden`.
5. **`SolvaExplanation.decide_gate()`** — always raises `SolvaExplainMustNotDecide` (DAP-20 boundary: "It proposes; the gates decide").
6. **`SolvaExplanation.to_answer_card()`** — serialises into the Canon-5 §29 answer-card shape.

## Files landed

* `backend/services/journey_assistant/__init__.py`
* `backend/services/journey_assistant/solva_explain.py`
* `backend/tests/invariants/test_wm4_sw1_solva_explain_surface.py` — 7 tests.

## Discipline

Strict tests-first held.  Mechanical RED banked at `phase0/m4_receipts/20260914T100553Z_M4_SW1_RED.log` (7/7 `ModuleNotFoundError`).  Double-green byte-match `3811 passed, 1 skipped, 438 warnings` (stripped-timing diff = 0).

## Ratchet

3804 → **3811** (+7)

## Notes

* No re-implementation of the three-action envelope itself — that's already at `services/solva_v2/` CP-S4 (W-SOLVA-V2-LIFT).  This surface is the user-facing routing wrapper §4.5 named as absent.
* `[framing, not canon]`: §4.5 JOURNEY_AND_ASSISTANT_AUDIT identifies the absence of a Solva-facing chat surface.  This SW1 delivers the deterministic user-facing surface for it, without introducing a chat/LLM stream — the wrapper is a structural surface, not a conversational one.  Any conversational Solva-explain UI is deferred behind future ownership.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
