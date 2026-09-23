# CP-AIP-3-CHARACTER-REGISTER · Comprehensive Seal Receipt

**Seal timestamp:** 2026-02-23T06:35:00Z
**Ledger anchor:** EXECUTION_ORDER.md Item 5.3 · CP-AIP-3 (Character Register custody-of-identity boundary · AIP v1.0 §6)
**Owner authorization:** GO at Item 4 checkpoint (2026-02-23) verbatim: "continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals" · owner reminder 4 verbatim (HARD GATE) · owner interim-report checkpoint due post-Commit-C fixup.

**Ledger check** — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-3-CHARACTER-REGISTER and nothing else.

---

## 1 · Scope

The custody-of-identity boundary for the Character Register. This seal lands the CP-M6-3-3 write-path leakage-refusal boundary and the CP-M6-3-4 clustering-embedding-destruction helper as ADDITIVE modules composing sealed CP-M6-3-1 (`character_register.py`) schema and sealed CP-M6-3-2 (`leakage_path_harness.py`) harness contract.

The custody invariant harness is now GREEN: all four §6.3 P100 leakage paths (small stratum · idiolect marker · narrowing combination · exemplar storage) plus the §6.1 P093 organic exclusion FAIL to store on write-path exercise; the §6.2 P098 cond-4 clustering embedding destruction is structurally enforced (input list emptied in place; return type surfaces only centroids).

Every future change to the register code must keep this harness GREEN (§6.3 P100 verbatim "on every change to the register code"). This is enforced by the RED-first pin `test_run_leakage_path_harness_green_against_write_boundary`.

### New additive modules under `backend/services/audio_plane_v1/`:

- **`character_register_write_boundary_v1.py`** (~260 lines):
  - Five typed refusal sentinels — `SmallStratumRefused`, `IdiolectMarkerRefused`, `NarrowingCombinationRefused`, `ExemplarStorageRefused`, `NonLearnedRefused` — all subclass sealed `LeakageRefusalError` (CP-M6-3-2 harness contract).
  - `WriteBoundaryConfig_v1` governed-seam bundle (§16.2 platform minimum defaults · frozen dataclass · six carriers).
  - `write_character_entry(entry, *, config=DEFAULT_CONFIG) -> None` — fails-fast refusal boundary. §6.3 P100 unrepresentable-not-policed enforced BEFORE persistence.

- **`character_register_clustering_v1.py`** (~130 lines):
  - `assign_clusters_destroy_embeddings(*, utterance_embeddings, n_clusters, max_iterations=25) -> Tuple[Tuple[float, ...], ...]` — K-means-like assignment with structural embedding destruction (input list emptied in place per §6.2 P098 verbatim).

### RED-first invariant pins (12 · `test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py`):

| # | Pin name | Spec anchor |
|---|---|---|
| 1 | `test_write_boundary_refuses_small_stratum_with_typed_sentinel` | §6.2 P096 cond-2 · `SmallStratumRefused` |
| 2 | `test_write_boundary_refuses_idiolect_marker_with_typed_sentinel` | §6.4 P102 · own dedicated test (owner anchor (a)) · `IdiolectMarkerRefused` |
| 3 | `test_write_boundary_refuses_narrowing_combination_with_typed_sentinel` | §6.2 P097 cond-3 · `NarrowingCombinationRefused` |
| 4 | `test_write_boundary_refuses_exemplar_storage_with_typed_sentinel` | §6.2 P098 cond-4 (owner anchor (b)) · `ExemplarStorageRefused` |
| 5 | `test_write_boundary_refuses_non_learned_organic_with_typed_sentinel` | §6.1 P093 · `NonLearnedRefused` |
| 6 | `test_character_entry_schema_has_no_identity_leakage_fields` | §1.5 + §6.3 P100 · structural (no audio_bytes / no per_utterance_embedding / no speaker_id / no voiceprint / no speaker_embedding / no utterance_bytes / no raw_audio) |
| 7 | `test_clustering_destroys_embeddings_and_returns_only_centroids` | §6.2 P098 cond-4 (owner anchor (b)) · input list emptied in place + return type centroids-only |
| 8 | `test_conjunctive_conditions_learned_alone_is_not_sufficient` | §6.2 CONJUNCTIVE (owner anchor (a)) · learned+small-stratum still refused |
| 9 | `test_run_leakage_path_harness_green_against_write_boundary` | §6.3 P100 verbatim · full 4-scenario harness integration |
| 10 | `test_all_four_refusal_sentinels_subclass_sealed_leakage_refusal_error` | CP-M6-3-2 harness contract · classification discipline |
| 11 | `test_new_modules_do_not_redeclare_sealed_register_carriers` | §1.2 modality-extension-not-parallel · 13 forbidden symbols scanned |
| 12 | `test_new_modules_cite_section_6_and_ledger_check_anchor` | Anti-drift §3 + §5 · §6.3 P100 + §6.4 + §6.2 + P098 + ledger-check anchor scan |

---

## 2 · RED-first evidence

Pre-modules test run (RED sweep · 2026-02-23T06:28:00Z):

```
tests/invariants/test_cp_aip_3_character_register_custody_aip_v1_0_section_6.py
  FAILED test_write_boundary_refuses_small_stratum_with_typed_sentinel                  (ModuleNotFoundError right-reason)
  FAILED test_write_boundary_refuses_idiolect_marker_with_typed_sentinel                (ModuleNotFoundError right-reason)
  FAILED test_write_boundary_refuses_narrowing_combination_with_typed_sentinel          (ModuleNotFoundError right-reason)
  FAILED test_write_boundary_refuses_exemplar_storage_with_typed_sentinel               (ModuleNotFoundError right-reason)
  FAILED test_write_boundary_refuses_non_learned_organic_with_typed_sentinel            (ModuleNotFoundError right-reason)
  PASSED test_character_entry_schema_has_no_identity_leakage_fields                     (sealed carrier already guarantees structural impossibility · anti-regression pin)
  FAILED test_clustering_destroys_embeddings_and_returns_only_centroids                 (ModuleNotFoundError right-reason)
  FAILED test_conjunctive_conditions_learned_alone_is_not_sufficient                    (ModuleNotFoundError right-reason)
  FAILED test_run_leakage_path_harness_green_against_write_boundary                     (ModuleNotFoundError right-reason)
  FAILED test_all_four_refusal_sentinels_subclass_sealed_leakage_refusal_error          (ModuleNotFoundError right-reason)
  FAILED test_new_modules_do_not_redeclare_sealed_register_carriers                     (AssertionError · module missing right-reason)
  FAILED test_new_modules_cite_section_6_and_ledger_check_anchor                        (AssertionError · module missing right-reason)
========================= 11 failed, 1 passed in 0.79s =========================
```

Post-modules test run (GREEN sweep · 2026-02-23T06:29:30Z):

```
============================= 12 passed in 0.72s ==============================
```

All 11 RED pins flipped GREEN post-module authorship. The 1 anti-regression pin (`test_character_entry_schema_has_no_identity_leakage_fields`) stayed GREEN — it guards the sealed CP-M6-3-1 carrier against any future addition of identity-leakage fields.

---

## 3 · Pre-Commit-A double-green byte-identical sweep

Both sweeps ran under `BASELINE_GUARD=1 PYTHONHASHSEED=0`.

- **Sweep A:** `6272 passed / 1 skipped / 0 failed / 520 warnings in 191.38s`.
- **Sweep B:** `6272 passed / 1 skipped / 0 failed / 520 warnings in 191.97s`.
- **stripped_sha256 (both sweeps):** `920dc8131eb1bbf2512e04ea3ab2ea90f59f534a13ea4ace6b386c2fdb237999` — **IDENTICAL**.

Raw + stripped logs banked at `phase0/cp_aip_3_character_register_20260223/sweep_A.log` + `sweep_A.stripped` + `sweep_B.log` + `sweep_B.stripped`.

The passed count 6272 exceeds the ratchet floor 6266 by 6 (comprises tests outside the ratchet baseline manifest — expected). The three baseline_failures.json listed failures were flagged as expected. The CP10 harness receipt was refreshed pre-sweep (2026-09-23T05:18:27Z) so no wall-clock drift.

---

## 4 · Ratchet bump

- **Floor:** 6254 → 6266 (+12 canonical measured pins from CP-AIP-3).
- **baseline_failures.json sha256 pre-bump:** `73f87115f9a78e94fd16544d07a81e54e7a68941021005acb466df49a8f708b4` (post-CP-AIP-2).
- **baseline_failures.json sha256 post-bump:** `42910fa760d7f3ba84644b10f1f2d6f36daacd35aecfd95d19946ecbce29ccc0`.
- Written with `indent=2, ensure_ascii=False` per BL #7 + BL #11.
- `ratchet_history` entry appended with schema-complete fields (`at_utc` + `commit` (PENDING at authorship · filled post-Commit-A) + `cp` + `note` + `passed=6266`).
- `invariants_enforced_when_baseline_guard_1.passed_floor` advanced 6254 → 6266 in lock-step with `counts_at_baseline.passed` (per `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` invariant).

---

## 5 · Sealed carriers UNCHANGED (SO §3.8 additive-only)

- `backend/services/audio_plane_v1/character_register.py` (CP-M6-3-1 · sealed 2026-09-15 schema-only carriers).
- `backend/services/audio_plane_v1/leakage_path_harness.py` (CP-M6-3-2 · sealed 2026-09-15 harness framework · LEAKAGE_PATHS + LeakageRefusalError + HarnessAcceptedForbiddenError + HarnessRefusalTypeError + LeakageScenario + build_leakage_scenarios + run_leakage_path_harness).
- All CP-AIP-1 + CP-AIP-2 modules (`ingestion_provenance_v1.py` + `ingestion_capture_v1.py` + `dedup_instance_provenance_v1.py` + `dedup_capture_v1.py`) — untouched this seal.
- `services/rms_station_language_axis.py` + `services/instance_condition_map.py` + `services/dedup_path.py` + all prior sealed carriers — untouched.

---

## 6 · Owner content anchors banked

- **(a) §6.2 CONJUNCTIVE** — 'learned' alone is never sufficient; the idiolect rule (§6.4) must be its own test case. Enforced by PIN-2 (idiolect own dedicated test) + PIN-8 (conjunctive reinforcement · learned+small-stratum still refused).
- **(b) §6.2.4 embedding destruction + no-instance-voiceprint-field** — enforced by PIN-6 (schema shape guard · 7 forbidden field names) + PIN-7 (clustering destroys embeddings in-place · centroids-only return type).

---

## 7 · SPEC-CONFLICT log this slice

**NONE.**

---

## 8 · HARD GATE status

Per owner reminder 4 verbatim: *"CP-AIP-3 is the hard gate: the custody invariant harness (four leakage paths - small stratum, idiolect marker, narrowing combination, exemplar storage - all must FAIL to store) must be GREEN before any CP-AIP-5 cluster is stored."*

**Custody invariant harness: GREEN.** All four §6.3 P100 leakage paths refuse to store. §6.2 P098 cond-4 embedding destruction structurally enforced. Schema-shape guard structurally impossible per §1.5. CP-AIP-5 cluster storage is now UNBLOCKED by the HARD GATE (subject to owner GO for CP-AIP-4 first per sequencing).

**INTERIM REPORT DUE post-Commit-C fixup** per owner explicit direction: *"after CP-AIP-3 seals (custody harness green), send an interim report — that is the highest-risk boundary in the whole plane."* Main agent will HALT after this seal and await owner GO before opening CP-AIP-4.

---

## 9 · Standing bounds

Unchanged. R-102 productized-or-honest-gap · R-103 continuous · R-104 CORRECTED · R-105 partial-retirement · R-106 P3-CLOSED + P4-(a-d-i) + CP-CENSUS + CP-AIP-1 + CP-AIP-2 SEALED-A · §6.8 plan-authority report-and-continue.

Additive-only §3.8 · monotonic-up ratchet floor 6266 · no sealed carrier touched · no refactoring · terminal `pytest` only · `testing_agent` BANNED.
