# Wave F · Retirement Charter · D1a-1 Residue Class

Charter opened: 2026-08-27 at CP-D6 close (owner ruling this session · Q2 grant activation).

## Scope

The following **19 files** carry the D1a-1 residual quarantine per CP-D6 Q2 grant (owner ruling verbatim: "If, after CP-D6, the manifest residue is EXCLUSIVELY event-loop class, Q2 is then GRANTED in advance for exactly those files: quarantine expansion with the explicit file list + per-file error counts + Wave-F retirement charter, ceiling updated in the same commit").

Every listed test-node under `@pytest.mark.skip(...)` fails with `RuntimeError: Event loop is closed` under `pytest-asyncio==1.2.0`. Zero semantic-drift residue remains (confirmed post-CP-D6 by tb=line categorization).

| # | file | q'd tests (Q2) | notes |
|---|---|---:|---|
| 1 | `tests/invariants/test_phase_5_stage_b_async_delivery.py` | 19 | Full async-delivery lifecycle: recover / cancel / webhook / idempotency; 32 tests in the same file still pass. |
| 2 | `tests/invariants/test_phase_8_seam_3_sub_stage_1.py` | 17 (12 defs) | Seam-3 refusal-family classifier + coverage marker; 5 tests still pass. |
| 3 | `tests/invariants/test_phase_8_b_5a_compliance.py` | 10 | DPO trace view + refusals-by-month aggregations; 23 tests still pass. |
| 4 | `tests/invariants/test_phase_8_seam_3_sub_stage_2.py` | 8 | Retention loosening + authorized-deletion emit path; 24 tests still pass. |
| 5 | `tests/invariants/test_composed_conclusion_dispatch.py` | 5 | Composed-conclusion floor + dispatch (all live-path exercises). |
| 6 | `tests/invariants/test_dispatch_shape_responsive.py` | 4 | Dispatch shape at admission edges (unknown freshness / warm / fresh forks). |
| 7 | `tests/invariants/test_feasibility_honesty_under_absence.py` | 4 | Feasibility "unknown / stale / censused / never-fabricate" contract. |
| 8 | `tests/invariants/test_qualified_data_selection.py` | 4 | qualified_data selection filters + provenance / license-class refusal. |
| 9 | `tests/invariants/test_engineer_key_grant_ledger.py` | 3 | Engineer-key-grant issuance / revocation / idempotency ledger emit. |
| 10 | `tests/invariants/test_feasibility_dual_consumer_schema.py` | 3 | Feasibility snapshot_ref / reach_ref + dual-consumer schema. |
| 11 | `tests/invariants/test_master_admin_tier_lock_path_a_ledger.py` | 2 | Path-A tier_lock commit emit + idempotency (independent of tier_lock probe: cleanup fixture landed CP-D6 does NOT resolve the loop-teardown class here). |
| 12 | `tests/invariants/test_memory_service_m_g1_to_m_g9.py` | 2 | M-G4 (mind-context isolation) + M-G8 (plane-state reconstructibility). |
| 13 | `tests/invariants/test_8_ext.py` | 1 | EE-G4 approve-flow ledger emit + JWT mint. |
| 14 | `tests/invariants/test_connect_ui1c_gates.py` | 1 | C-B5 ceiling read from single source of truth (17 tests still pass — seeder-drift retirement covered the rest at CP-D6 Q3). |
| 15 | `tests/invariants/test_engineer_key_grant_e2_taxonomy.py` | 1 | E2 taxonomy: grant endpoint role-appropriate response. |
| 16 | `tests/invariants/test_master_admin_auth_reconciliation.py` | 1 | Seeded-admin master role reconciliation. |
| 17 | `tests/invariants/test_memory_engineer_key_grant_e2e_propagation.py` | 1 | M-G E2E single-source users / key-grants never read for auth. |
| 18 | `tests/invariants/test_phase_7_stage_b_1_wizard.py` | 1 | Wizard turn-ledger stamp_audit sidecar. |
| 19 | `tests/invariants/test_qualified_data_outer_gate_ride.py` | 1 | Wire-shape governance-key pins on qualified_data. |
|  | **TOTAL** | **88** |  |

Two files are also fully quarantined at file-level (Q1 residue from CP-D5 · listed under `quarantined_d1a1_files_exclusive`): `test_phase_8_b_5b.py` (26 tests) and `test_phase_8_seam_3_sub_stage_3.py` (45 tests). Combined chartered quarantine: **21 files · 159 tests** (`quarantined_d1a1_max` at CP-D6 close).

## Root cause (owner ruling this session, verbatim)

> "1.2.0 was a good partial win; bank it. No further attempts on pytest-asyncio internals this wave."

Under pytest-asyncio 1.2.0, four D1a-1 files un-quarantined cleanly (CP-D5 Q1 landing). Two files remain 100% cross-loop errored (CP-D5 chartered exclusive). The 88 tests above surface `RuntimeError: Event loop is closed` at teardown or fixture-setup phase — a framework-level teardown-leak class that 1.2.0 does not fully fix and 1.4.0 REGRESSES 151 tests (measured CP-D5).

## Wave F retirement path

Wave F opens when the owner rings the bell for the D1a-1 class. Options (owner decides on Wave F):

1. **Framework upgrade path**: Retry pytest-asyncio ≥1.5.x when released (may include the loop-teardown fix that 1.4.0 lacks). Requires Wave-F pilot on 3-5 chartered files first.
2. **Fixture refactor path**: Re-author `tests/invariants/conftest.py::_motor_rebound_to_loop` OR add a per-test fixture that explicitly closes/reopens Motor+async connections at setup, avoiding the loop-teardown surface entirely. Requires an owner ruling on framework vs code discipline split.
3. **Selective per-file fixture path**: For the higher-value files (phase_5 async delivery, phase_8 seam_3), author dedicated conftest overrides that bypass the Motor rebind pattern (return to plain async fixture).
4. **Contract retreat path**: Retire specific tests as no-longer-needed given upstream refactors (unlikely — most of these are ratified invariants).

## Wave F entry criteria

- Owner opens Wave F explicitly (Wave D remains open until CP-D8 UI mass closes; CP-D7/D8 requires owner UI verification flag).
- pytest-asyncio release cadence (Wave-F option 1) OR owner ruling on framework/code split (Wave-F option 2).
- Q1 landing (pytest-asyncio 1.2.0) STAYS across Wave D → Wave F. Wave F may bump further.

## Guard state at CP-D6 close (banked)

- **manifest**: 0 baseline_failures. Wave D endgame ("manifest=0 + chartered quarantine only") achieved.
- **passed_floor**: 2066 (monotonic ratchet from 2041 at CP-D5).
- **quarantined_d1a1_max**: 159 (21 files).
- **total_skipped_max**: 160 (159 chartered + 1 legacy conditional).
- **quarantined_d1a1_files_exclusive**: 2 (Q1 legacy). Q2 additions are per-test-skipped inside files with mixed pass/quarantine.
