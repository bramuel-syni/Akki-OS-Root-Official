# CP-AIP-2-DEDUP-CONDITION-MAP · Comprehensive Seal Receipt

**Seal timestamp:** 2026-02-23T06:15:00Z  
**Ledger anchor:** EXECUTION_ORDER.md Item 5.2 · CP-AIP-2 (Dedup as augmentation · AIP v1.0 §4.5 + §4.6 (b))  
**Owner authorization:** GO at Item 4 checkpoint (2026-02-23) verbatim: "continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals".

**Ledger check** — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-2-DEDUP-CONDITION-MAP and nothing else.

---

## 1 · Scope

Additive dedup-instance provenance carriers per AIP v1.0 §4.5 + §4.6 (b) via §1.2 modality-extension composing:
- CP-M6-2-1 sealed `InstanceConditionMap` schema + constructor + gate helper.
- CP-AIP-1 sealed `IngestionSegmentProvenance_v1` as `base_provenance`.

Closes CP-AIP-1's deferred §4.6 (b) branch per owner GO reminder 1 (b) verbatim.

### New additive modules under `backend/services/audio_plane_v1/`:

- **`dedup_instance_provenance_v1.py`** (~110 lines):
  - `DedupInstanceProvenanceIncomplete` refusal class.
  - `RobustnessStratumTag_v1` (frozen dataclass · §4.5 "zero acquisition cost" verbatim provenance · refuses False).
  - `DedupInstanceProvenance_v1` (frozen dataclass · wraps CP-AIP-1 `base_provenance` + sealed `instance_condition_map` + Literal `dedup_role` + `robustness_stratum` · §1.5 __post_init__ gates).

- **`dedup_capture_v1.py`** (~95 lines):
  - `DedupInstanceProvenanceRefused` refusal class.
  - `compose_dedup_instance_provenance(...)` composer invoking sealed `construct_instance_condition_map` (CP-M6-2-1).
  - `assert_dedup_provenance_meets_section_4_6_b(item)` gate callable invoking sealed `dedup_item_has_instance_condition_map(item)` (CP-M6-2-1).

### RED-first invariant pins (10 · `test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py`):

| # | Pin name | Spec anchor |
|---|---|---|
| 1 | `test_dedup_instance_provenance_requires_non_empty_variants` | §4.5 variants non-empty (via sealed VariantsEmptyError) |
| 2 | `test_dedup_instance_provenance_dedup_role_is_canonical_or_variant` | §4.5 canonical-vs-variant Literal |
| 3 | `test_robustness_stratum_tag_carries_zero_acquisition_cost_flag` | §4.5 zero-acquisition-cost provenance |
| 4 | `test_assert_dedup_provenance_gate_refuses_missing_instance_condition_map` | §4.6 (b) verbatim |
| 5 | `test_assert_dedup_provenance_gate_accepts_wellformed_item` | §4.6 (b) accept path |
| 6 | `test_dedup_capture_composes_sealed_instance_condition_map_constructor` | §1.2 · uses sealed constructor |
| 7 | `test_new_modules_do_not_redeclare_sealed_dedup_carriers` | §1.2 no-parallel-machinery |
| 8 | `test_assert_gate_uses_sealed_dedup_item_helper` | §1.2 · uses sealed gate helper |
| 9 | `test_dedup_instance_provenance_composes_cp_aip_1_ingestion_provenance` | CP-AIP-1 composition via base_provenance |
| 10 | `test_new_modules_cite_section_4_5_and_ledger_check_anchor` | Anti-drift §3 + §5 |

---

## 2 · Drill receipts (all under `phase0/drill_receipts_cp_aip_2_dedup_condition_map/` in the CODE repo)

- **RED_pre_20260223T055500Z.log** · 10 failed / 0 passed in 0.71s · authentic ModuleNotFoundError for missing NEW modules.
- **GREEN_post_20260223T060000Z.log** · 9 passed / 1 failed (dedup_role Literal alias string issue).
- **GREEN_post_20260223T060200Z.log** · 10 passed / 0 failed in 0.71s (Literal inlined in dataclass field).
- **sweep_A_20260223T060500Z.log** · **6260 passed / 1 skipped / 0 failed / 520 warnings / 192.17s** (BASELINE_GUARD=1 PYTHONHASHSEED=0).
- **sweep_B_20260223T061000Z.log** · **6260 passed / 1 skipped / 0 failed / 520 warnings / 191.73s**.

**Double-green byte-identical stripped_sha256:** `b018e5d06851a5d1612a12c219e94a8f7990d82ac6dbcad9528d06f5d4fbaed8` IDENTICAL both sweeps.

---

## 3 · Ratchet

- `passed_floor: 6244 → 6254` (+10 canonical measured)
- `counts_at_baseline.passed: 6244 → 6254`
- `ratchet_history` +1 entry (ensure_ascii=False + indent=2 per BL #11 + BL #7)
- baseline_failures.json sha256 post-bump: `73f87115f9a78e94fd16544d07a81e54e7a68941021005acb466df49a8f708b4`

Above-floor delta: 6260 − 6254 = 6 (same as CP-AIP-1 sweep — 3 pod_shell mirror-drift tests still passing above baseline_failures list + 3 additional pre-existing above-floor tests).

---

## 4 · Doctrine binding

- **§1.2 modality-extension-not-parallel** — new modules COMPOSE sealed `InstanceConditionMap` + `InstanceConditionVariant` + `construct_instance_condition_map` + `dedup_item_has_instance_condition_map` + `IngestionSegmentProvenance_v1` via imports. Negative-scan pin 7 enforces.
- **§1.5 unrepresentable-not-policed** — `DedupInstanceProvenance_v1.instance_condition_map` typed non-Optional; `RobustnessStratumTag_v1.__post_init__` refuses `zero_acquisition_cost=False` structurally.
- **§4.6 (b) closed** — CP-AIP-1 deferred branch now landed as gate callable using sealed helper.
- **Anti-drift guards** — every pin cites its §4.5 or §4.6 or §1.2 anchor; module docstrings carry `§4.5`, `§4.6`, and ledger-check anchor.

---

## 5 · SPEC-CONFLICT log

**NONE this slice.**

---

## 6 · What was NOT done (in-scope for later CPs)

- Wiring dedup path (sealed `dedup_path.py`) to *populate* `DedupInstanceProvenance_v1` from actual occurrence-index output — this is a downstream integration slice; CP-AIP-2 lands the schema + composer + gate only.
- CP-AIP-3 · Character Register (§6 · custody harness · HARD GATE per owner reminder 4 · INTERIM REPORT DUE post-seal).
- CP-AIP-4..10.

---

## 7 · Full 5-commit seal chain (SHAs post-landing)

To be filled in via state mini-bank commit post-fixup.

---

## 8 · Next

**Item 5.3 · CP-AIP-3-CHARACTER-REGISTER** opens next per owner sequencing directive.

**CP-AIP-3 is the HARD GATE per owner GO reminder 4 verbatim:**
> "CP-AIP-3 is the hard gate: the custody invariant harness (four leakage paths — small stratum, idiolect marker, narrowing combination, exemplar storage — all must FAIL to store) must be GREEN before any CP-AIP-5 cluster is stored. If sequencing pressure ever tempts storing a cluster early, that is a HALT condition."

**Owner interim-report checkpoint due after CP-AIP-3 seals** — "that is the highest-risk boundary in the whole plane".
