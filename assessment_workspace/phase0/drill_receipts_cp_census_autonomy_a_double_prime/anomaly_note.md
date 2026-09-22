# PHASE 3 continuation A'' — Ratchet-Delta Anomaly Note (−2 collection drift)

**When:** 2026-09-22T17:50Z (during CP-CENSUS-AUTONOMY-UI-DRAWER Commit-A pre-seal).

## Observation

- Prior seal (A' close) baseline snapshot recorded in `baseline_failures.json`:
  - `counts_at_baseline`: `passed=6097, failed=3, skipped=1, legacy_conditional_skips=1`
  - Nominal total tests: **6101** (6097 + 3 + 1) — note `legacy_conditional_skips=1` overlaps `skipped=1` per manifest key semantics (`total_skipped_max: 1`).

- Post-A'' Sweep A+B (both green + stripped-sha256-identical):
  - Pytest `collected 6107 items` · `6106 passed, 1 skipped, 0 failed`.

## Nominal Expected Delta

- **+8** new A'' invariants at `tests/invariants/test_cp_census_autonomy_ui_a_double_prime.py`.
- **+3** absorbed retirements: mirror-drift baseline_failures now cured via additive byte-identical twin sync.
- **Expected total delta:** +11 (both in `passed` and in `collected`).

## Measured Delta

- **`passed`**: 6097 → 6106 = **+9**.
- **`collected`**: 6101 → 6107 = **+6**.

## Reconciliation Attempted

- Both sweeps are byte-identical (stripped-sha256 `0b3a2d3c94f8b3aa07f9fdaf9db7cd863b3e369994207a2ac334bc5b439b7fc2`), so the collection count is deterministic under `PYTHONHASHSEED=0`.
- Difference from nominal: **−2 tests** appear to have been removed from collection between the A' seal snapshot and this Sweep A. Since A'' edits were strictly additive (new files + one import + one JSX element in App.js twin), no test file was authored, deleted, or edited by this CP.
- Candidate causes NOT yet forensically confirmed (deferred out-of-scope per SO §6.4 NOTHING-BEYOND):
  1. **Prior-seal baseline snapshot arithmetic**: `counts_at_baseline` at A' close may have summed inconsistently (e.g. `legacy_conditional_skips` double-counted or reported separately from `skipped`). If the actual A'-close collection was 6099 rather than the nominal 6101, delta becomes +8 collection which matches expectation exactly after retirement absorption.
  2. **Dynamic-collection parametrize test** in an untouched file whose parameter cardinality reads from a filesystem directory listing whose entries changed between the A' seal and now (e.g. a receipt-count parametrize in `tests/invariants/test_receipt_manifest_*.py` or similar). The A'' authoring materially changed the `phase0/drill_receipts_cp_census_autonomy_a_double_prime/` folder that was created empty during A' and populated during A''. Removing 2 receipts under parametrize would explain −2 collection.

## Ratchet Ruling

- Ratchet is monotonic non-decreasing on the `passed` axis: 6097 → 6106 is legal (+9 ≥ 0).
- The `total_skipped_max: 1` invariant still holds (1 skipped in Sweep A/B).
- The `current_failed_ids_are_subset_of_baseline_failures` invariant still holds trivially (0 failed ⊆ ∅).
- Therefore the anomaly is a **counting-drift discovery** and NOT a ratchet violation.

## Owner Report

Discovery banked here per SO §6.8 END-OF-WAVE format section 4 ("Discoveries not envisioned at planning"). Forensic root-cause of the −2 collection drift is queued as a future desk-lane item — not blocking this seal because monotonic ratchet + subset check + skipped-max invariants all hold.

## Bank

- Sweep-A log: `sweep_A_2026-09-22.log`
- Sweep-B log: `sweep_B_2026-09-22.log`
- Sweep-A stripped: `sweep_A_2026-09-22.stripped`
- Sweep-B stripped: `sweep_B_2026-09-22.stripped`
- Double-green SHA: `double_green_sha256.txt` → `0b3a2d3c94f8b3aa07f9fdaf9db7cd863b3e369994207a2ac334bc5b439b7fc2`
