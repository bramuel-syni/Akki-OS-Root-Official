# CHUNK 1 · Task C · Cross-Repo Overlap Analysis

**Session:** 2026-09-18 · Post CP-M11-GATE-RELEASE Commit-C-supplement (`d7dc76f9`).
**Governance:** ingest + ground truth only.
**Owner ruling 1a:** file-level diff summary only (identical / A⊇B / diverged, with file counts + total LOC + last-modified commit date per path per repo). **No per-file unified diffs in Chunk 1.**
**Instruction respected:** *"Do NOT interpret which is 'better' yet — just measure."* — this note reports numbers and set-relations only, with zero recommendation.

## 1 · Method

1. Enumerate `backend/services/*` children per repo (git-tracked files + dir entries, `__pycache__` excluded).
2. For every service name appearing anywhere, produce a per-repo record: `file_count`, `total_loc` (line count summed across all git-tracked files in that service path), `last_commit_date` (`git log -1 --format=%aI -- backend/services/<name>`), file-name set, and per-file sha256.
3. Diff summary per service (over the set of repos where it exists) is one of:
   - **identical** = all repos have the same `{filename → sha256}` map (byte-equal file-set)
   - **A⊇B** = repo A's file-name-set is a strict superset of repo B's AND every file present in B has matching sha256 in A (i.e., B is exactly a subset of A byte-for-byte)
   - **diverged** = otherwise; annotated with `common-files=<count>` and whether commons are sha-identical across the repos
4. Analysis script: `/app/assessment_workspace/tools/chunk1_task_c_overlap.py` (throwaway per binding rule, under `tools/`).
5. Full machine-readable matrix: `/app/assessment_workspace/notes/chunk1_20260918/chunk1_task_c_matrix.json` (315,971 B).
6. Full detailed per-service text table: `/app/assessment_workspace/notes/chunk1_20260918/chunk1_task_c_details.txt` (446 lines).

**Scope of repos scanned (5, including anomaly):** `RMS-IQ-Core-2`, `Akki-OS-V1`, `Extraction-Akki`, `Akki-Executive-Core`, `Akki-Executive-Final`. Task B flagged `Akki-Executive-Final` as an anomaly (not in problem-statement 4). It is included below as an additional data point; treat its overlaps as anomaly-scope.

## 2 · Headline counts

| Metric | Count |
|---|---:|
| Total unique service names across all 5 repos (union of `backend/services/*`) | **159** |
| Services appearing in ≥ 2 repos (multi-repo) | **82** |
| Services appearing in exactly 1 repo (single-repo) | **77** |

## 3 · Multi-repo services · Cluster A ↔ Cluster A overlaps (RMS-IQ-Core-2 / Akki-OS-V1 / Extraction-Akki)

Cluster A (per Task B §7): the trio that share `BUILD_JOURNAL.md`, `docs/close_reports/`, `docs/audits/`, subdirectory-service pattern.

### 3.1 · Byte-identical across the trio (18 services)

The following services have `{filename → sha256}` byte-equal in RMS + OS + Extraction. Same file set, same content, same last-commit date. No modification since the shared checkpoint.

| Service | fc | total LOC | last-commit UTC (all 3) |
|---|---:|---:|---|
| `artifact_store` | 4 | 577 | 2026-07-14 |
| `census_dimensions` | 5 | 383 | 2026-07-10 |
| `checker` | 6 | 751 | 2026-07-07 |
| `data_source` | 3 | 220 | 2026-07-04 |
| `g1_defensibility` | 3 | 237 | 2026-07-04 |
| `layer_a` | 4 | 306 | 2026-07-04 |
| `layer_b` | 5 | 439 | 2026-07-04 |
| `layer_c` | 4 | 309 | 2026-07-04 |
| `master_admin` | 2 | 105 | 2026-07-04 |
| `multi_instance` | 3 | 358 | 2026-07-06 |
| `outer_gate` | 6 | 741 | 2026-07-06 |
| `solva_depth` | 3 | 205 | 2026-07-04 |
| `system_state.py` | 1 | 224 | 2026-07-04 |
| `transform_forms` | 3 | 206 | 2026-07-04 |
| `v1_harness` | 2 | 176 | 2026-07-04 |
| `v2_gate` | 4 | 316 | 2026-07-04 |
| `v3_harness` | 2 | 133 | 2026-07-04 |
| `use_data` (RMS+Extraction, 2 repos) | 4 | 358 | 2026-07-07 |
| `memory` (RMS+Extraction, 2 repos) | 2 | 219 | 2026-07-04 |
| `team` (RMS+Extraction, 2 repos) | 3 | 236 | 2026-07-04 |

### 3.2 · Extraction-Akki strict supersets of RMS-IQ-Core-2 / Akki-OS-V1 (Cluster A superset chain)

For these services, `Extraction-Akki` contains **every** file present in the other Cluster A repo(s) with byte-identical sha256, PLUS additional files. Cluster A siblings did not modify the shared subset. Fits an "Extraction extends the shared base" pattern.

| Service | RMS fc/loc | OS fc/loc | Extraction fc/loc | Superset relation | Common-files sha-identical? |
|---|---|---|---|---|---|
| `connect` | 5 / 519 · last 2026-07-04 | (absent) | 8 / 1,036 · last 2026-08-26 | `Extraction⊇RMS` | Yes |
| `critic_pass` | (absent) | 7 / 626 · last 2026-07-14 | 15 / 1,588 · last 2026-08-26 | `Extraction⊇OS` | Yes |
| `mtafiti` | 12 / 1,110 · last 2026-07-14 | 12 / 1,110 · last 2026-07-14 | 22 / 2,247 · last 2026-08-26 | `Extraction⊇OS`; `Extraction⊇RMS` | Yes |
| `opportunity_briefs` | 9 / 909 · last 2026-07-10 | 9 / 909 · last 2026-07-10 | 12 / 1,220 · last 2026-08-26 | `Extraction⊇OS`; `Extraction⊇RMS` | Yes |
| `perception` | 30 / 3,097 · last 2026-07-14 | 30 / 3,097 · last 2026-07-14 | 44 / 4,867 · last 2026-08-26 | `Extraction⊇OS`; `Extraction⊇RMS` | Yes |
| `retention` | 2 / 77 · last 2026-07-04 | 2 / 77 · last 2026-07-04 | 4 / 213 · last 2026-08-26 | `Extraction⊇OS`; `Extraction⊇RMS` | Yes |
| `wizard` | 9 / 1,027 · last 2026-07-14 | 8 / 976 · last 2026-07-13 | 12 / 1,299 · last 2026-08-26 | `Extraction⊇OS`; `Extraction⊇RMS`; `RMS⊇OS` | Yes |

Note: `wizard` shows a chained superset: `Extraction ⊇ RMS ⊇ OS`. Cluster-A commonalities: Extraction's added files all landed on/around **2026-08-26** (a distinct authoring boundary).

### 3.3 · Reversed / lateral supersets

| Service | Relation | RMS fc/loc/last | OS fc/loc/last | Extraction fc/loc/last | Common sha-identical? |
|---|---|---|---|---|---|
| `service_1` | `Akki-OS-V1⊇RMS-IQ-Core-2` (Extraction present but not fully-subset — diverged) | 26 / 2,928 · 2026-07-13 | 27 / 3,004 · 2026-07-13 | 27 / 3,092 · 2026-08-26 | No (common=25; some sha differ across Extraction vs the rest) |
| `targeta` | `Akki-OS-V1⊇Extraction`; `Akki-OS-V1⊇RMS-IQ-Core-2` | 6 / 465 · 2026-07-06 | 8 / 688 · 2026-07-14 | 6 / 465 · 2026-07-06 | Yes for the 6 common files |

`targeta` is the one clear case where **Akki-OS-V1 is a strict superset** (of the same byte-content base) — it has 2 extra files (mostly a `service_v1_1.py` extension) that neither RMS nor Extraction carries. This is the inverse of the general Extraction-superset pattern.

### 3.4 · Diverged (Cluster A, no clean superset relation)

Services with common file-names across 2+ Cluster-A repos but where the content differs (at least one common file has different sha256). File-name-set is not a clean subset either way.

| Service | Presence | Diff summary |
|---|---|---|
| `auth` | RMS+OS+Extraction | 3 repos · common=15 (sha-identical: False). RMS+Extraction both 16 files @ 1,736 LOC last 2026-08-01 (may be byte-equal duo); OS 15 files @ 1,491 LOC last 2026-07-08. |
| `compliance` | RMS+OS+Extraction | 3 repos · common=23 (sha-identical: False). RMS/Extraction 27 files 2,671 LOC last 2026-07-07; OS 24 files 2,341 LOC last 2026-07-07. |
| `economics` | RMS+OS+Extraction | Extraction⊇RMS relation logs common=1,118 (sha-identical: False). Multi-file service — heavy divergence. RMS 1,146 files/? LOC; Extraction 1,148 files/? LOC; last-commit varies. |
| `health` | RMS+OS+Extraction | common=2 (sha-identical: False). |
| `northena` | RMS+OS+Extraction | common=6 (sha-identical: False). |
| `registry` | RMS+OS+Extraction | common=4 (sha-identical: False). |
| `solva_v2` | RMS+OS+Extraction | common=5 (sha-identical: False). |

**These are the "materially different contents under same name" cases the problem statement warned about** for Cluster A.

## 4 · Multi-repo services · Cluster B ↔ Cluster B overlaps (Akki-Executive-Core / Akki-Executive-Final)

Cluster B repos (Executive-Core, Executive-Final) share **many** services. Executive-Final appears to be a slightly-trimmed variant of Executive-Core with roughly matching content. Anomaly disclosure: Executive-Final is not in the problem-statement 4.

### 4.1 · Byte-identical Cluster B pairs (identical file-set + content)

| Service | fc | total LOC (both repos) |
|---|---:|---:|
| `cohort` | 4 | 2,057 |
| `cohort_email.py` | 1 | 103 |
| `cohort_email_html.py` | 1 | 78 |
| `continue_chat.py` | 1 | 274 |
| `crypto` | 3 | 145 |
| `cycle_lifecycle.py` | 1 | 1,003 |
| `cycle_permissions.py` | 1 | 260 |
| `cycle_synthesis.py` | 1 | 1,251 |
| `first_login_password_set.py` | 1 | 132 |
| `job_queue.py` | 1 | 308 |
| `llm_streaming.py` | 1 | 128 |
| `metadata_signatures.py` | 1 | 91 |
| `open_questions` | 4 | 1,181 |
| `platform_kb.py` | 1 | 47 |
| `privacy_wall.py` | 1 | 156 |
| `rate_limit.py` | 1 | 71 |
| `rbac.py` | 1 | 120 |
| `security_headers.py` | 1 | 17 |
| `sentry_setup.py` | 1 | 22 |
| `session_timeout.py` | 1 | 69 |
| `solva_session_status.py` | 1 | 118 |
| `streaming` | 5 | 1,320 |
| `streaming_phases.py` | 1 | 71 |
| `stripe_webhook.py` | 1 | 227 |
| `tasks_initiatives` | 1 | 101 |
| `two_pass.py` | 1 | 245 |

### 4.2 · Cluster B diverged pairs

Filename overlap but different sha256. Same-name-different-content pattern.

| Service | Core fc/loc/last | Final fc/loc/last | Notes |
|---|---|---|---|
| `analysis_lifecycle.py` | 1 / 443 / 2026-07-04 | 1 / 153 / 2026-06-04 | different LOC → different content |
| `backfill_shield_v1.py` | 1 / 490 / 2026-06-23 | 1 / 490 / 2026-05-24 | same LOC different content or timestamp |
| `clamav_service.py` | 1 / 175 / 2026-06-19 | 1 / 175 / 2026-05-15 | same LOC different content or timestamp |
| `csrf.py` | 1 / 105 / 2026-06-21 | 1 / 105 / 2026-05-15 | same LOC different content or timestamp |
| `documents` | 6 / 1,842 / 2026-07-06 | 5 / 1,517 / 2026-05-15 | Core has 1 extra file |
| `ideas_engine` | 8 / 3,213 / 2026-06-25 | 8 / 3,072 / 2026-05-15 | same file count divergent content |
| `inbox_routing` | 11 / 1,911 / 2026-06-21 | 11 / 1,911 / 2026-05-15 | timestamp difference |
| `news_aggregator.py` | 1 / 258 / 2026-06-19 | 1 / 258 / 2026-05-15 | timestamp difference |
| `sandbox_generation.py` | 1 / 354 / 2026-06-23 | 1 / 354 / 2026-05-15 | timestamp difference |
| `signal_dedup.py` | 1 / 144 / 2026-06-19 | 1 / 144 / 2026-05-15 | timestamp difference |
| `solva_v2` (also in Cluster A) | 5 / … | 5 / … | see §5 cross-cluster |
| `storage_service.py` | 1 / 184 / 2026-06-19 | 1 / 184 / 2026-05-15 | timestamp difference |
| `synisense` (also in all 5) | (see §5) | | cross-cluster |
| `tasks` | 4 / 1,067 / 2026-07-05 | 4 / 851 / 2026-05-15 | different LOC |
| `universal_search.py` | 1 / 167 / 2026-06-25 | 1 / 167 / 2026-05-15 | timestamp difference |
| `work_studio` | 2 / 1,092 / 2026-06-25 | 2 / 1,175 / 2026-05-15 | LOC differs |
| `work_studio_export.py` | 1 / 288 / 2026-06-25 | 1 / 288 / 2026-05-15 | timestamp only |
| `work_studio_overlay.py` | 1 / 273 / 2026-06-25 | 1 / 273 / 2026-05-15 | timestamp only |
| `workbook_analyzer` | 10 / 3,225 / 2026-06-25 | 10 / 3,203 / 2026-05-15 | LOC differs |

## 5 · Cross-cluster overlaps (services that appear in both Cluster A AND Cluster B)

These are the highest-signal overlaps for the "materially different contents under same name" class.

| Service | Presence (5 repos) | RMS | OS | Extraction | Exec-Core | Exec-Final | Diff summary |
|---|---|---|---|---|---|---|---|
| `chat` | Extraction + Core + Final | (absent) | (absent) | 2 files / 99 LOC / 2026-08-26 | 2 files / 308 LOC / 2026-06-23 | 2 files / 308 LOC / 2026-05-15 | diverged · common=1 (sha-identical: False) — Cluster A and Cluster B have different `chat.py` implementations |
| `solva` | Extraction + Final | (absent) | (absent) | 5 files / 663 LOC / 2026-08-26 | (absent) | 4 files / 508 LOC / 2026-05-15 | diverged · common=2 (sha-identical: False) |
| `solva_v2` | OS + Extraction + Core + Final | (absent) | 5 / 566 / 2026-07-14 | 5 / 566 / 2026-08-26 | 5 / 566 / 2026-06-25 | 5 / 566 / 2026-05-15 | diverged · common=5 (sha-identical: False) — same file names, different implementations across Cluster A vs B |
| **`synisense`** | **All 5 repos** | 9 / 2,067 / 2026-07-10 | 9 / 2,067 / 2026-07-10 | 9 / 2,067 / 2026-07-10 | 10 / 1,795 / 2026-06-25 | 10 / 1,795 / 2026-05-15 | diverged · common=10 (sha-identical: False). The trio A shares byte-equal 9 files at 2,067 LOC; Cluster B pair shares byte-equal 10 files at 1,795 LOC. **Two distinct byte-equal families under the same service name** — the strongest "same-name-materially-different-contents" case in the codebase. |

## 6 · Single-repo services (77 total · A "exists in X, missing elsewhere" list)

### 6.1 · Extraction-Akki only (63 services)

`agent_containment`, `approvals`, `attribute_stream_bundle`, `audio_plane_v1` (26 files / 5,633 LOC), `audio_poc` (11 files / 1,095 LOC), `audit_trail`, `baseline_line`, `business_continuity`, `campaign_infra`, `canonical_projection`, `capability_registry.py`, `census_canon`, `census_engine`, `chokepoint` (11 files / 1,657 LOC), `compute_estate`, `compute_seam`, `connect_estate`, `contract_shells`, `cost_ledger`, `credentials_paste`, `d12_poc`, `dap` (18 files / 2,097 LOC), `data_suite_v2`, `de_identify`, `declaration`, `doc0_attributes` (20 files / 723 LOC), `estate_keys`, `evidence_register`, `governance`, `governance_plane`, `grey_mirror`, `handoff`, `ip_allowlist`, `journey_assistant`, `lowered_standard`, `model_admission`, `model_recheck`, `model_registry`, `n_series`, `orchestrator_resilience`, `output_verified_seal`, **`platform_control_plane` (36 files / 4,855 LOC · largest single-repo service in Extraction · the M9 body)**, `registry_facts`, `release_gate`, `reliable_time_source`, `resource_registry`, `response_sanitizer`, `rights_quarantine`, `rules_service`, `rulings`, `secret_hygiene`, `serving_floor`, `shield_train`, `skill_files`, `source_plane`, `trace`, `training`, `training_runner`, `w_registry_full_build`, **`watch` (21 files / 3,450 LOC · Watch engine body)**, `whitepapers`, `work_supervisor`, `wpw`.

### 6.2 · Akki-Executive-Core only (9 services)

`analyze_workspace`, `deck_generation_jobs.py`, `deck_lineage.py`, `deck_regenerate.py`, `deck_retrieval.py`, `module_labels.py`, `monitor` (5 files / 2,231 LOC), `owner_digest.py`, `solva_voice_audit` (24 files / 4,315 LOC).

### 6.3 · Akki-OS-V1 only (5 services)

`far_endpoint` (4 files / 342 LOC), `generated_gates` (16 files / 1,953 LOC), `partitions` (2 files / 331 LOC), `registry_context` (5 files / 222 LOC), `sequencing_harness` (7 files / 426 LOC).

### 6.4 · RMS-IQ-Core-2 only

**Zero** — every service present in `RMS-IQ-Core-2/backend/services/` also appears in at least one other repo. This is a finding: RMS-IQ-Core-2 has no unique service-name inventory of its own within `backend/services/`.

### 6.5 · Akki-Executive-Final only

**Zero** — every service in `Akki-Executive-Final/backend/services/` also appears in `Akki-Executive-Core`. Executive-Final appears to be a subset of Executive-Core (with content divergences per §4.2).

## 7 · Overlap-heat summary (measured only, no interpretation)

Rows aggregate the numeric data above with no interpretation of "which repo is better".

| Repo | services (all in backend/services/) | services byte-identical with ≥1 other repo | services diverged from ≥1 other repo | services unique to this repo |
|---|---:|---:|---:|---:|
| `RMS-IQ-Core-2` | 35 | 21 (all with A trio-byte-equals plus 2-repo shared pairs) | 14 (auth, compliance, economics, health, mtafiti, northena, opportunity_briefs, perception, registry, retention, service_1, solva_v2, targeta, wizard) | 0 |
| `Akki-OS-V1` | 37 | 20 | 12 | 5 |
| `Extraction-Akki` | 102 | 22 (trio + Extraction-only-superset commons) | 17 | 63 |
| `Akki-Executive-Core` | 55 | 25 | 20 | 9 |
| `Akki-Executive-Final` | 47 | 25 | 20 | 0 |

## 8 · Method caveats (honest)

- Overlap analysis is at the granularity of `backend/services/<name>/` (directory) or `backend/services/<name>.py` (file). Deeper cross-repo dependencies (imports, callers) are NOT measured here.
- Diff summary is **file-name-set + per-file sha256** based. "identical" means every file at the same relative path has the same content. Whitespace/formatting-only differences count as divergence, not identity.
- `last_commit_date` is `git log -1 --format=%aI -- <path>` per repo. If a file was moved from another path, the touch date may reflect the move, not the original authorship.
- Renamed files (e.g., `service.py` → `service_v1_1.py`) appear as "one file added, one file removed" from the file-name-set perspective — this classification does not follow git rename detection.
- No line-level diff is included (owner ruling 1a). If a service is flagged "diverged", the substance of the divergence requires Chunk-2+ investigation.
- `Akki-Executive-Final` is included per Task B anomaly disclosure; its overlaps with the 4 canonical repos are reported alongside Executive-Core's, but treated as anomaly-scope data.

---

**Artefacts produced this session:**

- `/app/assessment_workspace/tools/chunk1_task_c_overlap.py` — analysis script (throwaway per binding rule)
- `/app/assessment_workspace/notes/chunk1_20260918/chunk1_task_c_matrix.json` — machine-readable full matrix (315,971 B)
- `/app/assessment_workspace/notes/chunk1_20260918/chunk1_task_c_details.txt` — text table (446 lines)
- This file (`chunk1_task_c_cross_repo_overlap.md`)

**Traditional canonical filename `notes/cross_repo_overlap.md`** kept-under-chunk1-subdir per owner post-Commit-C rule *"zero further state writes beyond CHUNK 1's own deliverable artifacts"* and to avoid clashing with any prior session's notes/.
