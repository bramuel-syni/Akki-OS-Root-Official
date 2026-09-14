READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M3-SW8 · W-PRUNING-UNLEARNING — close

**Sub-wave slot:** 8 of M3.  **UTC close:** 2026-09-14T08:41Z.
**Canon:** `Pruning_Unlearning_Amendment_v1` DAP-37 · DAP-38 · R-12.

## Scope

Three mechanisms landed in `services/dap/pruning_unlearning.py`:

1. **DAP-37 hash-identity invariant.**  `PrunedArtefact` is a frozen dataclass whose `__post_init__` refuses construction when `post_pruning_hash == pre_pruning_hash`, raising `PruningHashCollision` directly (not wrapped in `ValidationError`).  `assert_pruned_artefact_is_new` re-checks downstream so callers holding a value can fail closed if the type was ever bypassed.
2. **DAP-38 rights-withdrawal dispatch.**  `handle_rights_withdrawal(withdrawn_unit, manifests)` iterates `TrainingManifest` records and, for every manifest that cites the withdrawn unit, appends one action: `re_derive` when `was_sisa_sharded=True` (norm), or `recall` when the run was not sharded — with `r12_pending_override = "PENDING-OVERRIDE"` attached so no silent flip is possible while R-12 is unresolved.
3. **DAP-38 budget clause as invariant.**  `budget_refund_forbidden(unit_id)` returns `True` unconditionally.  The function IS the invariant; refund is forbidden on unlearning.

`PRUNING_UNLEARNING_R12_PENDING_OVERRIDE` module constant equals `"PENDING-OVERRIDE"` and rides on every non-sharded action.

## Test file

`tests/invariants/test_wm3_sw8_pruning_unlearning.py` — 6 tests, all citing `Pruning_Unlearning_Amendment_v1` verbatim in module docstring:

* `test_sw8_module_fabric` — required exports present
* `test_sw8_r12_pending_override_marker` — marker == "PENDING-OVERRIDE"
* `test_sw8_pruned_artefact_must_have_new_hash` — DAP-37 constructor refusal on collision + happy path
* `test_sw8_rights_withdrawal_returns_re_derive_or_recall` — DAP-38 sharded norm
* `test_sw8_non_sharded_falls_to_r12_pending_override` — R-12 marker rides on recall
* `test_sw8_budget_not_refunded` — DAP-38 refund-forbidden invariant

## Discipline

Strict tests-first RED-before-mechanism held (no co-authoring concession).  RED phase banked 6/6 `ModuleNotFoundError` for `services.dap.pruning_unlearning` before the module was authored.  Byte-identity double-green at floor 3765.

## Ratchet

3759 → **3765** (+6)

## Open items (unchanged by SW8)

* R-12 stays PENDING-OVERRIDE.  Silent flip forbidden until owner rules on whether re-derivation is mandatory for non-sharded runs.
* SEC-2026-09-12-01 and SEC-2026-09-13-T4-01/03/04/05 remain USER-VERIFICATION-PENDING (owner-side rotations; do not block code+tests work).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
