READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P3-CP3 · M9 · Platform-layer connector_mode_lattice · seal note · 2026-09-17T~05:40Z

**Track-a HEAD:** `547ba3975d5ba4a199881eb5c8948f424a685d12`. **Ratchet:** 4534 → **4544** (+10).

## Anchor
§5.3 M-C-2 3-mode verbatim vocabulary · §5.3 M-C-3 (mode enforced in connector runtime) · §5.3 M-C-4 (raising mode requires data_steward/tenant_admin approval + log + task-invalidation).

## Mechanism
`services/platform_control_plane/connector_mode_lattice.py` · `CONNECTOR_MODES = ("discovery", "read", "write")` · `MODE_RANK` dict · `mode_rank(*, mode) -> int` (0/1/2) refuses `UnknownModeRefused` on unknown (case-sensitive) · `assert_downgrade_only(*, from_mode, to_mode) -> None` refuses `UpgradeRequiresApprovalRefused` when `rank(to_mode) > rank(from_mode)`; permits downgrade and same-mode. Upgrade approval is composed at CP-P3-CP4. 3 refusal classes.

## Invariants (10)
Module fabric · CONNECTOR_MODES verbatim tuple · MODE_RANK values · mode_rank refuses unknown (incl. case-mismatch) · refusal hierarchy · assert refuses each of 3 upgrade shapes · assert permits each of 3 downgrade shapes · assert permits same-mode across the 3 · assert refuses unknown from/to · anchor + grep-negative + import-negative.

## Double-green
GREEN1 4544/1/0 · GREEN2 4544/1/0.

## §3.3
- A `547ba3975d5ba4a199881eb5c8948f424a685d12` ✅.
- B `29a6da446c4b250cba2c476ad470811dd1699640` ✅.
- C this-turn.

## GPU util
Elapsed **25.79 h** · remaining **46.21 h**.

## CONTRACT-MODELED items enabled
- **Item 14** · Real connector runtime enforcing mode. Vocabulary + partial order + upgrade-refuses-without-approval shape-frozen so the connector-runtime binding is a bind-only change.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
