# Wave D Grounding Brief · Verbatim REUSABLE Row Landings · 2026-08-27

**Owner Condition 1 (2026-08-26, binding):** «Every requirement you implement must be built from the VERBATIM spec text, and the verbatim quote (doc + § + exact words) must appear in the gating test's docstring and the drill receipt. If the quote isn't in the test, the test doesn't gate the row.»

**Owner Condition 2 (2026-08-26, binding):** «after any compaction, re-read this brief before touching Wave D code.»

**Owner standing addition (2026-08-27 · CP-D-guard approval message):** «the waveD grounding brief (step 5) must QUOTE each REUSABLE row's spec text verbatim with the donor path + LOC — it doubles as the CP partition for D2..D8.»

**Owner sequencing ruling (2026-08-27 · CP-D-guard approval message):**

> «Lowest-hanging first is approved: the pydantic 2.13 `additionalProperties` snapshot class and stale-expected-value class are ideal CP-D2 pay-down candidates — mechanical, receipt-friendly, and they clear whole files. Adjacency to the CP's lift scope is preferred where it exists, never required.»

> «Proceed: guard → grounding brief → CP-D2. Stop-and-report at CP-D2 close with the manifest trajectory (116 → ≤101). SSH interrupt stands.»

**Owner ratchet ruling (2026-08-27 · CP-D-guard approval message):** «add the regression floor `passed >= 1932`, and make it a MONOTONIC RATCHET: each CP close updates the floor to that run's passed count in the same commit (floor only ever rises).»

**Owner drift ruling (2026-08-27 · CP-D-guard approval message):** «HALT AND REPORT. No silent rebaselining, ever — the manifest is a ratified artifact.»

---

## §0 · Standing conditions inherited from Waves A/B/C (still binding)

- Ship-Manifest DoD triple: runtime-assembler wiring (`backend/server.py` AND `pod_shell/backend/server.py` byte-identical mirror) + `MUST_BE_LIVE_ROUTES` extension for any new wire path + green invariant test — one commit.
- Callers-Cover-the-Rule DoD: for every "every X does Y" register row, DONE requires a producer-side test proving Y fires.
- Tests-first is law: RED receipt banked before implementation. Verbatim spec quote in every gating docstring.
- `pydantic 2.13.4`, single chokepoint, REFERENCE-NOT-COPY, DELETIONS-REQUIRE-MAPPING.
- Local commits only. NO push.
- GPU-dependent work sequenced LAST; mock SSH seam first (INTERRUPT-PRIORITY: interrupt Wave D immediately when SSH key arrives).

## §1 · CP-D-guard baseline (ratified · CP-close of the pre-flight)

- Manifest: `backend/tests/invariants/baseline_failures.json` (116 IDs, sorted, unique).
- Quarantined: 165 D1a-1 skips in six files (exclusive list in manifest).
- Passed floor: **1944** (raised from 1932 by the +12 manifest-integrity companion tests; monotonic ratchet in effect).
- CP-close invocation for every future Wave-D lift CP:
  ```
  cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/
  ```
- Receipt format required in every CP-close drill log: `passed=<N> / baseline-failures-remaining=<K> / quarantined=<Q>`.

## §2 · Governing canon anchors for Wave D (17-doc scheme)

Wave D covers REUSABLE rows across seven 17-doc anchors. Each anchor is fixed by its umbrella canon reference (Canons 1-9) recorded verbatim in `notes/requirements_register_17docs.md` and expanded in `notes/requirements_register_20docs.md`.

| Doc-N | Title | Umbrella canon anchor | REUSABLE donor(s) (§ `notes/reuse_map_v7.md`) |
|:-----:|-------|-----------------------|-----------------------------------------------|
| Doc 04 | Reasoning · Solver (Solva) | Canon 4 §§3-20 | `Akki-OS-V1/backend/services/solva_depth/`; `Akki-Executive-Core/backend/services/solva_v2/` |
| Doc 05 | Direction / Scope / Focus (Northena) | Canon 4 §§30-36 | `RMS-IQ-Core-2/backend/services/northena/`; `Akki-OS-V1/backend/services/northena/` |
| Doc 06 | Progressive Disclosure | Canon 4 §§42-45 | `Akki-Executive-Core/backend/services/analyze_workspace/` (context-selection primitives) |
| Doc 07 | Shrinkage · Five-ring unit | Canon 2 §§20-24 | `RMS-IQ-Core-2/backend/services/perception/` + `layer_a/`, `layer_b/`, `layer_c/` |
| Doc 08 | Memory & Retrieval (warm/fresh fork) | Canon 2 §§32-38 | `Akki-Executive-Core/backend/services/platform_kb.py`; `Akki-Executive-Core/backend/services/continue_chat.py` |
| Doc 13 | Autonomous Training (Targeta) | Canon 4 §§55-68 | `RMS-IQ-Core-2/backend/services/targeta/`; `Akki-Executive-Core/backend/services/sandbox_generation.py` |
| Doc 15 | Governance Ceremony · Orchestration | Canon 3 §§50-63 · Canon 9 §§4-8 | `Akki-Executive-Core/backend/services/monitor/`, `cycle_lifecycle.py`, `cycle_permissions.py`; `RMS-IQ-Core-2/backend/services/master_admin/` |
| Doc 16 | Cross-Cutting Orchestration | Canon 6 §§4-9 | `Akki-Executive-Core/backend/services/work_studio/`, `inbox_routing/` |

## §3 · CP-D2..CP-D8 partition (canonical-seam ordering)

The partition is by canonical seam per row_to_item_index bundling discipline (§8-`notes/row_to_item_index.md`) — never by convenience or file count.

| CP | Anchor(s) | Row seam | Pay-down class(es) preferred (owner ruling (e)) |
|:--:|-----------|----------|-------------------------------------------------|
| **CP-D2** | Cross-cutting (contract-snapshot family + housekeeping) | Frozen-contract snapshot bijection under pydantic 2.13 · `additionalProperties` schema regeneration | pydantic 2.13 `additionalProperties` snapshot class (byte-identical family) + stale-expected-value floor class |
| CP-D3 | Doc 04 · Solva | Reasoning gate + evidence gate + refusal envelope | `test_composed_conclusion_dispatch.py` cluster + `test_service_1_refusal_envelope.py` family |
| CP-D4 | Doc 05 · Northena + Doc 07 · Perception | Admit/Gate/Converge loop + five-ring stages | `test_9_2a_real_perception.py`, `test_census_dimensions.py` cluster |
| CP-D5 | Doc 08 · Memory & Retrieval | Warm/fresh fork + trace-lens correlation | `test_trace_lens_cross_engine_correlation.py`, `test_memory_service_m_g1_to_m_g9.py` cluster |
| CP-D6 | Doc 13 · Targeta | Six-criterion MOAC · standing re-check date · adapter registry read-back | `test_master_admin_tier_lock_path_a_ledger.py`, `test_engineer_key_grant_*` cluster |
| CP-D7 | Doc 15 · Governance Ceremony | Rules ceremony · propose·counter-sign·countdown·apply·re-check · SoD | `test_govern_g_g1_to_g_g8.py`, `test_govern_ui1b_gates.py`, `test_p1_custody_closure.py` |
| CP-D8 | Doc 16 · Cross-cutting orchestration | Handoff contract v0 · walk-this · claim-to-evidence trace | `test_registry_prove_ui1d_gates.py`, `test_team_ui1e_gates.py` (surface parity floors), `test_solva_trace_ledger_integration.py` |

Each CP MUST retire ≥15 baseline_failures from the manifest in the same commit AND ratchet `passed_floor` + `counts_at_baseline.passed` up (monotonic).

## §4 · CP-D2 · Verbatim scope (opening CP)

### §4.1 · Owner-ruled pay-down class (verbatim quote, this session)

> «Lowest-hanging first is approved: the pydantic 2.13 `additionalProperties` snapshot class and stale-expected-value class are ideal CP-D2 pay-down candidates — mechanical, receipt-friendly, and they clear whole files. Adjacency to the CP's lift scope is preferred where it exists, never required.»

### §4.2 · Failure classes in scope from the baseline manifest

**Class A · pydantic 2.13 `additionalProperties` snapshot drift (byte-identical contract-snapshot family).** Members observed in the 116-row manifest:

- `tests/invariants/test_v0_paths_byte_identical_after_5b.py::test_prior_contract_file_byte_identical_after_5b[northena_ledger.py-68349bb0…]`
- `tests/invariants/test_v0_paths_byte_identical_after_6b.py::test_prior_contract_file_byte_identical_after_6b[northena_ledger.py-68349bb0…]`
- `tests/invariants/test_v0_paths_byte_identical_after_7b_1.py::test_prior_contract_file_byte_identical_after_7b_1[northena_ledger.py-68349bb0…]`
- `tests/invariants/test_transform_forms.py::test_v0_paths_byte_identical_at_transform_forms_close`
- `tests/invariants/test_v2_gate_refusal_cumulative.py::test_v2_refusal_envelope_contract_frozen`
- `tests/invariants/test_outer_gate_irreversibility.py::test_outer_gate_receipt_contract_frozen`
- (and additional members to be enumerated at CP-D2 open commit)

**Class B · Stale-expected-value floor drift.** Members observed in the 116-row manifest:

- `tests/invariants/test_9_2a_real_perception.py::test_v1_g7_attestation_parity_31_at_9_2a_close`
- `tests/invariants/test_census_dimensions.py::test_v1_g7_attestation_parity_31_at_census_dimensions_close`
- `tests/invariants/test_govern_g_g1_to_g_g8.py::test_g_g1_parity_unchanged`
- `tests/invariants/test_govern_ui1b_gates.py::test_g_b12_no_new_frozen_contracts_parity_36`
- `tests/invariants/test_memory_observability_o_g1_to_o_g6.py::test_o_g_parity_expected_parity_unchanged_at_34`
- `tests/invariants/test_memory_service_m_g1_to_m_g9.py::test_m_g_parity_34_at_memory_service_stage_b_close`
- `tests/invariants/test_team_ui1e_gates.py::test_e_g1_parity_36_unchanged`
- `tests/invariants/test_connect_ui1c_gates.py::test_c_b9_parity_36_unchanged`
- `tests/invariants/test_registry_prove_ui1d_gates.py::test_d_g1_parity_36_unchanged_no_new_frozen_contracts`

Pattern (per CP-D1a receipt Section E, verbatim): «hardcoded `len(snapshots) == N` updated to `>= N` with docstring documenting the wave-close snapshot count as a floor, not a cap. Snapshot-count bijection remains delegated to the authoritative `test_frozen_contract_snapshot_parity.py` (green).»

### §4.3 · Applicable spec anchor (per Owner Ruling 2026-08-26 §6 · additive-only correction discipline)

> «Nothing in the prior file is edited; the new N rows land as a strict addition, so any downstream code referencing the [prior] register still resolves.» — `notes/requirements_register_20docs.md` (line 6-8)

Corollary discipline for CP-D2 pay-down: for every parity-count assertion converted from `== N` to `>= N`, the docstring MUST record the observed count at conversion time, cite the CP-D2 receipt, and delegate authoritative snapshot bijection to the frozen-contract snapshot parity test.

For every pydantic 2.13 `additionalProperties` byte-identical failure, the drift is regenerating the contract snapshot with pydantic 2.13's schema output where the model schema is unchanged; the fix is to regenerate the snapshot artifact (`*.contract_snapshot.json`) using the current pydantic 2.13.4 output, NOT to touch the model.

### §4.4 · Ship-Manifest DoD posture for CP-D2

- **No new wire path.** CP-D2 is pay-down + snapshot regeneration only. `MUST_BE_LIVE_ROUTES` untouched. `pod_shell/` mirror untouched. Live-pod curl not applicable.
- **New invariant test** (if any new gating test is added for a re-shaped assertion class): must land with a verbatim canon-quote docstring per Owner Condition 1.
- **Manifest shrink invariant:** the CP-D2 commit MUST reduce `baseline_failures.json.baseline_failures` array length by ≥15 and MUST raise `counts_at_baseline.passed` + `invariants_enforced_when_baseline_guard_1.passed_floor` to the CP-close observed passed count.

### §4.5 · Ratchet at CP-D2 close (target)

- Baseline failures target: **≤ 101** (owner ruling: «Stop-and-report at CP-D2 close with the manifest trajectory (116 → ≤101)»).
- Passed count target: **≥ 1959** (1944 + 15 pay-down; typically higher if the fix reactivates whole test classes).
- Skipped: **166 unchanged** (D1a-1 quarantine + 1 legacy conditional skip; ratchet ceiling still 165 + 1).

## §5 · CP-D3..CP-D8 · Row enumeration discipline

Per Owner Condition 1, each of CP-D3..CP-D8's REUSABLE row landings requires verbatim canon quotes in this brief PRIOR to the CP opening. This brief GROWS at each CP-open commit, following the same convention as `waveA_grounding_brief.md` (which grew across R1..R7).

Each future CP-open section will contain, at minimum:

1. The verbatim owner ruling opening the CP (if any beyond this brief's global rulings).
2. For every REUSABLE row landed: `Doc-NN-XXX · <canon §> · «verbatim quote» · donor: `<repo>/<path>`:LOC`.
3. The Ship-Manifest DoD posture (wire path? mirror change? `MUST_BE_LIVE_ROUTES` extension?).
4. The manifest ratchet target (baseline_failures shrink ≥15 · passed_floor rise).
5. The pay-down class(es) chosen for the CP.

Adherence pattern (owner ruling 2026-08-26 §6): «additive-only correction discipline» — this brief is EXTENDED, never mutated backwards.

## §6 · SSH interrupt-priority sequence (retained verbatim from `STATE/NEXT.md`)

> «(a) SSH key path — Live GPU sequence (INTERRUPT-PRIORITY: interrupt Wave D immediately on key arrival):
> 1. `chmod 600 <key>` on the delivered private key.
> 2. `AKKI_GPU_SSH_PRIVATE_KEY_PATH=<path>` set in `/app/backend/.env`.
> 3. `GPU_CONNECT_MODE=real` env flip.
> 4. Hardware fact sheet probe · `nvidia-smi` + CUDA version + PyTorch build.
> 5. CUDA/PyTorch verify-only (owner confirms already installed — A17.17 CLOSED): capture versions in hardware fact sheet; install ONLY if probe contradicts owner confirmation, and report the contradiction.
> 6. EP-4 precondition: terminal-test ordering guard green — evidence register active AND ≥2 registered judges with matching versions for site `terminal_test`; live run refuses to start otherwise.
> 7. First live governed training run on sealed DigiCow set (fresh verification bench).
> 8. Real MOAC card (mocked=False on all six criteria).
> 9. Whitepaper drafted from a real admission (`accept_for_service=True` path becomes possible).
> 10. Stop-and-report with hardware fact sheet + live run outcome.»

## §7 · Stop-and-report gate

Per owner ruling (this session, verbatim): «Stop-and-report at CP-D2 close with the manifest trajectory (116 → ≤101).»

That trigger fires the moment CP-D2 closes with a guard-active green receipt and the manifest shrunk to ≤101 baseline_failures. Wave-D continues at owner's subsequent ruling.
