# CP-AIP-5-CLUSTERING · Comprehensive Seal Receipt

**Seal timestamp:** 2026-02-23T07:20:00Z
**Ledger anchor:** EXECUTION_ORDER.md Item 5.5 · CP-AIP-5 (Character-Register Clustering acceptance boundary · AIP v1.0 §5.3)
**Owner authorization:** Owner cadence directive verbatim (2026-02-23 CP-AIP-4 GO): "run CP-AIP-5 → CP-AIP-10 sequentially; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>." + Owner reminder 4 verbatim (HARD GATE MET at CP-AIP-3 unblocks cluster storage) + Item-4 checkpoint GO.

**Ledger check** — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-5-CLUSTERING and nothing else.

---

## 1 · Scope

The character-register clustering acceptance boundary per AIP v1.0 §5.3. This seal lands TWO additive modules composing sealed CP-M6-5-1 `clustering.py` (`CandidateStratum` + `ClusteringBackend` Protocol + `cluster_character_register`), sealed CP-M6-5-2 `human_validation.py` (`HumanValidationVerdict` + `ValidatedStratum` + `bind_verdict_to_stratum` + `derive_task_id`), sealed CP-M6-5-3 `cluster_stability.py` (`assert_cluster_carries_no_human_name` + `assert_clustering_is_deterministic` + `assert_validated_stratum_preserves_candidate`), and sealed CP-AIP-3 `character_register_write_boundary_v1.py` (`WriteBoundaryConfig_v1` + `DEFAULT_CONFIG`) via §1.2 modality-extension. Zero sealed-carrier edit per SO §3.8.

Every §5.3 acceptance criterion is enforced by RED-first pytest invariants:

- **Acceptance criterion 1 (cluster-count invariant · N speakers minimum)** — `SmallClusterRefused` composes `WriteBoundaryConfig_v1.minimum_group_size` (default 5 per §16.2) via §1.2 import. No parallel N-config.
- **Acceptance criterion 3 (cluster-carries-only-description invariant)** — `StoredClusterCandidate_v1` structurally forbids 8 per-utterance-identifier field names per §6.2 cond-4 + §1.5.
- **Acceptance criterion 4 (naming-commissioned-not-inferred)** — `StoredClusterCandidate_v1.name=None` default + `NamedAtStorageRefused` on storage-time naming + `NamingCommissionReceiptMissing` on empty commissioning receipt.
- **§5.3 clause 2 verbatim end-to-end** — `commission_cluster_naming` invokes sealed CP-M6-5-2 `bind_verdict_to_stratum` verbatim (§1.2 modality-extension); storage boundary invokes sealed CP-M6-5-3 `assert_cluster_carries_no_human_name` gate at write time.

§6.3 P100 HARD GATE (custody invariant harness) MET at CP-AIP-3 unblocks storage per owner reminder 4 verbatim.

### New additive modules under `backend/services/audio_plane_v1/` (2 files):

- **`cluster_storage_boundary_v1.py`** (~150 lines):
  - `StoredClusterCandidate_v1` frozen dataclass with 4 description-shape carriers (`stratum_id` + `member_attribute_names` + `backend_name` + `name`). `name` defaults to `None`.
  - 3 typed refusal sentinels all subclassing sealed `ClusterStorageRefused`: `SmallClusterRefused` (§6.2 cond-2) · `NamedAtStorageRefused` (§5.3 clause 2 verbatim) · `ClusterHumanNameLeakAtStorageRefused` (§5.3 clause 2 end-to-end via sealed CP-M6-5-3).
  - `store_cluster_candidate(*, stratum, n_distinct_speakers, config=None, proposed_name_at_storage_time=None)` — fails-fast refusal boundary composing sealed CP-AIP-3 `DEFAULT_CONFIG` + invoking sealed CP-M6-5-3 `assert_cluster_carries_no_human_name`.
  - `HONEST_GAP_V1_POSTURE` Final marker citing §5.3 clause 2 verbatim.

- **`cluster_naming_commission_v1.py`** (~90 lines):
  - `NamingCommissionReceiptMissing` refusal class.
  - `commission_cluster_naming(*, stratum, proposed_name, commissioning_receipt_ref, verdict_type="accept")` — quoted-cost gate refuses on empty/whitespace-only `commissioning_receipt_ref` per §5.3 clause 2 + §1.4.
  - Invokes sealed CP-M6-5-2 `bind_verdict_to_stratum` + `derive_task_id` + `HumanValidationVerdict` verbatim (§1.2 modality-extension).
  - `HONEST_GAP_V1_POSTURE` Final marker citing §5.3 clause 2 verbatim.

### RED-first invariant pins (12 · `test_cp_aip_5_clustering_aip_v1_0_section_5_3.py`):

| # | Pin name | Spec anchor |
|---|---|---|
| 1 | `test_cluster_storage_boundary_refuses_below_minimum_group_size` | §5.3 acc.crit.1 + §6.2 cond-2 verbatim · `SmallClusterRefused` composing sealed `WriteBoundaryConfig_v1.minimum_group_size` |
| 2 | `test_cluster_storage_persists_with_name_null_until_naming_commission` | §5.3 acc.crit.4 + clause 2 verbatim · `StoredClusterCandidate_v1.name=None` default |
| 3 | `test_cluster_storage_payload_has_no_per_utterance_identifiers` | §5.3 acc.crit.3 + §6.2 cond-4 + §1.5 · structural scan of 8 forbidden field names |
| 4 | `test_cluster_naming_commission_binds_via_sealed_bind_helper` | §1.2 modality-extension · sealed CP-M6-5-2 `bind_verdict_to_stratum` invoked |
| 5 | `test_cluster_naming_commission_refuses_without_commissioning_receipt` | §5.3 clause 2 verbatim (quoted-cost) + §1.4 measure-don't-assert · `NamingCommissionReceiptMissing` |
| 6 | `test_cluster_storage_refuses_name_at_storage_time` | §5.3 clause 2 verbatim ('not what it is called') · `NamedAtStorageRefused` |
| 7 | `test_storage_boundary_composes_write_boundary_config_v1` | §1.2 · sealed CP-AIP-3 `WriteBoundaryConfig_v1` / `DEFAULT_CONFIG` imported |
| 8 | `test_storage_boundary_invokes_sealed_no_human_name_gate` | §1.2 · sealed CP-M6-5-3 `assert_cluster_carries_no_human_name` invoked |
| 9 | `test_new_modules_do_not_redeclare_sealed_clustering_symbols` | §1.2 modality-extension-not-parallel · 13 forbidden symbols scanned |
| 10 | `test_new_modules_carry_no_audio_byte_or_waveform_carriers` | §3.1 P038 + §6.3 P100 mirror · 4 forbidden tokens |
| 11 | `test_new_modules_do_not_assert_throughput_or_accuracy_figures` | §1.4 measure-don't-assert |
| 12 | `test_new_modules_cite_section_5_3_and_ledger_check_anchor` | Anti-drift §3 + §5 · §5.3 + ledger-check anchor scan |

---

## 2 · RED-first evidence

Pre-modules test run (RED sweep · 2026-02-23T07:10:00Z · before authoring the 2 additive modules):

```
tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py
  FAILED test_cluster_storage_boundary_refuses_below_minimum_group_size            (ModuleNotFoundError right-reason)
  FAILED test_cluster_storage_persists_with_name_null_until_naming_commission      (ModuleNotFoundError right-reason)
  FAILED test_cluster_storage_payload_has_no_per_utterance_identifiers             (ModuleNotFoundError right-reason)
  FAILED test_cluster_naming_commission_binds_via_sealed_bind_helper               (AssertionError · module missing right-reason)
  FAILED test_cluster_naming_commission_refuses_without_commissioning_receipt      (ModuleNotFoundError right-reason)
  FAILED test_cluster_storage_refuses_name_at_storage_time                         (ModuleNotFoundError right-reason)
  FAILED test_storage_boundary_composes_write_boundary_config_v1                   (AssertionError · module missing right-reason)
  FAILED test_storage_boundary_invokes_sealed_no_human_name_gate                   (AssertionError · module missing right-reason)
  FAILED test_new_modules_do_not_redeclare_sealed_clustering_symbols               (AssertionError · module missing right-reason)
  FAILED test_new_modules_carry_no_audio_byte_or_waveform_carriers                 (AssertionError · module missing right-reason)
  FAILED test_new_modules_do_not_assert_throughput_or_accuracy_figures             (AssertionError · module missing right-reason)
  FAILED test_new_modules_cite_section_5_3_and_ledger_check_anchor                 (AssertionError · module missing right-reason)
============================== 12 failed in 0.71s ==============================
```

Post-modules test run (GREEN sweep · 2026-02-23T07:15:00Z):

```
============================== 12 passed in 0.70s ==============================
```

All 12 RED pins flipped GREEN post-module authorship. Drill receipts banked at `backend/phase0/drill_receipts_cp_aip_5_clustering/` (RED_pre + GREEN_post + sweep_A + sweep_B).

---

## 3 · Pre-Commit-A double-green byte-identical sweep

Both sweeps ran under `BASELINE_GUARD=1 PYTHONHASHSEED=0`.

- **Sweep A:** `6298 passed / 1 skipped / 0 failed / 520 warnings in 185.28s` (real 3m7.778s).
- **Sweep B:** `6298 passed / 1 skipped / 0 failed / 520 warnings in 185.67s` (real 3m8.385s).
- **stripped_sha256 (both sweeps):** `310792f02204dd0522eba19623c091d8c3476d2875b5fea3e3c8d25581d2f1f2` — **IDENTICAL**.

Pre-Commit-A wire-up trips (fixed additively before sweep A):
1. **Vendored twin sync trip** — `test_vendored_tree_byte_identical_mirror_of_spine` failed on stale MANIFEST. Fixed via `prod_vendor_sync.py` (file_count 1048 → 1050 · structural_sha256 `90080bfb2582263f6ffc3f1fd13e63733d5e1b9b0f0a3d28b8e01245ed31899d`).
2. **ORCH_BOOT ratchet-only regen trip** — `test_orch_boot_anti_forget_manifest_matches_live_ratchet_and_sealed_heads` failed on stale ratchet. Fixed via append-only ORCH_BOOT.md regen block (ratchet.passed_floor 6280 → 6292 + baseline_failures.json sha256 to `5deb18b96c28659fed8e71f47abfef57d27177097164c772be1cc3f0080557cd` · heads_last_sealed UNCHANGED at CP-AIP-4).

Raw + stripped logs banked at `phase0/cp_aip_5_clustering_20260223/sweep_A.log` + `sweep_A.stripped` + `sweep_B.log` + `sweep_B.stripped`.

---

## 4 · Ratchet bump

- **Floor:** 6280 → 6292 (+12 canonical measured pins from CP-AIP-5).
- **baseline_failures.json sha256 pre-bump:** `678982b96d12fe19d55a001ca0fbf33abbda2cd869bd6bc5579f95959c64cab0` (post-CP-AIP-4).
- **baseline_failures.json sha256 post-bump:** `5deb18b96c28659fed8e71f47abfef57d27177097164c772be1cc3f0080557cd`.
- Written with `indent=2, ensure_ascii=False` per BL #7 + BL #11.
- `ratchet_history` entry appended with schema-complete fields (`at_utc` + `commit` (PENDING at authorship · filled post-Commit-A) + `cp` + `note` + `passed=6292`).
- `invariants_enforced_when_baseline_guard_1.passed_floor` advanced 6280 → 6292 in lock-step.

---

## 5 · Sealed carriers UNCHANGED (SO §3.8 additive-only)

- `backend/services/audio_plane_v1/clustering.py` (CP-M6-5-1 · sealed).
- `backend/services/audio_plane_v1/human_validation.py` (CP-M6-5-2 · sealed).
- `backend/services/audio_plane_v1/cluster_stability.py` (CP-M6-5-3 · sealed).
- `backend/services/audio_plane_v1/character_register_clustering_v1.py` (CP-AIP-3 · sealed).
- `backend/services/audio_plane_v1/character_register_write_boundary_v1.py` (CP-AIP-3 · sealed).
- `backend/services/audio_plane_v1/character_register.py` (CP-M6-3-1 · sealed).
- `backend/services/audio_plane_v1/leakage_path_harness.py` (CP-M6-3-2 · sealed).
- All CP-AIP-1 + CP-AIP-2 + CP-AIP-4 modules — untouched this seal.
- All perception/audio_codec/ modules (CP-AIP-4 seal) — untouched.

---

## 6 · Owner content anchors banked

- **HARD GATE MET at CP-AIP-3** — owner reminder 4 verbatim: 'the custody invariant harness (four leakage paths - small stratum, idiolect marker, narrowing combination, exemplar storage - all must FAIL to store) must be GREEN before any CP-AIP-5 cluster is stored.' CP-AIP-3 custody harness is GREEN; CP-AIP-5 cluster storage is UNBLOCKED per this reminder.
- **§16.2 cluster-naming-commissioned-internally** — owner working default 2026-02-23T04:15Z: naming validation commissioned internally. Enforced by `NamingCommissionReceiptMissing` quoted-cost gate.
- **HONEST_GAP_V1_POSTURE** — both new modules carry Final markers citing §5.3 clause 2 verbatim (naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost).

---

## 7 · SPEC-CONFLICT log this slice

**NONE.**

---

## 8 · Standing bounds

Unchanged. R-102 productized-or-honest-gap · R-103 continuous · R-104 CORRECTED · R-105 partial-retirement · R-106 P3-CLOSED + P4-(a-d-i) + CP-CENSUS + CP-AIP-1..4 SEALED-A + CP-AIP-5 SEALED-A · §6.8 plan-authority report-and-continue.

Additive-only §3.8 · monotonic-up ratchet floor 6292 · no sealed carrier touched · no refactoring · terminal `pytest` only · `testing_agent` BANNED · Six Standing Bans in force.
