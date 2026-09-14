READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M4-SW2 · Shaping-Wizard never-pre-fill invariant (§14 · surface a) — close

**Sub-wave slot:** 2 of M4.  **UTC close:** 2026-09-14T10:16Z.
**Canon:** Canon-5 §14 (JOURNEY_AND_ASSISTANT_AUDIT §1.2 verbatim).

## Scope

`services/journey_assistant/never_pre_fill.py` — Canon-5 §14 Shaping-Wizard invariant:

  * `MandatoryFieldSlot` frozen dataclass.  Default `state='empty'` and `value=None`.  `__post_init__` REFUSES construction with `agent_proposed_value != None` OR `state='agent_assumed'` (both raise `AgentPreFillForbidden`).
  * `AgentAskOnly` — the ONE turn shape the wizard emits for a mandatory field; carries only `question_text` + `slot`, no proposed value.
  * `build_ask_turn` — the only ask-turn constructor.
  * `assert_no_prefill_on_mandatory_field` — downstream fail-closed re-check.

## Files landed

* `backend/services/journey_assistant/never_pre_fill.py`
* `backend/tests/invariants/test_wm4_sw2_never_pre_fill_invariant.py` — 8 tests.

## Discipline

Strict tests-first held.  Mechanical RED banked at `phase0/m4_receipts/20260914T101538Z_M4_SW2_RED.log` (8/8 `ModuleNotFoundError`).  Double-green byte-match `3819 passed, 1 skipped, 438 warnings` (stripped-timing diff = 0).

## Ratchet

3811 → **3819** (+8)

## Notes

* The invariant is asymmetric: the USER may fill a mandatory slot (`state='filled_by_user'`), but the AGENT is refused.  This is exactly Canon-5 §14's asymmetry.
* `state='agent_assumed'` is permitted only on OPTIONAL fields (SW3 will land the optional-field surface separately if scoped).  For MANDATORY fields, this state is forbidden.
* The estate-check chip + inline-before-feasibility half of Canon-5 §14 lands in the next sub-wave (SW3).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
