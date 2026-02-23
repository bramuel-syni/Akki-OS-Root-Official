---
card_id: CP_AIP_5_CLUSTERING
title: AIP v1.0 §5.3 · Character-Register Clustering acceptance boundary · N-speakers gate + name-null-until-ceremony + no-per-utterance-payload + quoted-cost naming commission · Item 5.5 CP-AIP-5
ratified_at_utc: 2026-02-23T07:20:00Z
ratified_by: Owner cadence directive (2026-02-23 CP-AIP-4 GO verbatim) 'run CP-AIP-5 → CP-AIP-10 sequentially · brief report-and-continue after CP-AIP-6 seals · HALT after CP-AIP-10 for full plane completion report · immediate HALT on any SPEC-CONFLICT-<n>' + owner reminder 4 verbatim HARD GATE MET at CP-AIP-3 unblocking cluster storage + Item-4 checkpoint GO 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
card_sha256: 3c9ff53e65b407260bb2bda9d59e4a664d6bfc4a1daf93fec14b796b6b04fc09
milestone_status: OPEN (Item 5.5 CP-AIP-5 · in-flight for this seal · HARD GATE MET at CP-AIP-3 unblocks storage)
---

# CP-AIP-5-CLUSTERING · AIP v1.0 §5.3 Character-Register Clustering Acceptance Boundary

## OBJECTIVE

Land the additive cluster storage boundary + cluster naming commission wrapper per AIP v1.0 §5.3 as pure §1.2 modality-extension of sealed CP-M6-5-1 `clustering.py` (`CandidateStratum` + `ClusteringBackend` Protocol + `cluster_character_register`), sealed CP-M6-5-2 `human_validation.py` (`HumanValidationVerdict` + `ValidatedStratum` + `bind_verdict_to_stratum` + `derive_task_id`), sealed CP-M6-5-3 `cluster_stability.py` (`assert_cluster_carries_no_human_name` + `assert_clustering_is_deterministic` + `assert_validated_stratum_preserves_candidate`), and sealed CP-AIP-3 `character_register_write_boundary_v1.py` (`WriteBoundaryConfig_v1` + `DEFAULT_CONFIG`). Zero sealed-carrier edit per SO §3.8.

§5.3 acceptance criterion 1 (cluster-count invariant) is enforced by `SmallClusterRefused` composing `WriteBoundaryConfig_v1.minimum_group_size` (§6.2 cond-2 N speakers). §5.3 acceptance criterion 3 (cluster-carries-only-description invariant) is enforced structurally by the `StoredClusterCandidate_v1` frozen dataclass carrying only description-shape fields (no per-utterance-identifier fields). §5.3 acceptance criterion 4 (naming-commissioned-not-inferred invariant) is enforced by `StoredClusterCandidate_v1.name=None` default + `NamedAtStorageRefused` on storage-time naming + `NamingCommissionReceiptMissing` on empty commissioning receipt. The custody invariant tie-in (§6.3 P100) is preserved by structural embedding-destruction discipline inherited from CP-AIP-3 clustering + storage-time invocation of sealed CP-M6-5-3 `assert_cluster_carries_no_human_name` gate.

`canon_ref: AIP v1.0 §5.3 P089 verbatim (clause 1 + clause 2) + §6.2 P096..P098 (cond-2 N-speakers + cond-3 narrowing + cond-4 exemplar) + §6.3 P100 leakage-path invariant + §1.2 modality-extension + §1.4 measure-don't-assert + §1.5 unrepresentable-not-policed + §16.2 cluster-naming-commissioned-internally working default.`

Owner reminder 4 verbatim (2026-02-23 · HARD GATE): "CP-AIP-3 is the hard gate: the custody invariant harness (four leakage paths - small stratum, idiolect marker, narrowing combination, exemplar storage - all must FAIL to store) must be GREEN before any CP-AIP-5 cluster is stored." HARD GATE MET at CP-AIP-3; CP-AIP-5 cluster storage is UNBLOCKED per this reminder.

## MUST DO

1. **§5.3 acceptance criterion 1 · N-speakers gate composed via sealed CP-AIP-3 seam** — `store_cluster_candidate(..., n_distinct_speakers=k)` refuses with `SmallClusterRefused` when `k < WriteBoundaryConfig_v1.minimum_group_size` (governed platform default 5 per §16.2). §1.2 modality-extension via import of sealed `DEFAULT_CONFIG` / `WriteBoundaryConfig_v1`; no parallel N-config declared. Enforced by `test_cluster_storage_boundary_refuses_below_minimum_group_size`. `canon_ref: AIP §5.3 acceptance criterion 1 + §6.2 cond-2 verbatim + §16.2 platform default.`

2. **§5.3 acceptance criterion 4 · name=null until human ceremony** — `StoredClusterCandidate_v1.name` is `Optional[str] = None` by default; `store_cluster_candidate` returns with `name=None` on happy path. Enforced by `test_cluster_storage_persists_with_name_null_until_naming_commission`. `canon_ref: AIP §5.3 clause 2 verbatim + acceptance criterion 4.`

3. **§5.3 acceptance criterion 3 · no per-utterance identifiers in cluster payload** — `StoredClusterCandidate_v1` dataclass fields structurally forbid 8 per-utterance-identifier field names (`utterance_id` / `utterance_bytes` / `audio_bytes` / `raw_audio` / `per_utterance_embedding` / `speaker_id` / `speaker_embedding` / `voiceprint`) per §6.2 cond-4 + §1.5 unrepresentable-not-policed. Enforced by `test_cluster_storage_payload_has_no_per_utterance_identifiers`. `canon_ref: AIP §5.3 acceptance criterion 3 + §6.2 cond-4 + §1.5.`

4. **§5.3 clause 2 verbatim · naming ceremony via sealed bind_verdict_to_stratum** — `commission_cluster_naming(...)` invokes sealed CP-M6-5-2 `bind_verdict_to_stratum` (§1.2 modality-extension), not a parallel bind. Enforced by `test_cluster_naming_commission_binds_via_sealed_bind_helper`. `canon_ref: AIP §5.3 clause 2 verbatim + §1.2 + CP-M6-5-2 seal record.`

5. **§5.3 clause 2 · quoted-cost commissioning receipt gate** — `commission_cluster_naming` refuses with `NamingCommissionReceiptMissing` when `commissioning_receipt_ref` is empty / whitespace-only / falsy. §5.3 clause 2 verbatim ('commissioned like any other qualified work with quoted cost') + §1.4 measure-don't-assert. Enforced by `test_cluster_naming_commission_refuses_without_commissioning_receipt`. `canon_ref: AIP §5.3 clause 2 verbatim + §1.4 + §1.5.`

6. **§5.3 clause 2 verbatim · storage-time naming refused** — `store_cluster_candidate` refuses with `NamedAtStorageRefused` when a `proposed_name_at_storage_time` argument is passed. §5.3 clause 2 verbatim ('a cluster asserts that a distinct variant exists — not what it is called'). Enforced by `test_cluster_storage_refuses_name_at_storage_time`. `canon_ref: AIP §5.3 clause 2 verbatim.`

7. **§1.2 modality-extension · storage boundary composes CP-AIP-3 WriteBoundaryConfig_v1** — the storage boundary imports sealed `DEFAULT_CONFIG` / `WriteBoundaryConfig_v1` and cites `character_register_write_boundary_v1` in module docstring / imports. Enforced by `test_storage_boundary_composes_write_boundary_config_v1`. `canon_ref: AIP §1.2 + CP-AIP-3 seal record.`

8. **§1.2 modality-extension · storage boundary invokes sealed CP-M6-5-3 gate** — the storage boundary invokes sealed `assert_cluster_carries_no_human_name` at write time; not a parallel human-name scan. Enforced by `test_storage_boundary_invokes_sealed_no_human_name_gate`. `canon_ref: AIP §1.2 + CP-M6-5-3 seal record.`

9. **§1.2 no-redeclaration scan of 13 sealed symbols** — the NEW modules do NOT redeclare `CandidateStratum` / `ClusteringBackend` / `ValidatedStratum` / `HumanValidationVerdict` / `ClusterHumanNameLeakError` / `ClusteringNonDeterministicError` / `WriteBoundaryConfig_v1` / `LeakageRefusalError` / `cluster_character_register` / `bind_verdict_to_stratum` / `assert_cluster_carries_no_human_name` / `assert_clustering_is_deterministic` / `assign_clusters_destroy_embeddings`. Enforced by `test_new_modules_do_not_redeclare_sealed_clustering_symbols`. `canon_ref: AIP §1.2 verbatim + BL #4.`

10. **§3.1 P038 tokens-not-waveforms mirror on cluster storage payload** — the NEW modules carry NO audio-byte / waveform carriers (`audio_bytes` / `waveform` / `samples` / `raw_audio`). Enforced by `test_new_modules_carry_no_audio_byte_or_waveform_carriers`. `canon_ref: AIP §3.1 P038 + §6.3 P100 mirror.`

11. **§1.4 measure-don't-assert scan** — the NEW modules carry NO asserted throughput / accuracy figures. Enforced by `test_new_modules_do_not_assert_throughput_or_accuracy_figures`. `canon_ref: AIP §1.4 verbatim + owner directive verbatim.`

12. **12 RED-first pytest invariants** — RED_pre 12/12 failed → GREEN_post 12/12 passed. Each pin cites the exact §5.3 or §6.2 or §1 spec anchor it enforces. `canon_ref: SO §3 RED-first + Anti-drift standing guard §3.`

13. **Ratchet floor 6280 → 6292** — +12 canonical measured pins · `ensure_ascii=False, indent=2` per BL #11 + BL #7 · `ratchet_history` entry appended schema-complete (`passed=6292`). `invariants_enforced_when_baseline_guard_1.passed_floor` advanced in lock-step. `canon_ref: SO §3 no-silent-rebaselining + BL #6/7/11.`

14. **5-commit seal on dual branches + /app companion** — same shape as CP-AIP-1..4 seals. Terminal `pytest` only. `testing_agent` BANNED. `BASELINE_GUARD=1 PYTHONHASHSEED=0` double-green byte-identical `stripped_sha256`. `canon_ref: SO §3.3 5-Commit-Seal + Six Standing Bans.`

## MUST NOT

- Edit any sealed §5.3 carrier (`clustering.py` CP-M6-5-1 + `human_validation.py` CP-M6-5-2 + `cluster_stability.py` CP-M6-5-3), or any CP-AIP-3 module (`character_register_clustering_v1.py` + `character_register_write_boundary_v1.py`), or any prior CP-AIP-1/2/4 or CP-CENSUS carrier. `canon_ref: SO §3.8 additive-only.`

- Redeclare any of the 13 sealed clustering + validation + write-boundary symbols listed above. `canon_ref: AIP §1.2 verbatim + BL #4.`

- Introduce ANY audio-byte or waveform carriers (`audio_bytes` / `waveform` / `samples` / `raw_audio`) in the NEW modules. `canon_ref: AIP §3.1 P038 tokens-not-waveforms + §6.3 P100 mirror.`

- Store a cluster with a human-readable name at storage time. §5.3 clause 2 verbatim — the only path to a name is the commission wrapper post-storage. `canon_ref: AIP §5.3 clause 2 verbatim.`

- Commission cluster naming without a quoted-cost commissioning receipt reference. §5.3 clause 2 verbatim + §1.4 measure-don't-assert. `canon_ref: AIP §5.3 clause 2 verbatim + §1.4.`

- Persist per-utterance identifiers in the cluster storage payload. §5.3 acceptance criterion 3 + §6.2 cond-4 + §1.5 unrepresentable-not-policed. `canon_ref: AIP §5.3 + §6.2 cond-4 + §1.5.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-5-CLUSTERING and nothing else. `canon_ref: SO §7 guard 5 + Anti-drift standing guard §3 + §5.`

## EXIT

**12 RED-first invariants (RED_pre 12/12 failed · GREEN_post 12/12 passed · authored under this seal · continue verbatim GREEN post-Commit-A):**

- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_cluster_storage_boundary_refuses_below_minimum_group_size
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_cluster_storage_persists_with_name_null_until_naming_commission
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_cluster_storage_payload_has_no_per_utterance_identifiers
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_cluster_naming_commission_binds_via_sealed_bind_helper
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_cluster_naming_commission_refuses_without_commissioning_receipt
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_cluster_storage_refuses_name_at_storage_time
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_storage_boundary_composes_write_boundary_config_v1
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_storage_boundary_invokes_sealed_no_human_name_gate
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_new_modules_do_not_redeclare_sealed_clustering_symbols
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_new_modules_carry_no_audio_byte_or_waveform_carriers
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_new_modules_do_not_assert_throughput_or_accuracy_figures
- tests/invariants/test_cp_aip_5_clustering_aip_v1_0_section_5_3.py::test_new_modules_cite_section_5_3_and_ledger_check_anchor

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6280 → 6292 (+12 canonical measured)
- baseline_failures list unchanged
- both sweeps byte-identical `stripped_sha256 310792f02204dd0522eba19623c091d8c3476d2875b5fea3e3c8d25581d2f1f2` · 6298 passed / 1 skipped / 0 failed / 520 warnings both sweeps

## STOP

Stop at 5-commit seal landing. Continue immediately into CP-AIP-6-OBJECTIVE-WIZARD per owner cadence directive.

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §5.3 or §6.2 or §16.2, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report immediately (no continue). `canon_ref: STATE/EXECUTION_ORDER.md anti-drift §3 + owner cadence directive.`

## ANCHORS

**Spec anchors (AIP v1.0):**
- §5.3 P089 verbatim (V59 · clause 1 + clause 2): 'Unsupervised clustering over the character stream yields candidate strata. A cluster asserts that a distinct variant exists — not what it is called. Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost.'
- §5.3 acceptance criteria 1 (cluster-count · N speakers minimum per §6.2 cond-2) + 3 (cluster-carries-only-description · no per-utterance identifiers) + 4 (naming-commissioned-not-inferred · `name=null` until human ceremony).
- §6.2 P096 cond-2 (N distinct speakers minimum).
- §6.2 P097 cond-3 (narrowing combination refused at storage · inherited via CP-AIP-3 sealed write-boundary posture).
- §6.2 P098 cond-4 (exemplar / per-utterance carriers refused).
- §6.3 P100 (four-leakage-path harness · HARD GATE MET at CP-AIP-3).
- §15 P233 build sequence: 'Character register clustering (§5.3) — Requires 1–4.'
- §16.2 cluster naming validation — commissioned internally per owner working default 2026-02-23T04:15Z.
- §1.2 modality extension, not parallel machinery.
- §1.4 measure-don't-assert.
- §1.5 unrepresentable, not policed.

**Owner directives (verbatim):**
- Item 4 GO (2026-02-23): 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
- CP-AIP-4 GO + Cadence GO (2026-02-23 post-INTERIM REPORT): 'run CP-AIP-5 → CP-AIP-10 sequentially; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>.'
- Owner reminder 4 verbatim (HARD GATE): 'CP-AIP-3 is the hard gate: the custody invariant harness (four leakage paths - small stratum, idiolect marker, narrowing combination, exemplar storage - all must FAIL to store) must be GREEN before any CP-AIP-5 cluster is stored.' HARD GATE MET.

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/services/audio_plane_v1/clustering.py` (CP-M6-5-1 · `CandidateStratum` + `ClusteringBackend` Protocol + `cluster_character_register` seam).
- `backend/services/audio_plane_v1/human_validation.py` (CP-M6-5-2 · `HumanValidationVerdict` + `ValidatedStratum` + `bind_verdict_to_stratum` + `derive_task_id`).
- `backend/services/audio_plane_v1/cluster_stability.py` (CP-M6-5-3 · `assert_cluster_carries_no_human_name` + `assert_clustering_is_deterministic` + `assert_validated_stratum_preserves_candidate`).
- `backend/services/audio_plane_v1/character_register_clustering_v1.py` (CP-AIP-3 · `assign_clusters_destroy_embeddings`).
- `backend/services/audio_plane_v1/character_register_write_boundary_v1.py` (CP-AIP-3 · `WriteBoundaryConfig_v1` + `DEFAULT_CONFIG`).
- All CP-AIP-1 + CP-AIP-2 + CP-AIP-4 modules — untouched this seal.

**New additive modules landed by this seal (2 files · `backend/services/audio_plane_v1/`):**
- `cluster_storage_boundary_v1.py` (~150 lines · `StoredClusterCandidate_v1` frozen dataclass with 4 description-shape carriers + 3 typed refusal sentinels `SmallClusterRefused` / `NamedAtStorageRefused` / `ClusterHumanNameLeakAtStorageRefused` all subclassing sealed `ClusterStorageRefused` + `store_cluster_candidate` fails-fast boundary composing sealed CP-AIP-3 `WriteBoundaryConfig_v1.minimum_group_size` + invoking sealed CP-M6-5-3 `assert_cluster_carries_no_human_name` + `HONEST_GAP_V1_POSTURE` Final marker citing §5.3 clause 2 verbatim).
- `cluster_naming_commission_v1.py` (~90 lines · `NamingCommissionReceiptMissing` refusal + `commission_cluster_naming` gated callable · quoted-cost `commissioning_receipt_ref` gate · invokes sealed CP-M6-5-2 `bind_verdict_to_stratum` + `derive_task_id` + `HumanValidationVerdict` verbatim · `HONEST_GAP_V1_POSTURE` Final marker citing §5.3 clause 2 verbatim).

**Standing Orders anchors:**
- SO §3 RED-first · SO §3.3 5-Commit Seal · SO §3.8 additive-only · SO §4 product-language · SO §6.2 objective-card shape + hash-pin · SO §7 17-guard consolidated set · Six Standing Bans · STATE/EXECUTION_ORDER.md anti-drift §3 + §5.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-5-CLUSTERING and nothing else.
