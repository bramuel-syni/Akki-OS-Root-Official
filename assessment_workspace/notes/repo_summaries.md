# Repo Summaries — Chunk 1 ground truth

Session evidence only. All facts below come from `git` commands and `git ls-files`
executed against the pinned HEAD SHAs listed for each repo.

## 1. Header table

| Repo | Default branch | Pinned HEAD SHA | Last commit (ISO) | Total commits |
|---|---|---|---|---:|
| RMS-IQ-Core-2 | `main` | `ea5aa019521eee22ad4f8ea29efdfa2af357be3b` | 2026-08-01T08:10:07+00:00 | 198 |
| Akki-OS-V1 | `main` | `8c361903cdd319bfdc0709de3f4392f5bfa3956b` | 2026-08-14T05:30:51+00:00 | 167 |
| Extraction-Akki | `main` | `b150c21c1ac6fae8d052332aaff56ae952daae25` | 2026-08-14T05:27:40+00:00 | 204 |
| Akki-Executive-Core | `main` | `5844eee95d5faffea0dcab98bd4fe5e8d1419f32` | 2026-07-08T13:46:49+00:00 | 929 |

- Last commit message on all four repos: `"Auto-generated changes"`. Recorded as fact, no interpretation.
- Extraction-Akki and Akki-OS-V1 both show a 2026-08-14 top-of-tree commit; RMS-IQ-Core-2 is 13 days behind them at 2026-08-01; Akki-Executive-Core is 5+ weeks behind at 2026-07-08.

## 2. File-count by type

Buckets exactly as requested (py / js / jsx / ts / tsx / other). "test files" = any tracked path
matching `(^|/)tests?(/|$)` OR filename `*_test.*` / `*_spec.*` / `*.test.*` / `*.spec.*`.

| Repo | py | js | jsx | ts | tsx | other | test files | total files |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RMS-IQ-Core-2 | 498 | 82 | 50 | 24 | 0 | 1865 | 254 | 2519 |
| Akki-OS-V1 | 487 | 67 | 13 | 24 | 0 | 1532 | 222 | 2123 |
| Extraction-Akki | 499 | 83 | 55 | 24 | 0 | 1892 | 256 | 2553 |
| Akki-Executive-Core | 1013 | 74 | 392 | 4 | 0 | 4435 | 505 | 5918 |

Observations (measurements only, not interpretation):
- No `.tsx` files exist in ANY of the four repos.
- Akki-Executive-Core has ~2× the Python code and ~7× the `jsx` files of the other three.
- The three "core" repos (RMS-IQ-Core-2 / Akki-OS-V1 / Extraction-Akki) sit in the same order of magnitude on every axis; Akki-Executive-Core sits on a different scale.

## 3. Top-level directory tree (level 1)

Only non-hidden entries and depth 1. Numbers are `git ls-files` entry counts under each entry.

### 3.1 RMS-IQ-Core-2 (level 1)
```
.dockerignore                            1
.emergent/                               6
.gitconfig                               1
.github/                                 1
.gitignore                               1
BUILD_JOURNAL.md                         1
Dockerfile                               1
Makefile                                 1
README.md                                1
backend/                              1965
docker-compose.yml                       1
docs/                                  300
frontend/                              119
memory/                                  6
salvage/                                66
test_reports/                           41
test_result.md                           1
tools/                                   6
```

### 3.2 Akki-OS-V1 (level 1)
```
.dockerignore                            1
.emergent/                               6
.gitconfig                               1
.github/                                 1
.gitignore                               1
BUILD_JOURNAL.md                         1
Dockerfile                               1
Makefile                                 1
README.md                                1
backend/                              1669
docker-compose.yml                       1
docs/                                  278
frontend/                              126
memory/                                  7
salvage/                                18
test_reports/                            4
tools/                                   6
```
Note (measured, not inferred): Akki-OS-V1 has NO `test_result.md` at repo root.

### 3.3 Extraction-Akki (level 1)
```
.dockerignore                            1
.emergent/                               6
.gitconfig                               1
.github/                                 1
.gitignore                               1
BUILD_JOURNAL.md                         1
Dockerfile                               1
Makefile                                 1
README.md                                1
backend/                              1976
docker-compose.yml                       1
docs/                                  315
frontend/                              125
memory/                                  6
salvage/                                66
test_reports/                           43
test_result.md                           1
tools/                                   6
```

### 3.4 Akki-Executive-Core (level 1)
```
.dockerignore                            1
.emergent/                               1
.gitconfig                               1
.github/                                 7
.gitignore                               1
.gitleaks.toml                           1
AUDIT_iter68.md                          1
CHAT.docx                                1
DEPLOY.md                                1
Dockerfile.backend                       1
Dockerfile.frontend                      1
INTEGRATION.docx                         1
Makefile                                 1
README.md                                1
SOLVA.docx                               1
afya.docx                                1
auth_testing.md                          1
backend/                              3768
backend_test.py                          1
design_guidelines.json                   1
docker-compose.prod.yml                  1
docker-compose.yml                       1
docs/                                    40
frontend/                              597
memory/                               1305
nginx/                                   1
scripts/                                23
sdk/                                    12
syni.docx                                1
test_reports/                          140
test_result.md                           1
test_screenshots/                        2
tests/                                   1
```
Structural finding: Akki-Executive-Core has a materially different repo shape
— `sdk/` (12), `nginx/`, split `Dockerfile.backend`/`Dockerfile.frontend`, and
loose top-level `.docx` files (CHAT/INTEGRATION/SOLVA/afya/syni). The other three
repos share a common shape (`Dockerfile`, `BUILD_JOURNAL.md`, `salvage/`, etc.).

## 4. `backend/services/` (or equivalent) subdirectory listing per repo

Full per-repo listing with file counts. Details in
`_raw_services.txt` (lines 5–177). Summary:

| Repo | # service dirs under backend/services/ | # files under backend/services/ |
|---|---:|---:|
| RMS-IQ-Core-2 | 36 | 1692 |
| Akki-OS-V1 | 38 | 1423 |
| Extraction-Akki | 36 | 1702 |
| Akki-Executive-Core | 56 | 195 |

- The 56 "service dirs" in Akki-Executive-Core mostly resolve to single loose `.py`
  files sitting directly under `backend/services/` (e.g. `csrf.py`,
  `rate_limit.py`, `two_pass.py`, `platform_kb.py`), not real subdirectories.
  Genuine sub-directories under Akki-Executive-Core's `backend/services/` are
  fewer: `analyze_workspace`, `chat`, `cohort`, `crypto`, `documents`,
  `ideas_engine`, `inbox_routing`, `monitor`, `open_questions`, `solva_v2`,
  `solva_voice_audit`, `streaming`, `synisense`, `tasks`, `tasks_initiatives`,
  `work_studio`, `workbook_analyzer`.

The three "core" repos share a common set of ~34 service directories
(economics, mtafiti, northena, perception, synisense, service_1, solva_depth,
compliance, auth, data_source, etc.). Only `synisense` overlaps by name with
Akki-Executive-Core (see cross_repo_overlap.md for the measured delta).

## 5. BUILD_JOURNAL / docs/close_reports / docs/audits presence

Titles/dates only per instructions (verification of claims is Chunk-2 work).

### 5.1 RMS-IQ-Core-2
- `BUILD_JOURNAL.md`: present (1 file)
- `docs/close_reports/`: **44 files** — full listing in `_raw_services.txt` (lines 294–338). Examples: `p1_custody_closure_honest_startup.md`, `phase3_subcycle1_real_material_readiness_2026-08-01.md`, `phase_8_conformance_map.md`, `production_housing_ph_r1.md`, `machine_readable_registry.md`.
- `docs/audits/`: **19 files**. Examples: `engine_conformance_v1.md`, `g3_solva_conformance_v1.md`, `g4_mtafiti_conformance_v1.md`, `g4_targeta_conformance_v1.md`, `g5a_conformance_v1.md`, `g5b_conformance_v1.md`, `g6_conformance_v1.md`, `northena_conformance_v1.md`, `solva_conformance_v1.md`, plus a `substrate_drop_v1/` sub-folder with 6 reconciliation files.

### 5.2 Akki-OS-V1
- `BUILD_JOURNAL.md`: present (1 file)
- `docs/close_reports/`: **44 files** — full listing in `_raw_services.txt` (lines 363–406). Contains extras not in RMS-IQ-Core-2/Extraction-Akki: `change_order_2026_07_25.md`, `critic_pass.md`, `eab_2.md`, `eab_3.md`, `g_13.md`, `substrate_drop_v3.md`.
- `docs/audits/`: **22 files** — includes items not in the other two: `lt2_forensic_correction_2026_07_24.md`, `lt2_sequencing_harness_provenance_d7_2026_07_24.md`, `product_doc_v3_1_untraceable_d7_2026_07_24.md`, `substrate_drop_v3_reconciliation_2026_07_24.md`.

### 5.3 Extraction-Akki
- `BUILD_JOURNAL.md`: present (1 file)
- `docs/close_reports/`: **44 files** — full listing in `_raw_services.txt` (lines 434–477). List matches RMS-IQ-Core-2 exactly by filename.
- `docs/audits/`: **19 files** — list matches RMS-IQ-Core-2 exactly by filename.

### 5.4 Akki-Executive-Core
- `BUILD_JOURNAL.md`: **MISSING**.
- `docs/close_reports/`: **0 files** (directory does not exist under docs/).
- `docs/audits/`: **0 files** (directory does not exist under docs/).
- What exists under `docs/` in Akki-Executive-Core (40 files total) is different: `docs/RUNBOOKS/` (5), `docs/runbooks/` (5), `docs/sprints/` (5), plus loose files. It does NOT participate in the "canon build-journal + close-report + audit" documentation model used by the other three.

The problem statement's expectation that each repo carries these three artifacts holds
for RMS-IQ-Core-2, Akki-OS-V1, and Extraction-Akki. It does NOT hold for
Akki-Executive-Core — reported explicitly, not papered over.

## 6. Notes on read-only handling
All measurements were produced by:
- `git rev-parse HEAD`, `git rev-parse --abbrev-ref HEAD`, `git log -1 --format=…`, `git rev-list --count HEAD`
- `git ls-files` + Python counting/hashing
- `git log -1 --format=%cI -- <path>` for per-path dates

No repo file was modified. All analysis scripts live under
`/app/assessment_workspace/tools/`.
