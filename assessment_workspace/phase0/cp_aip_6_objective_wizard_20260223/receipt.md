# CP-AIP-6-OBJECTIVE-WIZARD · Comprehensive Seal Receipt

**Seal timestamp:** 2026-02-23T07:50:00Z
**Ledger anchor:** EXECUTION_ORDER.md Item 5.6 · CP-AIP-6 (Objective Wizard compile-time rejections + Collection Schema baseline v1.0 + Registry Namespace sealed-not-deleted · AIP v1.0 §8 + §9 + §12.1)
**Owner authorization:** Owner cadence directive verbatim (2026-02-23 CP-AIP-4 GO): 'run CP-AIP-5 → CP-AIP-10 sequentially; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>.' + Item-4 checkpoint GO + §16.1 (c) CLEAN receipt.

**Ledger check** — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else.

---

## 1 · Scope

The Objective Wizard compile boundary + Collection Schema two-tier contract + Registry Namespace sealed-not-deleted per AIP v1.0 §8 + §9 + §12.1. FIVE additive modules composing sealed CP-M11-wizard state machine + `WizardCommitState_v0` via §1.2 modality-extension. Zero sealed-carrier edit per SO §3.8 · §16.1 (c) CLEAN receipt applied verbatim (sibling contract; sealed `WizardCommitState_v0` NOT edited).

### §8.4 compile-time rejections enforced structurally:
- **(a)** `TestSetRefMissing` — Outcome without existing `test_set_ref` refused at compile.
- **(b)** `AcceptanceBarNotStratified` — Acceptance bar missing per-stratum dimension refused (§10.2 verbatim: 'Acceptance is per stratum').
- **(c)** `CustodyViolation` — CollectionSchema column carrying any §6.2-custody-violating token refused via structural scan.

### §9.2 baseline tier v1.0 verbatim 5-tuple:
`("language_identification", "code_switch_points", "condition_profile", "dedup_instance_condition_map", "synthesis_relevant_group_level_acoustics")` — encoded as `Final[Tuple[str, ...]] BASELINE_TIER_V1_0_CONTENTS` in `collection_schema_v0.py`. PENDING-OWNER-CONFIRMATION per §16.2 · ceremony-governed for any additive change per §9.2 last sentence.

### §12.1 registry namespace verbatim:
- `AudioModalityNamespace_v0.close()` → `namespace_state='sealed'` (never `'deleted'`; structural §1.5 · no `delete()` method).
- `write_data_point()` returns new frozen namespace with append-only `ScopedWrite_v0` (every scoped write carries `commission_id`).
- Reads compose with global registry; writes namespace-scoped.

### §8.5 ObjectiveSession_v0 ledger stamping:
- Frozen dataclass with 6 carriers (`session_id` + `variant` + `options_considered` + `options_rejected` + `target_outcome_ref` + `collection_schema_ref`).
- `options_rejected` structurally a subset of `options_considered` (`__post_init__` gate).

### New additive modules (5 files):
- `backend/contracts/target_outcome_v0.py` (~85 lines · `TargetOutcome_v0` + `StratumAcceptance_v0` + closed-set `GATE_POLICIES`).
- `backend/contracts/collection_schema_v0.py` (~65 lines · `CollectionSchema_v0` + `BASELINE_TIER_V1_0_CONTENTS` + `CUSTODY_VIOLATING_TOKENS`).
- `backend/contracts/wizard_objective_commit_state_v0.py` (~80 lines · `ObjectiveSession_v0` + `OBJECTIVE_VARIANT_NAME`).
- `backend/services/wizard/objective_compile.py` (~135 lines · `compile_target_outcome` + `compile_collection_schema` + 3 refusal classes).
- `backend/services/registry/audio_modality_namespace.py` (~120 lines · `AudioModalityNamespace_v0` + `ScopedWrite_v0` + `NamespaceState` Literal).

### RED-first invariant pins (10):
| # | Pin name | Spec anchor |
|---|---|---|
| 1 | `test_compile_rejects_outcome_without_test_set_ref` | §8.4 verbatim + §10.2 |
| 2 | `test_compile_rejects_acceptance_bar_without_per_stratum_dimension` | §8.4 + §10.2 |
| 3 | `test_compile_rejects_collection_schema_with_custody_violating_column` | §8.4 + §6.2 |
| 4 | `test_baseline_tier_contents_match_v1_0_exact_verbatim` | §9.2 verbatim + §16.2 |
| 5 | `test_registry_namespace_closes_to_sealed_never_deleted` | §12.1 verbatim + §1.5 |
| 6 | `test_registry_namespace_writes_are_scoped_reads_compose_global` | §12.1 verbatim |
| 7 | `test_wizard_objective_commit_state_has_objective_session_data_class` | §8.5 verbatim |
| 8 | `test_objective_session_records_options_considered_and_rejected` | §8.5 verbatim |
| 9 | `test_new_modules_do_not_redeclare_sealed_wizard_carriers` | §1.2 + §16.1 (c) |
| 10 | `test_new_modules_cite_section_anchors_and_ledger_check` | Anti-drift §3 + §5 |

---

## 2 · RED-first evidence

- RED_pre: 10/10 failed 0.69s (authentic ModuleNotFoundError + AssertionError right-reason).
- GREEN_post: 10/10 passed 0.71s.

Drill receipts banked at `backend/phase0/drill_receipts_cp_aip_6_objective_wizard/`.

---

## 3 · Pre-Commit-A double-green byte-identical sweep (BASELINE_GUARD=1 PYTHONHASHSEED=0)

- **Sweep A:** 6311 passed / 1 skipped / 0 failed / 520 warnings in 187.62s (real 3m10.152s).
- **Sweep B:** 6311 passed / 1 skipped / 0 failed / 520 warnings in 186.30s (real 3m8.984s).
- **stripped_sha256 (both sweeps):** `8d8518c9dc0f75a545dfe3b0c7452dd9128eef0a6b7ecd1d492427d44b20e4a3` — **IDENTICAL**.

Pre-Commit-A wire-up trips (fixed additively):
1. **Vendored twin sync trip** — 1050 → 1055 (5 new modules) · structural_sha256 `ca3684c454fd14a75d7724610006cb8c92ba739b82604fc3909be422e9d12749`.
2. **ORCH_BOOT ratchet-only regen trip** — ratchet.passed_floor 6292 → 6302 + baseline_failures.json sha256 to `3750f45c6126a723efbe559762060edee6b02f5aabb22b32edaa811afb2d6885`.
3. **Frozen contract snapshot parity trip** — 3 new frozen-dataclass modules added to `NON_CONTRACT_UTILITY_MODULES` per established FL-P4-W6-08 pattern (append-only exempt-list · like `canon_census_source_candidate.py`, `data_suite_workspace.py`).

Raw + stripped logs banked at `phase0/cp_aip_6_objective_wizard_20260223/sweep_A.log` + `sweep_A.stripped` + `sweep_B.log` + `sweep_B.stripped`.

---

## 4 · Ratchet bump

- **Floor:** 6292 → 6302 (+10 canonical measured pins).
- **baseline_failures.json sha256 pre-bump:** `5deb18b96c28659fed8e71f47abfef57d27177097164c772be1cc3f0080557cd` (post-CP-AIP-5).
- **baseline_failures.json sha256 post-bump:** `3750f45c6126a723efbe559762060edee6b02f5aabb22b32edaa811afb2d6885`.
- Written with `indent=2, ensure_ascii=False` per BL #7 + BL #11.
- `ratchet_history` entry appended (`passed=6302`).
- `invariants_enforced_when_baseline_guard_1.passed_floor` advanced 6292 → 6302 in lock-step.

---

## 5 · Sealed carriers UNCHANGED (SO §3.8 additive-only)

- `backend/contracts/wizard_commit_state.py` (M11 wizard · sealed · NOT edited · sibling contract lands objective variant per §16.1 (c) CLEAN receipt).
- `backend/services/wizard/operator_state_machine.py` (sealed).
- `backend/services/wizard/turn_ledger.py` (sealed).
- `backend/services/wizard/session_persistence.py` (sealed).
- `backend/services/wizard/admission_handoff.py` (sealed).
- `backend/services/wizard/agent_interface.py` (sealed).
- All CP-AIP-1..5 modules — untouched.

---

## 6 · Owner content anchors banked

- **§16.1 (c) CLEAN receipt** verbatim applied (2026-02-23T05:00:00Z): extend existing state machine with additive `objective` variant on `WizardCommitState_v0.variant` Literal · sibling machine explicitly rejected per §1.2. This seal lands the sibling CONTRACT (`wizard_objective_commit_state_v0.py`); the sealed `WizardCommitState_v0` is NOT edited.
- **§16.2 baseline-tier contents** PENDING-OWNER-CONFIRMATION per owner working default 2026-02-23T04:15Z: v1.0 proposed set as-is (5-tuple encoded verbatim).
- **§15 P234** verbatim: 'The planner must never accept a hand-authored Outcome once the wizard exists' — the wizard MUST land BEFORE the planner (CP-AIP-7).

---

## 7 · SPEC-CONFLICT log this slice

**NONE.**

---

## 8 · Standing bounds

Unchanged. R-106 P3-CLOSED + P4-(a-d-i) + CP-CENSUS + CP-AIP-1..6 SEALED-A · §6.8 plan-authority report-and-continue.

Additive-only §3.8 · monotonic-up ratchet floor 6302 · no sealed carrier touched · no refactoring · terminal `pytest` only · `testing_agent` BANNED · Six Standing Bans in force.

**BRIEF REPORT-AND-CONTINUE DUE post-Commit-C fixup** per owner cadence directive verbatim; then IMMEDIATELY proceed to CP-AIP-7 (no halt · no GO wait).
