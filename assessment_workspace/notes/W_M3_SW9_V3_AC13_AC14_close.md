READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW9 · V-3 · AC-13 (session-freeze contain) + AC-14 (SFP-8 path) — close

**Sub-wave slot:** 9 of M3.  **UTC close:** 2026-09-14T08:58Z.
**Canon:** `Serving_Integrity_Amendment_v1` §C V-3 · AC-13 · AC-14.

## Scope

Two mechanisms landed under `services/agent_containment/serving_freeze.py`:

1. **AC-13 · session-freeze contain.**  `SessionCheckpoint` (frozen dataclass) records `session_id`, `checkpoint_kind ∈ {prefix, recurrent_state}`, `inference_state_ref`, and `depth`.  `freeze_session` appends checkpoints under a session; `resume_session` returns the **deepest surviving** checkpoint (`max(depth)`).  `delete_checkpoint` is a refusing surface — attempting deletion raises `SessionCheckpointDeletedForbidden` (A5.3 stop-without-destroy is a structural invariant, not a comment).  Reversibility is satisfied at deeper granularity than restart-from-turn-zero: if a depth-5 checkpoint exists, resume returns depth 5, never depth 0.

2. **AC-14 · SFP-8-conforming path required for a decision.**  `classify_containment_signal(trigger_reason, serving_path)` calls `services.serving_floor.sfp_8.is_sfp_8_conforming` and dispatches:
   * conforming path → `{"kind": "decision", "may_contain": True}`
   * non-conforming path → `{"kind": "finding", "may_contain": False, "routes_to": "review"}` (finding-not-decision)
   `assert_sfp_8_conforming_for_contain` is the write-boundary helper for callers building a decision — raises `NonConformingPathIsFindingOnly` on a non-conforming path so fail-closed emerges from the type discipline.

## Test file

`tests/invariants/test_wm3_sw9_ac13_ac14_serving_freeze.py` — 7 tests, every docstring citing SIA §C V-3 verbatim:

* `test_sw9_module_fabric` — required exports present
* `test_sw9_ac13_freeze_persists_state_and_halts` — freeze + resume returns deepest checkpoint (monotonic depth)
* `test_sw9_ac13_stop_without_destroy` — `delete_checkpoint` refuses
* `test_sw9_ac14_containment_on_sfp8_conforming_path_is_decision`
* `test_sw9_ac14_containment_on_non_conforming_path_is_finding_only`
* `test_sw9_ac14_assert_helper_refuses_non_conforming`
* `test_sw9_ac13_reversibility_deeper_than_turn_zero`

## Discipline

Strict tests-first RED-before-mechanism held.  RED banked at `phase0/m3_receipts/20260914T085839Z_M3_SW9_RED.log` (7/7 `ModuleNotFoundError` against `services.agent_containment.serving_freeze`).  Double-green byte-match `3772 passed, 1 skipped, 438 warnings` on two consecutive full-suite runs (stripped-timing diff = 0 lines).

## Ratchet

3765 → **3772** (+7)

## Notes

* AC-14 composes on the SFP-8 gate already landed at M2 SW6 (`services/serving_floor/sfp_8.py`).  No new SFP-8 surface introduced.
* AC-11/AC-12 (from SW7) are the graduated-ladder and event-logged prerequisites; SW9 extends the ladder's `contain` rung with the session-freeze option and pins the conforming-path requirement on it.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
