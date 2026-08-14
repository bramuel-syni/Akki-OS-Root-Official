# Cross-Repo Overlap Analysis — Chunk 1

Scope: `backend/services/<name>/` directory names that appear in 2+ of the four
repos, plus services present in exactly one repo. All figures are measured
(file counts by `git ls-files`, LOC by line-count, SHA-256 content hashes,
per-path last-commit dates by `git log -1 --format=%cI -- <path>`).

**Do not read this file as ranking or scoring** — Chunk 3 will do the REUSE /
MODIFY / RE-POINT / BUILD / RETIRE assignment. Below is only measurement.

## 1. Presence matrix

| service | RMS-IQ-Core-2 (files) | Akki-OS-V1 (files) | Extraction-Akki (files) | Akki-Executive-Core (files) |
|---|---:|---:|---:|---:|
| `__init__.py` | 1 | 1 | 1 | 1 |
| `artifact_store` | 4 | 4 | 4 | — |
| `auth` | 16 | 15 | 16 | — |
| `census_dimensions` | 5 | 5 | 5 | — |
| `checker` | 6 | 6 | 6 | — |
| `compliance` | 24 | 23 | 24 | — |
| `connect` | 4 | — | 4 | — |
| `data_source` | 16 | 16 | 16 | — |
| `economics` | 1399 | 1118 | 1409 | — |
| `g1_defensibility` | 10 | 10 | 10 | — |
| `health` | 2 | 2 | 2 | — |
| `layer_a` | 9 | 9 | 9 | — |
| `layer_b` | 10 | 10 | 10 | — |
| `layer_c` | 3 | 3 | 3 | — |
| `master_admin` | 2 | 2 | 2 | — |
| `memory` | 12 | — | 12 | — |
| `mtafiti` | 12 | 12 | 12 | — |
| `multi_instance` | 3 | 3 | 3 | — |
| `northena` | 7 | 7 | 7 | — |
| `opportunity_briefs` | 9 | 9 | 9 | — |
| `outer_gate` | 4 | 4 | 4 | — |
| `perception` | 30 | 30 | 30 | — |
| `registry` | 5 | 4 | 5 | — |
| `retention` | 2 | 2 | 2 | — |
| `service_1` | 25 | 26 | 25 | — |
| `solva_depth` | 15 | 15 | 15 | — |
| `synisense` | 21 | 16 | 21 | 34 |
| `system_state.py` | 1 | 1 | 1 | — |
| `targeta` | 6 | 7 | 6 | — |
| `team` | 2 | — | 2 | — |
| `transform_forms` | 6 | 6 | 6 | — |
| `use_data` | 4 | — | 4 | — |
| `v1_harness` | 3 | 3 | 3 | — |
| `v2_gate` | 3 | 3 | 3 | — |
| `v3_harness` | 2 | 2 | 2 | — |
| `wizard` | 9 | 8 | 9 | — |

Only ONE service name (`synisense`) overlaps between the three "core" repos and
Akki-Executive-Core. All other engine-shaped services in Akki-Executive-Core
carry different names (see §4).

## 2. Delta per shared service — headline

Detail lives in `_raw_service_diff.md`. Notation:
- **IDENTICAL** = same file set AND every file byte-identical (SHA-256).
- **SUBSET_OF_ANCHOR** = anchor has every file this repo has (byte-identical), plus extras.
- **SUPERSET_OF_ANCHOR** = this repo has every anchor file (byte-identical) plus extras.
- **DIVERGED** = at least one same-named file has different content and/or path sets differ both ways.
- Anchor for each row = repo with the largest file count for that service.

### 2.1 Identical across all 3 "core" repos (RMS-IQ-Core-2 == Akki-OS-V1 == Extraction-Akki)
`artifact_store`, `census_dimensions`, `checker`, `data_source`, `g1_defensibility`,
`layer_a`, `layer_b`, `layer_c`, `master_admin`, `mtafiti`, `multi_instance`,
`northena`, `opportunity_briefs`, `outer_gate`, `perception`, `retention`,
`solva_depth`, `system_state.py`, `transform_forms`, `v1_harness`, `v2_gate`,
`v3_harness`.

**Measurement, not opinion.** In every one of the above, all three repos carry the
same file names AND the same SHA-256s AND the same last-commit date on the
service path.

### 2.2 Identical between RMS-IQ-Core-2 and Extraction-Akki, DIVERGED / SUBSET vs Akki-OS-V1
This pattern recurs strongly. It means Akki-OS-V1 is older / behind on these services.

| service | R vs E | R vs O | E vs O | Anchor | Notes |
|---|---|---|---|---|---|
| `auth` | IDENTICAL | DIVERGED (Akki-OS-V1 subset, 1 missing + 3 content-diff) | DIVERGED | RMS-IQ-Core-2 (16) | Akki-OS-V1 missing `demo_identity_seeder.py`; `engineer_key_grant.py`, `engineer_key_grant_service.py`, `user_store.py` differ. |
| `compliance` | IDENTICAL | DIVERGED (Akki-OS-V1: 1 missing + 2 content-diff) | DIVERGED | RMS-IQ-Core-2 (24) | Akki-OS-V1 missing `data_class_registry.v4.json`; `consequence_class.v0.json`, `deletion_ledger.py` differ. |
| `health` | IDENTICAL | DIVERGED (1 content-diff) | DIVERGED | RMS-IQ-Core-2 (2) | `parity_counter.py` differs in Akki-OS-V1. |
| `registry` | IDENTICAL | DIVERGED (Akki-OS-V1: 1 missing + 2 content-diff) | DIVERGED | RMS-IQ-Core-2 (5) | Akki-OS-V1 missing `sample_fixture_seeder.py`; `parser.py`, `validator.py` differ. |
| `wizard` | IDENTICAL | Akki-OS-V1 SUBSET (missing 1) | Akki-OS-V1 SUBSET (missing 1) | RMS-IQ-Core-2 (9) | Akki-OS-V1 missing `milestones.py`. |

### 2.3 Akki-OS-V1 is the anchor (largest) on two services
| service | Anchor | Delta |
|---|---|---|
| `service_1` | Akki-OS-V1 (26) | RMS-IQ-Core-2 and Extraction-Akki are subsets, missing `batch_quarantine.py`. All other files byte-identical. |
| `targeta` | Akki-OS-V1 (7) | RMS-IQ-Core-2 and Extraction-Akki are subsets, missing `gap_candidate_filer.py`. All other files byte-identical. |

### 2.4 `economics` — the largest divergence
| Repo | files | lines | last commit on path |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 1399 | 12,033 | 2026-08-01T04:13:23+00:00 |
| Akki-OS-V1 | 1118 | 9,776 | 2026-07-25T14:39:38+00:00 |
| Extraction-Akki | 1409 | 12,113 | 2026-08-01T20:02:51+00:00 |

Anchor: **Extraction-Akki** (1409 files).
- RMS-IQ-Core-2 vs Extraction-Akki: **SUBSET** (missing 10 files; all in the `tier_lock.v1387.json … tier_lock.v139x.json` range). All shared files byte-identical.
- Akki-OS-V1 vs Extraction-Akki: **DIVERGED** — missing 291 files (mostly `tier_lock.v11xx.json / v12xx.json / v13xx.json`) AND 380 files with same path but DIFFERENT CONTENT. So Akki-OS-V1's `economics` is not just older, it also has substantively different content for hundreds of shared file names — cannot be treated as a subset.

### 2.5 `synisense` — the multi-repo divergence
This is the one service present in ALL FOUR repos, and it is DIVERGED in every pairwise comparison.

| Repo | files | lines | last commit on path |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 21 | 2,928 | 2026-07-30T20:06:53+00:00 |
| Akki-OS-V1 | 16 | 2,362 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 21 | 2,928 | 2026-07-30T20:06:53+00:00 |
| **Akki-Executive-Core** | **34** | **6,304** | **2026-07-04T19:05:20+00:00** |

Anchor: **Akki-Executive-Core** (34 files).
- Executive-Core carries 24 files the other three don't have, e.g. `adapter.py`, `deck_signal_extraction.py`, `encryption.py`, `engine/derivation_scheduler.py`, plus a whole `engine/` subtree.
- The three "core" repos carry 11 files Executive-Core doesn't have (in `shield/`): `brief_prompt.v0.txt`, `brief_synthesizer.py`, `egress_firewall.py`, `fluency_prompt.v0.txt`, `fluency_synthesizer.py`, `perception_router.py`, and one more.
- Same-path content divergences exist on `__init__.py`, `config.py`, `shield/__init__.py`, `shield/llm_router.py`, `shield/tenant_entities.py`, and one more.

**Explicit finding**: "synisense in Akki-Executive-Core" and "synisense in the
three core repos" are structurally different implementations sharing only a
name. Any Chunk-3 assessment MUST diff both.

Between the three core repos, synisense is IDENTICAL between RMS-IQ-Core-2 and
Extraction-Akki, and Akki-OS-V1 is behind (SUBSET style — the differences are
files that exist in the newer two but not in Akki-OS-V1).

## 3. Services present in EXACTLY ONE repo

### 3.1 Present only in RMS-IQ-Core-2 or Extraction-Akki (not Akki-OS-V1)
- `connect` — 4 files, IDENTICAL between RMS-IQ-Core-2 and Extraction-Akki; ABSENT in Akki-OS-V1 and Akki-Executive-Core.
- `memory` — 12 files, IDENTICAL between RMS-IQ-Core-2 and Extraction-Akki; ABSENT in Akki-OS-V1 and Akki-Executive-Core.
- `team` — 2 files, IDENTICAL between RMS-IQ-Core-2 and Extraction-Akki; ABSENT in Akki-OS-V1 and Akki-Executive-Core.
- `use_data` — 4 files, IDENTICAL between RMS-IQ-Core-2 and Extraction-Akki; ABSENT in Akki-OS-V1 and Akki-Executive-Core.

### 3.2 Present only in Akki-OS-V1
- `critic_pass` (7 files)
- `far_endpoint` (4 files)
- `generated_gates` (16 files)
- `partitions` (2 files)
- `registry_context` (5 files)
- `sequencing_harness` (7 files)

### 3.3 Present only in Akki-Executive-Core (engine-shaped only — flat single-file "services" omitted)
- `analyze_workspace` (3), `chat` (2), `cohort` (8), `crypto` (2), `documents` (4),
  `ideas_engine` (8), `inbox_routing` (11), `monitor` (5), `open_questions` (2),
  `solva_v2` (30), `solva_voice_audit` (24), `streaming` (3), `tasks` (5),
  `tasks_initiatives` (3), `work_studio` (2), `workbook_analyzer` (10).
- Plus loose files sitting directly in `backend/services/*.py` (36 of them):
  `analysis_lifecycle.py`, `backfill_shield_v1.py`, `clamav_service.py`,
  `cohort_email.py`, `cohort_email_html.py`, `continue_chat.py`,
  `csrf.py`, `cycle_lifecycle.py`, `cycle_permissions.py`, `cycle_synthesis.py`,
  `deck_generation_jobs.py`, `deck_lineage.py`, `deck_regenerate.py`,
  `deck_retrieval.py`, `first_login_password_set.py`, `job_queue.py`,
  `llm_streaming.py`, `metadata_signatures.py`, `module_labels.py`,
  `news_aggregator.py`, `owner_digest.py`, `platform_kb.py`, `privacy_wall.py`,
  `rate_limit.py`, `rbac.py`, `sandbox_generation.py`, `security_headers.py`,
  `sentry_setup.py`, `session_timeout.py`, `signal_dedup.py`,
  `solva_session_status.py`, `storage_service.py`, `streaming_phases.py`,
  `stripe_webhook.py`, `two_pass.py`, `universal_search.py`,
  `work_studio_export.py`, `work_studio_overlay.py`.

## 4. Top findings (measurement level only)

1. **RMS-IQ-Core-2 ≡ Extraction-Akki on all shared services except two tier_lock deltas in `economics`.** These two repos are near-duplicates by content. Extraction-Akki holds the more recent commit on `economics` (2026-08-01T20:02Z vs RMS-IQ-Core-2's 2026-08-01T04:13Z) and adds 10 tier_lock files.
2. **Akki-OS-V1 is an older, partially-superset fork.** It carries several services the other two don't (`critic_pass`, `far_endpoint`, `generated_gates`, `partitions`, `registry_context`, `sequencing_harness`), but is behind the other two on `auth`, `compliance`, `economics`, `health`, `registry`, `synisense`, `wizard`, and lacks `connect`, `memory`, `team`, `use_data` entirely.
3. **Akki-OS-V1 has extra services on `service_1` and `targeta`** that RMS-IQ-Core-2 / Extraction-Akki lack: `batch_quarantine.py`, `gap_candidate_filer.py`.
4. **Akki-Executive-Core is not the same platform.** Only one service name (`synisense`) overlaps with the core three, and that overlap is DIVERGED both ways. Executive-Core does NOT carry the `mtafiti / northena / perception / solva_depth / layer_[abc] / opportunity_briefs / v[123]_harness / v2_gate / g1_defensibility / outer_gate / master_admin` engine set at all. It carries its own set: `solva_v2`, `solva_voice_audit`, `ideas_engine`, `inbox_routing`, `workbook_analyzer`, `cohort`, `cycle_*`, `deck_*`, `work_studio*`, and a large loose-file services surface.
5. **`economics` is the highest-volatility service.** 291 files present in Extraction-Akki are missing from Akki-OS-V1, and 380 additional files have the same name but different content between those two — so it is impossible to describe Akki-OS-V1's `economics` as a subset. It has genuinely diverged.
6. **Only Akki-Executive-Core lacks BUILD_JOURNAL.md, docs/close_reports/, and docs/audits/** — the other three all carry them.

## 5. Method

- All paths and file counts: `git ls-files` inside each repo.
- All content comparisons: SHA-256 of every file bytes, path-keyed.
- All dates: `git log -1 --format=%cI -- <path>` at HEAD SHAs listed in `repo_summaries.md` §1.
- Scripts producing this data:
  - `/app/assessment_workspace/tools/services_overlap.py` (raw dump → `notes/_raw_services.txt`)
  - `/app/assessment_workspace/tools/service_diff.py` (delta table → `notes/_raw_service_diff.md`)
