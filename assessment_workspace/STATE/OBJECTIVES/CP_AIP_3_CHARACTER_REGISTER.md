---
card_id: CP_AIP_3_CHARACTER_REGISTER
title: AIP v1.0 §6 · Character Register custody-of-identity boundary · four-leakage-path harness GREEN · HARD GATE · Item 5.3 CP-AIP-3
ratified_at_utc: 2026-02-23T06:30:00Z
ratified_by: Owner GO at Item 4 checkpoint (2026-02-23 · verbatim "continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals") + owner reminder 4 verbatim HARD GATE + owner content anchors (a) §6.2 CONJUNCTIVE + (b) §6.2.4 embedding destruction.
card_sha256: 70a025ef1370a480322b099d6aeeeca8cb33e5697ad754251f0543e5b9bc9779
milestone_status: OPEN (Item 5.3 CP-AIP-3 · in-flight for this seal · HARD GATE · INTERIM REPORT DUE post-Commit-C fixup)
---

# CP-AIP-3-CHARACTER-REGISTER · AIP v1.0 §6 Custody-of-Identity Boundary · HARD GATE

## OBJECTIVE

Land the additive CP-M6-3-3 write-path leakage-refusal boundary + CP-M6-3-4 clustering-embedding-destruction helper as pure §1.2 modality-extension of sealed CP-M6-3-1 (`character_register.py`) schema and sealed CP-M6-3-2 (`leakage_path_harness.py`) harness contract. Zero sealed-carrier edit per SO §3.8.

Every §6.3 P100 leakage path (small stratum · idiolect marker · narrowing combination · exemplar storage) plus the §6.1 P093 organic exclusion MUST fail to store on write-path exercise, enforced by RED-first pytest invariants that run on every change to the register code (§6.3 P100 verbatim). §6.2 P098 cond-4 embedding destruction is structurally enforced (input list emptied in place; return type surfaces only centroids).

`canon_ref: AIP v1.0 §6.1 P092/P093 + §6.2 P095..P098 + §6.3 P100 + §6.4 P102 + §1.2 modality-extension + §1.5 unrepresentable-not-policed.`

Owner reminder 4 verbatim (2026-02-23 · HARD GATE): "CP-AIP-3 is the hard gate: the custody invariant harness (four leakage paths - small stratum, idiolect marker, narrowing combination, exemplar storage - all must FAIL to store) must be GREEN before any CP-AIP-5 cluster is stored. If sequencing pressure ever tempts storing a cluster early, that is a HALT condition."

## MUST DO

1. **§6.3 P100 four-leakage-path harness GREEN** — full four-scenario integration test (`test_run_leakage_path_harness_green_against_write_boundary`) runs sealed `run_leakage_path_harness(write_callable=write_character_entry)` and completes without raising `HarnessAcceptedForbiddenError` or `HarnessRefusalTypeError`. Every future change to the register code must keep this GREEN. `canon_ref: AIP §6.3 P100 verbatim.`

2. **Five typed refusal sentinels all subclass sealed LeakageRefusalError** — `SmallStratumRefused` (§6.2 cond-2) · `IdiolectMarkerRefused` (§6.4 · owner anchor (a) own test) · `NarrowingCombinationRefused` (§6.2 cond-3) · `ExemplarStorageRefused` (§6.2 cond-4 · owner anchor (b)) · `NonLearnedRefused` (§6.1 P093). Enforced by `test_all_four_refusal_sentinels_subclass_sealed_leakage_refusal_error`. `canon_ref: CP-M6-3-2 harness contract + AIP §6.1..§6.4.`

3. **§6.2 CONJUNCTIVE reinforcement (owner anchor (a))** — 'learned' alone is never sufficient. A dedicated pin (`test_conjunctive_conditions_learned_alone_is_not_sufficient`) proves an entry with `is_learned=True` but `n_distinct_speakers=1` STILL fails cond-2 and is refused. The idiolect rule (§6.4) has its own dedicated test case (`test_write_boundary_refuses_idiolect_marker_with_typed_sentinel`). `canon_ref: AIP §6.2 CONJUNCTIVE + §6.4 P102 + owner anchor (a) 2026-02-23.`

4. **§6.2.4 embedding-destruction + no-instance-voiceprint-field (owner anchor (b))** — `assign_clusters_destroy_embeddings` empties the input list in place after cluster assignment (structural evidence) and returns only centroid tuples (no per-utterance embeddings surface). Schema-shape guard confirms `CharacterEntry` structurally cannot represent an instance-level voiceprint (7 forbidden field names scanned: audio_bytes · per_utterance_embedding · speaker_id · voiceprint · speaker_embedding · utterance_bytes · raw_audio). Enforced by `test_clustering_destroys_embeddings_and_returns_only_centroids` + `test_character_entry_schema_has_no_identity_leakage_fields`. `canon_ref: AIP §6.2 P098 verbatim + §6.3 P100 + §1.5 + owner anchor (b) 2026-02-23.`

5. **§1.2 modality-extension via composition (no redeclaration)** — the NEW modules import sealed `CharacterEntry`, `construct_character_entry`, and `LeakageRefusalError` from CP-M6-3-1 + CP-M6-3-2; they do not redeclare any of those symbols or the sealed harness API. Enforced by `test_new_modules_do_not_redeclare_sealed_register_carriers` (13 forbidden symbols scanned). `canon_ref: AIP §1.2 modality-extension-not-parallel.`

6. **12 RED-first pytest invariants** — RED_pre 11/12 failed (1 anti-regression on sealed schema) → GREEN_post 12/12 passed. Each pin cites the exact §6 or §1 spec anchor it enforces. `canon_ref: SO §3 RED-first + Anti-drift standing guard §3.`

7. **Ratchet floor 6254 → 6266** — +12 canonical measured pins · `ensure_ascii=False, indent=2` per BL #11 + BL #7 · `ratchet_history` entry appended schema-complete (`passed=6266`). `invariants_enforced_when_baseline_guard_1.passed_floor` advanced in lock-step with `counts_at_baseline.passed`. `canon_ref: SO §3 no-silent-rebaselining + BL #6/7/11.`

8. **5-commit seal on dual branches + /app companion** — same shape as CP-AIP-1 + CP-AIP-2 seals. Terminal `pytest` only. BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical stripped_sha256. `canon_ref: SO §3.3 5-Commit-Seal + SO §7 guard 6.`

## MUST NOT

- Edit any sealed §6 carrier (`character_register.py` CP-M6-3-1 or `leakage_path_harness.py` CP-M6-3-2) or any prior CP-AIP-1/CP-AIP-2 or CP-CENSUS carrier. `canon_ref: SO §3.8 additive-only.`

- Redeclare sealed `CharacterEntry`, `CharacterRegister`, `LEAKAGE_PATHS`, `LeakageRefusalError`, `HarnessAcceptedForbiddenError`, `HarnessRefusalTypeError`, `LeakageScenario`, `build_leakage_scenarios`, or `run_leakage_path_harness` (parallel-machinery ban). `canon_ref: AIP §1.2 verbatim.`

- Add ANY field to `CharacterEntry` (structurally impossible per §1.5 — sealed frozen dataclass) or introduce any new schema field capable of representing an instance-level voiceprint. Owner anchor (b) verbatim. `canon_ref: AIP §6.3 P100 + §1.5.`

- Persist per-utterance embeddings after cluster assignment. `assign_clusters_destroy_embeddings` MUST empty its input list in place (§6.2 P098 verbatim 'destroyed after cluster assignment'). `canon_ref: AIP §6.2 P098 + owner anchor (b) 2026-02-23.`

- Accept ANY leakage path (small stratum / idiolect / narrowing / exemplar / organic) on the write-path. `canon_ref: AIP §6.3 P100 + §6.1 P093.`

- Quote unmeasured tok/s or accuracy figures in the seal receipt. `canon_ref: AIP §1.4 measure-don't-assert.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-3-CHARACTER-REGISTER and nothing else. `canon_ref: SO §7 guard 5.`

- Proceed to CP-AIP-4 without owner GO. HARD GATE per owner reminder 4 · INTERIM REPORT DUE post-Commit-C fixup. `canon_ref: Owner reminder 4 verbatim 2026-02-23.`

## EXIT

**12 RED-first invariants (RED_pre 11 failed + 1 anti-regression pass · GREEN_post 12/12 passed · authored under this seal · continue verbatim GREEN post-Commit-A):**

- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_write_boundary_refuses_small_stratum_with_typed_sentinel
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_write_boundary_refuses_idiolect_marker_with_typed_sentinel
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_write_boundary_refuses_narrowing_combination_with_typed_sentinel
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_write_boundary_refuses_exemplar_storage_with_typed_sentinel
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_write_boundary_refuses_non_learned_organic_with_typed_sentinel
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_character_entry_schema_has_no_identity_leakage_fields
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_clustering_destroys_embeddings_and_returns_only_centroids
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_conjunctive_conditions_learned_alone_is_not_sufficient
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_run_leakage_path_harness_green_against_write_boundary
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_all_four_refusal_sentinels_subclass_sealed_leakage_refusal_error
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_new_modules_do_not_redeclare_sealed_register_carriers
- tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py::test_new_modules_cite_section_6_and_ledger_check_anchor

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6254 → 6266 (+12 canonical measured)
- invariants_enforced_when_baseline_guard_1.passed_floor 6254 → 6266 (monotonic non-decreasing)
- baseline_failures list unchanged (still 3)
- Pre-Commit-A double-green byte-identical stripped_sha256 `920dc8131eb1bbf2512e04ea3ab2ea90f59f534a13ea4ace6b386c2fdb237999` IDENTICAL sweep_A/B both 6272 passed / 1 skipped / 0 failed / 520 warnings.

## STOP

**HALT after 5-commit seal landing.** Do NOT proceed into CP-AIP-4 in the same seal — CP-AIP-3 is the HARD GATE per owner reminder 4 and INTERIM REPORT is DUE to owner post-Commit-C fixup. The custody invariant harness must be GREEN (banked) before CP-AIP-5 clustering can store — CP-AIP-4 (codec service) still requires distinct owner GO post-report.

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §6, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report. `canon_ref: STATE/EXECUTION_ORDER.md anti-drift §3.`

## ANCHORS

**Spec anchors (AIP v1.0):**
- §6.1 P092 (organic characteristics · biometric · never registered).
- §6.1 P093 (learned characteristics · group properties · only learned may be registered).
- §6.2 P095..P098 (four conjunctive conditions · acquired-not-anatomical · shared · non-reconstructive-in-combination · description-not-exemplar).
- §6.3 P100 verbatim (four-leakage-path invariant · schema cannot represent voiceprint · unrepresentable-not-policed · on every change).
- §6.4 P102 verbatim (idiolect exclusion · learned-but-individuating · fails cond-2 or cond-3).
- §1.2 modality-extension not parallel plane.
- §1.5 unrepresentable, not policed.
- §16.2 governed seam · platform minimum-group-size.

**Owner directives (verbatim):**
- Item 4 GO (2026-02-23): 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
- Owner reminder 4 verbatim (HARD GATE): 'CP-AIP-3 is the hard gate: the custody invariant harness (four leakage paths - small stratum, idiolect marker, narrowing combination, exemplar storage - all must FAIL to store) must be GREEN before any CP-AIP-5 cluster is stored. If sequencing pressure ever tempts storing a cluster early, that is a HALT condition.'
- Owner interim-report checkpoint: 'after CP-AIP-3 seals (custody harness green), send an interim report - that is the highest-risk boundary in the whole plane.'
- Owner content anchor (a): '§6.2 conditions are CONJUNCTIVE - learned alone is never sufficient; the idiolect rule (§6.4) must be its own test case.'
- Owner content anchor (b): '§6.2.4 - clustering embeddings destroyed after cluster assignment; provenance points to material never speaker identity; the write-path schema must have NO field capable of representing an instance-level voiceprint (§6.3 unrepresentable-not-policed).'

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/services/audio_plane_v1/character_register.py` (CP-M6-3-1 · schema-only frozen carriers · 166 lines · seven-field CharacterEntry with zero identity-leakage fields structurally · REGISTER_LAYER_VALUES frozenset · LayerInvalidError refusal · construct_character_entry + construct_character_register).
- `backend/services/audio_plane_v1/leakage_path_harness.py` (CP-M6-3-2 · harness framework · 247 lines · LEAKAGE_PATHS Final verbatim four-tuple · LeakageRefusalError base class · HarnessAcceptedForbiddenError · HarnessRefusalTypeError · LeakageScenario frozen dataclass · build_leakage_scenarios canonical four synthetic · run_leakage_path_harness driver).

**New additive modules landed by this seal:**
- `backend/services/audio_plane_v1/character_register_write_boundary_v1.py` (~260 lines · 5 typed refusal sentinels + WriteBoundaryConfig_v1 governed-seam bundle + write_character_entry fails-fast boundary).
- `backend/services/audio_plane_v1/character_register_clustering_v1.py` (~130 lines · assign_clusters_destroy_embeddings K-means-like with structural embedding destruction).

**Standing Orders anchors:**
- SO §3 RED-first · SO §3.3 5-Commit Seal · SO §3.8 additive-only · SO §4 product-language · SO §6.2 objective-card shape + hash-pin · SO §7 17-guard consolidated set · STATE/EXECUTION_ORDER.md anti-drift §3 + §5.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-3-CHARACTER-REGISTER and nothing else.
