# CHUNK 1 · Task B · Repo Inventory

**Session:** 2026-09-18 · Post CP-M11-GATE-RELEASE Commit-C-supplement (`d7dc76f9`).
**Governance:** ingest + ground truth only.
**Scope note:** Task B describes the 4 problem-statement repos + 1 anomaly repo (`Akki-Executive-Final`) found on disk that is NOT in the problem-statement list of 4.

---

## 1 · Pinned HEAD SHAs and default-branch table

Data captured via `git rev-parse HEAD`, `git branch --show-current`, `git symbolic-ref refs/remotes/origin/HEAD`, `git remote get-url origin`, `git rev-list --count HEAD`, `git log -1 --format=%aI`.

| Repo | Remote (git origin) | Checked-out branch | Default branch (origin/HEAD) | Pinned HEAD SHA (this session) | Total commits | Last commit UTC | Last commit summary (h · subj-first-60) |
|---|---|---|---|---|---|---|---|
| `RMS-IQ-Core-2` | `https://github.com/bramuel-syni/RMS-IQ-Core-2` | `main` | `main` | `ea5aa019521eee22ad4f8ea29efdfa2af357be3b` | 198 | 2026-08-01T08:10:07+00:00 | `ea5aa01 Auto-generated changes` |
| `Akki-OS-V1` | `https://github.com/bramuel-syni/Akki-OS-V1` | `main` | `main` | `8c361903cdd319bfdc0709de3f4392f5bfa3956b` | 167 | 2026-08-14T05:30:51+00:00 | `8c36190 Auto-generated changes` |
| `Extraction-Akki` | `https://github.com/bramuel-syni/Extraction-Akki` | **`programme/track-a`** | `main` | `4132e725774fb591d1d3c9f87428677ca29f14f2` | 551 | 2026-09-18T02:17:34+00:00 | `4132e72 CP-M11-GATE-RELEASE Commit-A · R-18 Part 8 gate-release · Watch contract schemas + AST-equivalent signature-as-guard tests + P-15 canon-vocab equality + D.6 canon_ref documentation check + c…` |
| `Akki-Executive-Core` | `https://github.com/bramuel-syni/Akki-Executive-Core` | `main` | `main` | `5844eee95d5faffea0dcab98bd4fe5e8d1419f32` | 929 | 2026-07-08T13:46:49+00:00 | `5844eee9 Auto-generated changes` |
| **`Akki-Executive-Final`** (anomaly · not in problem-statement 4) | `https://github.com/bramuel-syni/Akki-Executive-Final.git` | `main` | `main` | `bba80ab5d07e5b7ba300e13e26a8e1cf7a60869e` | 677 | 2026-06-06T15:11:13+00:00 | `bba80ab Auto-generated changes` |

**Anomalies reported exactly (binding rule):**
- **B1 · `Extraction-Akki` is checked out on non-default branch.** The default branch (per `origin/HEAD`) is `main`, but the working tree is on `programme/track-a`. The pinned HEAD `4132e725…` is on the `programme/track-a` branch, sealed as CP-M11-GATE-RELEASE Commit-A (banked in ORCH_BOOT.md and DECISIONS.md this-session). This deviates from the problem-statement default-branch guidance but reflects the mature working state; reported verbatim.
- **B2 · Fifth repo present on disk.** `/app/assessment_workspace/repos/Akki-Executive-Final/` exists with 677 commits, last-commit 2026-06-06. It is NOT one of the 4 repos named in the problem statement. Included in the table below the horizontal-rule anomaly marker to keep it distinguishable from the canonical 4. Not analysed in the same "problem-statement scope" as the 4; overlap analysis (Task C) will include it as an additional data point but flagged separately.

## 2 · File counts by extension (git-tracked only)

Counts via `git ls-files | awk` grouping by lowercase file extension.

| Repo | py | js | jsx | ts | tsx | other | total (tracked) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `RMS-IQ-Core-2` | 498 | 82 | 50 | 24 | 0 | 1,865 | 2,519 |
| `Akki-OS-V1` | 487 | 67 | 13 | 24 | 0 | 1,532 | 2,123 |
| `Extraction-Akki` | 1,320 | 96 | 74 | 24 | 0 | 2,126 | 3,640 |
| `Akki-Executive-Core` | 1,013 | 74 | 392 | 4 | 0 | 4,435 | 5,918 |
| `Akki-Executive-Final` | 816 | 61 | 381 | 0 | 0 | 6,509 | 7,767 |

**Observation:** `Extraction-Akki` is python-heaviest at 1,320 .py. `Akki-Executive-Core` / `Akki-Executive-Final` have massive `.jsx` counts (392 / 381) reflecting a substantially different frontend shape than `RMS-IQ-Core-2` / `Akki-OS-V1` / `Extraction-Akki`.

## 3 · Test file counts

Regex used against `git ls-files`: `(^|/)(test|tests)/|test_[^/]*\.py$|.*\.test\.[jt]sx?$|.*_test\.[jt]sx?$|.*\.spec\.[jt]sx?$`.

| Repo | test files (tracked) |
|---|---:|
| `RMS-IQ-Core-2` | 254 |
| `Akki-OS-V1` | 222 |
| `Extraction-Akki` | 709 |
| `Akki-Executive-Core` | 507 |
| `Akki-Executive-Final` | 438 |

## 4 · Top-level directory tree (depth 2 · git-tracked)

### 4.1 · `RMS-IQ-Core-2`
Top-level dirs: `backend/`, `docs/`, `frontend/`, `memory/`, `salvage/`, `test_reports/`, `tools/`
Top-level files: `BUILD_JOURNAL.md` · `Dockerfile` · `Makefile` · `README.md` · `docker-compose.yml` · `test_result.md`

### 4.2 · `Akki-OS-V1`
Top-level dirs: `backend/`, `docs/`, `frontend/`, `memory/`, `salvage/`, `test_reports/`, `tools/`
Top-level files: `BUILD_JOURNAL.md` · `Dockerfile` · `Makefile` · `README.md` · `docker-compose.yml`

### 4.3 · `Extraction-Akki`
Top-level dirs: `backend/`, `contracts/`, `docs/`, `frontend/`, `memory/`, `phase0/`, `pod_shell/`, `salvage/`, `test_reports/`, `tools/`
Top-level files: `BUILD_JOURNAL.md` · `Dockerfile` · `Makefile` · `README.md` · `TCB.yaml` · `docker-compose.yml` · `test_result.md`
**Note:** `contracts/` and `phase0/` are `Extraction-Akki`-only at top-level among the 4. `TCB.yaml` is `Extraction-Akki`-only.

### 4.4 · `Akki-Executive-Core`
Top-level dirs: `backend/`, `docs/`, `frontend/`, `memory/`, `nginx/`, `scripts/`, `sdk/`, `test_reports/`, `test_screenshots/`, `tests/`
Top-level files: `AUDIT_iter68.md` · `CHAT.docx` · `DEPLOY.md` · `Dockerfile.backend` · `Dockerfile.frontend` · `INTEGRATION.docx` · `Makefile` · `README.md` · `SOLVA.docx` · `afya.docx` · `auth_testing.md` · `backend_test.py` · `design_guidelines.json` · `docker-compose.prod.yml` · `docker-compose.yml` · `syni.docx` · `test_result.md`
**Note:** No `BUILD_JOURNAL.md` at root. Split Dockerfiles (`Dockerfile.backend` + `Dockerfile.frontend`) unlike the other 3.

### 4.5 · `Akki-Executive-Final` (anomaly repo)
Top-level dirs: `backend/`, `backup/`, `docs/`, `frontend/`, `memory/`, `nginx/`, `scripts/`, `test_reports/`, `test_screenshots/`, `tests/`
Top-level files: `AUDIT_iter68.md` · `CHAT.docx` · `DEPLOY.md` · `Dockerfile.backend` · `Dockerfile.frontend` · `INTEGRATION.docx` · `Makefile` · `README.md` · `SOLVA.docx` · `afya.docx` · `auth_testing.md` · `backend_test.py` · `design_guidelines.json` · `docker-compose.prod.yml` · `docker-compose.yml` · `syni.docx` · `test_result.md`
**Note:** Nearly identical top-level shape to `Akki-Executive-Core`, but has `backup/` in place of `sdk/`.

## 5 · `backend/services/` directory listings

### 5.1 · `RMS-IQ-Core-2/backend/services/` — 35 entries
`artifact_store`, `auth`, `census_dimensions`, `checker`, `compliance`, `connect`, `data_source`, `economics`, `g1_defensibility`, `health`, `layer_a`, `layer_b`, `layer_c`, `master_admin`, `memory`, `mtafiti`, `multi_instance`, `northena`, `opportunity_briefs`, `outer_gate`, `perception`, `registry`, `retention`, `service_1`, `solva_depth`, `synisense`, `system_state.py`, `targeta`, `team`, `transform_forms`, `use_data`, `v1_harness`, `v2_gate`, `v3_harness`, `wizard`

### 5.2 · `Akki-OS-V1/backend/services/` — 37 entries
`artifact_store`, `auth`, `census_dimensions`, `checker`, `compliance`, `critic_pass`, `data_source`, `economics`, `far_endpoint`, `g1_defensibility`, `generated_gates`, `health`, `layer_a`, `layer_b`, `layer_c`, `master_admin`, `mtafiti`, `multi_instance`, `northena`, `opportunity_briefs`, `outer_gate`, `partitions`, `perception`, `registry`, `registry_context`, `retention`, `sequencing_harness`, `service_1`, `solva_depth`, `synisense`, `system_state.py`, `targeta`, `transform_forms`, `v1_harness`, `v2_gate`, `v3_harness`, `wizard`

### 5.3 · `Extraction-Akki/backend/services/` — 102 entries
`agent_containment`, `approvals`, `artifact_store`, `attribute_stream_bundle`, `audio_plane_v1`, `audio_poc`, `audit_trail`, `auth`, `baseline_line`, `business_continuity`, `campaign_infra`, `canonical_projection`, `capability_registry.py`, `census_canon`, `census_dimensions`, `census_engine`, `chat`, `checker`, `chokepoint`, `compliance`, `compute_estate`, `compute_seam`, `connect`, `connect_estate`, `contract_shells`, `cost_ledger`, `credentials_paste`, `critic_pass`, `d12_poc`, `dap`, `data_source`, `data_suite_v2`, `de_identify`, `declaration`, `doc0_attributes`, `economics`, `estate_keys`, `evidence_register`, `g1_defensibility`, `governance`, `governance_plane`, `grey_mirror`, `handoff`, `health`, `ip_allowlist`, `journey_assistant`, `layer_a`, `layer_b`, `layer_c`, `lowered_standard`, `master_admin`, `memory`, `model_admission`, `model_recheck`, `model_registry`, `mtafiti`, `multi_instance`, `n_series`, `northena`, `opportunity_briefs`, `orchestrator_resilience`, `outer_gate`, `output_verified_seal`, `perception`, `platform_control_plane`, `registry`, `registry_facts`, `release_gate`, `reliable_time_source`, `resource_registry`, `response_sanitizer`, `retention`, `rights_quarantine`, `rules_service`, `rulings`, `secret_hygiene`, `service_1`, `serving_floor`, `shield_train`, `skill_files`, `solva`, `solva_depth`, `solva_v2`, `source_plane`, `synisense`, `system_state.py`, `targeta`, `team`, `trace`, `training`, `training_runner`, `transform_forms`, `use_data`, `v1_harness`, `v2_gate`, `v3_harness`, `w_registry_full_build`, `watch`, `whitepapers`, `wizard`, `work_supervisor`, `wpw`

### 5.4 · `Akki-Executive-Core/backend/services/` — 55 entries
`analysis_lifecycle.py`, `analyze_workspace`, `backfill_shield_v1.py`, `chat`, `clamav_service.py`, `cohort`, `cohort_email.py`, `cohort_email_html.py`, `continue_chat.py`, `crypto`, `csrf.py`, `cycle_lifecycle.py`, `cycle_permissions.py`, `cycle_synthesis.py`, `deck_generation_jobs.py`, `deck_lineage.py`, `deck_regenerate.py`, `deck_retrieval.py`, `documents`, `first_login_password_set.py`, `ideas_engine`, `inbox_routing`, `job_queue.py`, `llm_streaming.py`, `metadata_signatures.py`, `module_labels.py`, `monitor`, `news_aggregator.py`, `open_questions`, `owner_digest.py`, `platform_kb.py`, `privacy_wall.py`, `rate_limit.py`, `rbac.py`, `sandbox_generation.py`, `security_headers.py`, `sentry_setup.py`, `session_timeout.py`, `signal_dedup.py`, `solva_session_status.py`, `solva_v2`, `solva_voice_audit`, `storage_service.py`, `streaming`, `streaming_phases.py`, `stripe_webhook.py`, `synisense`, `tasks`, `tasks_initiatives`, `two_pass.py`, `universal_search.py`, `work_studio`, `work_studio_export.py`, `work_studio_overlay.py`, `workbook_analyzer`

### 5.5 · `Akki-Executive-Final/backend/services/` — 47 entries (anomaly repo)
`analysis_lifecycle.py`, `backfill_shield_v1.py`, `chat`, `clamav_service.py`, `cohort`, `cohort_email.py`, `cohort_email_html.py`, `continue_chat.py`, `crypto`, `csrf.py`, `cycle_lifecycle.py`, `cycle_permissions.py`, `cycle_synthesis.py`, `documents`, `first_login_password_set.py`, `ideas_engine`, `inbox_routing`, `job_queue.py`, `llm_streaming.py`, `metadata_signatures.py`, `news_aggregator.py`, `open_questions`, `platform_kb.py`, `privacy_wall.py`, `rate_limit.py`, `rbac.py`, `sandbox_generation.py`, `security_headers.py`, `sentry_setup.py`, `session_timeout.py`, `signal_dedup.py`, `solva`, `solva_session_status.py`, `solva_v2`, `storage_service.py`, `streaming`, `streaming_phases.py`, `stripe_webhook.py`, `synisense`, `tasks`, `tasks_initiatives`, `two_pass.py`, `universal_search.py`, `work_studio`, `work_studio_export.py`, `work_studio_overlay.py`, `workbook_analyzer`

**Note:** Both Executive repos mix `.py`-file services and directory-services in the same listing (`backend/services/` contains both loose .py files acting as services AND subdirectories). This differs from the RMS/OS/Extraction pattern where every service is a subdirectory (with one exception: `system_state.py` file appears at the top of `backend/services/` in each of RMS/OS/Extraction).

## 6 · Presence of BUILD_JOURNAL / docs/close_reports / docs/audits

Titles/dates only per problem-statement scope (treat as claims, not findings).

### 6.1 · `RMS-IQ-Core-2`
- **`BUILD_JOURNAL.md`** at repo root · 240,112 B · 2026-08-14
- **`docs/close_reports/`** present · 30 files listed (titles include `8_ext.md`, `9_2a.md`, `answer_fluency.md`, `artifact_store.md`, `census_dimensions.md`, `commercial_cut_2026_07_06.md`, `eab_1.md`, `fixture_refresh.md`, `g2_registry_maintenance.md`, `g3_operating_values_v1_1.md`, `housekeeping_preflight.md`, `machine_readable_registry.md`, `memory_service_stage_b_2026-07-31.md`, `multi_instance_capability.md`, `opportunity_briefs.md`, `p1_addendum_frontend_backend_url_blocker_fix_2026-07-30.md`, `p1_custody_closure_honest_startup.md`, `phase3_subcycle1_real_material_readiness_2026-08-01.md`, `phase3_subcycle2_memory_and_registry_2026-08-02.md`, `phase3_subcycle3_govern_module_2026-08-02.md`, `phase_4a_stage_b.md`, `phase_4b.md`, `phase_5_stage_b.md`, `phase_6_stage_b.md`, `phase_7_stage_b_1.md`, `phase_7_stage_b_2.md`, `phase_7_stage_b_3.md`, `phase_8_b_1.md`, `phase_8_b_2.md`, `phase_8_b_3.md`, …)
- **`docs/audits/`** present · titles include `deviation_audit_v1.md`, `enforcement_check_count_derivation_2026-07-30.md`, `engine_conformance_v1.md`, `g3_precondition/`, `g3_solva_conformance_v1.md`, `g4_mtafiti_conformance_v1.md`, `g4_service_1_v1_conformance_v1.md`, `g4_targeta_conformance_v1.md`, `g5a_conformance_v1.md`, `g5b_conformance_v1.md`, `g6_conformance_v1.md`, `northena_conformance_v1.md`, `solva_conformance_v1.md`, `substrate_drop_v1/`

### 6.2 · `Akki-OS-V1`
- **`BUILD_JOURNAL.md`** at repo root · 194,148 B · 2026-08-14
- **`docs/close_reports/`** present · overlaps heavily with `RMS-IQ-Core-2` list plus `change_order_2026_07_25.md`, `critic_pass.md`, `eab_2.md`, `eab_3.md`, `g_13.md`, `phase_8_b_4.md`, etc.
- **`docs/audits/`** present · overlaps with `RMS-IQ-Core-2` plus `lt2_forensic_correction_2026_07_24.md`, `lt2_sequencing_harness_provenance_d7_2026_07_24.md`, `product_doc_v3_1_untraceable_d7_2026_07_24.md`, `substrate_drop_v3_reconciliation_2026_07_24.md`

### 6.3 · `Extraction-Akki`
- **`BUILD_JOURNAL.md`** at repo root · 240,112 B · 2026-08-14
- **`docs/close_reports/`** present · listing appears identical or near-identical to `RMS-IQ-Core-2` (byte-check deferred to Task C).
- **`docs/audits/`** present · listing appears identical or near-identical to `RMS-IQ-Core-2` (byte-check deferred to Task C).

### 6.4 · `Akki-Executive-Core`
- **NO `BUILD_JOURNAL.md`** at repo root (finding).
- **`docs/`** present but with different subdir shape: `docs/RUNBOOKS/`, `docs/runbooks/`, `docs/sprints/` (both cases of RUNBOOKS coexist).
- **`docs/close_reports/`** — directory absent / empty (nothing listed).
- **`docs/audits/`** — directory absent / empty (nothing listed).

### 6.5 · `Akki-Executive-Final` (anomaly repo)
- **NO `BUILD_JOURNAL.md`** at repo root.
- **`docs/`** present · subdirs: `docs/RUNBOOKS/`, `docs/runbooks/`, `docs/sprints/` (mirrors `Akki-Executive-Core` shape).
- **`docs/close_reports/`** — directory absent / empty.
- **`docs/audits/`** — directory absent / empty.

## 7 · Summary observations (measured only, no interpretation)

- **Three-way clustering pattern.** Structural shape sorts the 5 repos into two clusters plus one:
  - **Cluster A (RMS/OS/Extraction):** `BUILD_JOURNAL.md` + `docs/close_reports/` + `docs/audits/` + subdirectory-service pattern in `backend/services/`. `RMS-IQ-Core-2` and `Extraction-Akki` share the exact same `BUILD_JOURNAL.md` size (240,112 B); `Akki-OS-V1` diverges at 194,148 B.
  - **Cluster B (Executive-Core / Executive-Final):** no `BUILD_JOURNAL.md`, empty `docs/close_reports/audits`, mixed `.py`-file + dir services, split Dockerfiles, more `.docx` at root, `nginx/` + `scripts/` at top-level, prevalent `.jsx` (~380+).
  - **Extraction-Akki singular:** carries `contracts/`, `phase0/`, `pod_shell/`, `TCB.yaml` at top-level that no other repo has; has 3× the `backend/services/` count of RMS/OS.
- **Extraction-Akki is the mature working repo.** `programme/track-a` HEAD `4132e725…` was landed 2026-09-18 as CP-M11-GATE-RELEASE Commit-A this-turn; 551 commits total; 709 test files. The other 4 repos have stale HEADs (last commit ranging 2026-06-06 to 2026-08-14) with "Auto-generated changes" as the last-commit subject.

---

**End of Task B.** Data feeds directly into Task C overlap analysis.
