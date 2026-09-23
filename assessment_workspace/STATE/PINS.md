# PINS.md — Immutable references for cold-reader continuity

**Last updated:** 2026-08-14.

## Repository pins

| Repo | Branch | Pinned HEAD SHA | Last commit ISO | Total commits |
|---|---|---|---|---:|
| RMS-IQ-Core-2 | `main` | `ea5aa019521eee22ad4f8ea29efdfa2af357be3b` | 2026-08-01T08:10:07+00:00 | 198 |
| Akki-OS-V1 | `main` | `8c361903cdd319bfdc0709de3f4392f5bfa3956b` | 2026-08-14T05:30:51+00:00 | 167 |
| Extraction-Akki (spine) | `main` | `b150c21c1ac6fae8d052332aaff56ae952daae25` | 2026-08-14T05:27:40+00:00 | 204 |
| Akki-Executive-Core | `main` | `5844eee95d5faffea0dcab98bd4fe5e8d1419f32` | 2026-07-08T13:46:49+00:00 | 929 |

Spine cited throughout BUILD_STRATEGY as **Extraction-Akki** (≡ RMS-IQ-Core-2 byte-identical on all shared code; Extraction-Akki carries 10 additional `tier_lock.v139x.json` runtime snapshots and 3 additional repo-top files).

## Canon document pins

**Core 9-doc canon pack** — source archive: `https://customer-assets-v7afamib.emergentagent.net/job_a963bf18-f7d3-42c9-b8dd-aba51af40caf/artifacts/96u2c488_files%20%288%29.zip` (236,005 bytes · sha256 `5a46676d9c8506cc4d65616e3dbfa9db76885362fbaa0c210894295daae30759`). Extracted to plain text via `python-docx` at `/app/assessment_workspace/canon/text/`. Verified byte-identical to on-disk `/app/assessment_workspace/canon/canon_pack.zip` on 2026-09-13.

| Canon | Filename | Bytes | Extracted-text line count |
|---|---|---:|---:|
| 1 · Custody Platform | `Akki_Canon_1_Custody_Platform.docx` | (varies) | 206 |
| 2 · Conditioned Ideation Faculty | `Akki_Canon_2_CIF.docx` | | (opened) |
| 3 · Governance Engines | `Akki_Canon_3_Governance_Engines.docx` | | 265 |
| 4 · Operating Engines | `Akki_Canon_4_Operating_Engines.docx` | | 365 |
| 5 · Interface Architecture | `Akki_Canon_5_Interface_Architecture.docx` | | 421 |
| 6 · User Journeys | `Akki_Canon_6_User_Journeys.docx` | | 134 |
| 7 · Integration and Quality | `Akki_Canon_7_Integration_and_Quality.docx` | | 288 |
| 8 · The Watch | `Akki_Canon_8_The_Watch.docx` | | 223 |
| 9 · Mkondo Charter | `Akki_Canon_9_Mkondo_Charter.docx` | | 38 |

**Canon-family expansion beyond the core 9** (accumulated 2026-08-27 → 2026-09-13; refreshed at M0 close 2026-09-13):

| Batch | Path | Content | Extraction |
|---|---|---|---|
| Addendum 1 (2026-08-27) | `canon/AKKI_Canon_Addendum_1.docx` sha256 `9f00f7bc20…` (16,794 B) | AKKI CANON — ADDENDUM 1 | `notes/canon_addendum_1_requirements.md` (Aug 27) |
| W11 batch v3 (2026-08-28) | `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.docx` sha256 `991e02adf3…` (45,102 B) | Canon Documents 17–20 · GOVERNED ARTIFACT SPECIFICATION | ❌ pending scope decision |
| W11 new docs (2026-08-28) | `canon/w11_new_docs/canon_17_19.docx` sha `9b632df11f…` (32,600 B) · `audio_intel_plane_spec.docx` sha `b6ad57b369…` (26,623 B) · `training_capacity.docx` sha `d4c11f3c1b…` (21,783 B) · `training_techniques.docx` sha `5ca268505e…` (13,538 B) | 17-19 (older) · Audio Intelligence Plane · Training Capacity · Training Techniques | `notes/AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md` (partial); rest ❌ pending scope decision |
| Drop 2026-09-09 (files_14 · 11 docs) | `canon/drops/20260909/extracted/files_14/*.docx` + `DAP_Backend_Spec_v1.docx` (`e675990aa6…` · 21,346 B) | TCB Enumeration · Security Architecture Description · Determinism Inventory · Security Function Policies · Failure Posture Enumeration · Trust Domain Description · Handoff Generalisation · Business Continuity Annex · Pruning-Unlearning Amendment · Governance Architecture v1 (`b8af25f486…` · 51,456 B) · Security Assurance Promise Set v1 (`8c7a3b7205…` · 16,864 B) · DAP Backend Spec | Full row-level extraction M0 2026-09-13: `notes/canon_dap_backend_spec_v1_requirements.md` · `canon_tcb_enumeration_v1_requirements.md` · `canon_determinism_inventory_v1_requirements.md` · `canon_security_architecture_description_v1_requirements.md` · `canon_security_function_policies_v1_requirements.md` · `canon_failure_posture_enumeration_v1_requirements.md` · `canon_trust_domain_description_v1_requirements.md` · `canon_business_continuity_annex_v1_requirements.md` · `canon_handoff_generalisation_v1_requirements.md` · `canon_pruning_unlearning_amendment_v1_requirements.md` |
| Drop 2026-09-10 (files_15 · 3 docs) | `canon/drops/20260910/extracted/files_15/Agent_Swarm_Containment_Governance_Model_v1.docx` (`2824796d06…` · 18,435 B) · `Ratification_Record_v1.docx` (`b4de066419…` · 14,164 B) · `Master_Requirements_Registry.xlsx` (`27d413221e…` · 57,047 B) · `Akki_Governance_Architecture_v1.docx` **REVISED** (`b03932000c…` · 51,587 B · +131 bytes vs files_14) | Agent Containment · Ratification Record · Master Requirements Registry · Governance Architecture v1 (revised) | `notes/canon_agent_containment_spec_v1_requirements.md` (Sep 9) · Ratification-Record parsed into `MILESTONE_PROMISE_BINDING_20260913.md §D` and executed as `notes/RATIFICATION_C3_BATCH_20260913.md` · Governance-Architecture-v1 revised delta at `notes/canon_governance_architecture_v1_files15_delta.md` (M0 2026-09-13; base extraction at `notes/ingest_20260907/canon_doc0_governance_architecture_requirements.md`) · Master_Requirements_Registry cross-walk **deferred to scope decision** |
| Drop 2026-09-13 (owner-attached · 2 docs) | `canon/drops/20260913/raw/Security_Assurance_Promise_Set_v2.xlsx` sha256 `72a4e7620c959a8d0dd36c73ed5c712689ed8f0663630803b79a43f0db453088` (17,480 B; +S-27 row) · `Serving_Integrity_Amendment_v1.docx` sha256 `56af9f09c93e38ad8b80c6f70cd07c1dc03efba8c9661d2d9e717d54b3144269` (15,863 B) | Security Assurance Promise Set v2 (S-1..S-27; 27th is new) · Serving Integrity Amendment (V-1..V-4, R-13/14, adds A20.15/SFP-8/DAP-31+/DAP-32+/AC-13/AC-14/A5.7+) | `notes/canon_security_assurance_promise_set_v2_delta.md` · `notes/canon_serving_integrity_amendment_v1_requirements.md` |

**Verified count of unique canon-family artefacts on disk (M0 close 2026-09-13):** **29 unique .docx** (by sha256) · **2 unique .xlsx** · **2 unique .zip** (files_14, files_15) · **2 unique .html** (`RMS_AI_Prototype_standalone_v3.html`, `RMS_Data_Access_Portal_standalone.html`).

Prototype: `/app/assessment_workspace/prototype/prototype.html` (v6 Standalone · 626,618 bytes · 395 lines · sha256 `794fcd86374d0450d853afa47e2fdf4bd34a7aab85cb1945cae209a2cf60c25b`; v6 remains the assessment reference per Q4 DEFAULT-PENDING-OVERRIDE. Drop-09-09 ships `RMS_AI_Prototype_standalone_v3.html` and `RMS_Data_Access_Portal_standalone.html` as separate lineages — enter as additional surfaces flagged in prototype_inventory v9 at Phase-2 open).

## Deliverables — absolute paths

- `/app/assessment_workspace/REUSE_ASSESSMENT.md` (450 lines) — ACCEPTED 2026-08-14.
- `/app/assessment_workspace/BUILD_STRATEGY.md` — in progress.
- `/app/assessment_workspace/STATE/CONTEXT.md`, `STATE/PINS.md`, `STATE/DECISIONS.md`, `STATE/NEXT.md` — this directory.

## Notes files (all under `/app/assessment_workspace/notes/`)

Canon requirement extractions (C1–C9):
- `canon_1_requirements.md` (75 rows C1-001…C1-075)
- `canon_2_requirements.md` (66 rows C2-001…C2-066)
- `canon_3_requirements.md` (61 rows C3-001…C3-061)
- `canon_4_requirements.md` (68 rows C4-001…C4-068 incl. C4-037a–f)
- `canon_5_requirements.md` (70 rows C5-001…C5-070)
- `canon_6_requirements.md` (62 rows C6-001…C6-062)
- `canon_7_requirements.md` (35 rows C7-001…C7-035 + 26 defects C7-D01…C7-D26)
- `canon_8_requirements.md` (72 rows C8-001…C8-072)
- `canon_9_requirements.md` (50 rows C9-001…C9-050)

Domain tables:
- `domain_5_1.md` — Custody & Boundary
- `domain_5_2.md` — Direction & Record
- `domain_5_3.md` — Measurement / Targeting / Reasoning
- `domain_5_4.md` — Extraction & Quality
- `domain_5_5.md` — Integration
- `domain_5_6.md` — Governed values & Ceremony
- `domain_5_7.md` — Interface
- `domain_5_8.md` — The Watch
- `domain_5_9.md` — Orchestration (Mkondo)
- `domain_5_10.md` — Cross-cutting

Inventories:
- `build_inventory.md` — 148 BUILD rows + 9 HARVEST clusters
- `retire_inventory.md` — 37 concrete retire items + 7 renames

Assessment shaping / verification:
- `claims_verification.md` — seven §6 claims verified with cross-repo status
- `shaping_answers.md` — spine + Executive-Core RE-POINT reasoning

Chunk-1 outputs:
- `repo_summaries.md` · `cross_repo_overlap.md` · `prototype_inventory.md` · `chunk1_summary.md`
- `_raw_repo_trees.txt`, `_raw_services.txt`, `_raw_service_diff.md` (raw data dumps)

Strategy work-in-progress (to be created):
- `row_to_item_index.md` — every canon requirement row (C1-001 … C9-050) → work-item ID; mechanically audited.
- `strategy_items_part1.md` — MODIFY/PARTIAL, RE-POINT, HARVEST, RETIRE, WIRING items.
- (Future) `strategy_items_part2.md` — BUILD items.
- (Future) `fidelity_ledger.md` — every open question / uncertain field, phrased for owner ruling.

## Audit tools

- `/app/assessment_workspace/tools/citation_audit.py` — mechanical citation checker; must run clean before every deliverable submission. Latest run (post-remediation + assembly): **104/104 file · 1778/1778 canon · 0 failed**.
- Other analysis scripts: `extract_docx.py`, `repo_tree.py`, `services_overlap.py`, `service_diff.py`, `file_type_table.py`, `drift_map.py`, `drift_apply.py`, `drift_downstream.py`, `completeness_audit.py`, `assemble_build_strategy.py`.

## Execution pins (Build Order 01)

**Branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`.
**Baseline SHA:** `b150c21` (pinned citation baseline — never rewritten).
**Push:** none — owner Clarification 1 (2026-08-14). Local git history IS the record.

**Pod public egress IP** (for AISCA VM allowlist): **`35.225.230.28`** as of 2026-08-14 Owner-Simplification cycle (verified live via provisioning-card render in Playwright screenshot). Rotated from `104.198.214.223` last cycle → `34.170.12.145` cycle before that → `34.16.56.64` originally (fidelity-ledger FL-P2-09 OPEN for owner disposition — pod egress rotation is continuous). **The IP `34.16.56.64` remains in `SPINE_ALLOWED_IPS` per owner's strict stop-order directive; pod egress is NOT self-allowlisted.**

**Access mechanism (Owner stop-order 2026-08-14 · minted-credential pattern retired estate-wide).** Source-IP allowlist middleware live on BOTH FastAPI backend and CRA dev-server. Config in `/app/backend/.env`: `SPINE_ALLOWED_IPS` (comma-separated /32s) + `SPINE_TRUSTED_PROXY_HOPS=2`. Refusal grammar: HTTP 403 `text/plain` `"This surface answers allowlisted addresses only."`. Trust boundary: `xff.split(',')[-3]` per empirically discovered Cloudflare-worker + Cloudflare-edge + Google-Cloud-LB topology (FL-P2-10 CLOSED). No shared bearer token exists anywhere on the estate; `spine_auth.py` and `.owner_credentials` retired.

**Two-week checkpoint deadline:** **provisioning day + 14 — AWAITING PROVISIONING DATE** (per Build Order 01 §6). Update this pin to the actual UTC deadline once the VM is provisioned.

**Phase-1 A0/A1 tests-first evidence:** 26/26 gating tests pass (`phase0/A0-A1_report.md` + drill receipt `phase0/drill_receipts/20260814T120336Z_declaration_refusal_firing.log`).

**WS-BUILD-CONNECT-GPU + IP allowlist + re-home + wizard-completion + Owner Simplification single-panel collapse + Owner Phase-0 Execute + Owner Ruling first-DATA (Aurora RDS Data API) cycles 2026-08-14 → 2026-08-18:** **174/174 total gating tests green** on programme/track-a HEAD `f87b769` = 134 backend python (108 prior + 22 rds_data_submit + 4 credentials_paste parser data-source extension) + 12 frontend allowlist node --test + 28 frontend rehome/single-panel+data-source node --test. Right-reason failure receipts banked BEFORE each implementation lands (this cycle's additions):
- `phase0/drill_receipts/20260818T181236Z_sudo_invocation_right_reason_failure.log` (1/2 tests fail before sudo prefix lands on remote_harden)
- `phase0/drill_receipts/20260818T181454Z_harden_dropin_right_reason_failure.log` (2/3 tests fail before harden.sh drops 00-akki-no-password.conf)
- `phase0/drill_receipts/20260818T200211Z_rds_data_right_reason_failure.log` (21/39 tests fail before services.connect.rds_data_submit lands + parser AWS extension)
- `phase0/drill_receipts/20260818T200633Z_data_source_frontend_right_reason_failure.log` (4/28 rehome tests fail before ConnectWizard.jsx data-source path lands)
- Green receipt: `phase0/drill_receipts/20260818T200833Z_rds_data_green.log` (174/174 all three suites green).
- Playwright render-tree screenshots (Owner Ruling FL-P2-23 first DATA connection):
  `phase0/drill_receipts/screenshots/20260818T202000Z_data_source_{paste_parsed, manual_fields, four_questions_result}.jpeg` — prove data-source chip selects, aws_secret_access_key renders '•••• captured' sentinel in confirmation, manual fallback fields inline (aws_access_key_id/aws_secret_access_key/region/cluster_arn/secret_arn/database) with aws_secret masked type=password, four-questions result view renders `link_working=no`, `failure=other`, plain sentence 'The Data API returned an unexpected error (UnrecognizedClientException).', engine=aurora, channel=rds-data-api, standing creds stored key-custody-locally at `/app/backend/estate_keys/data_sources/akki-aurora.json` mode 0600.
- Prior-cycle receipts retained: `20260814T145500Z_ip_allowlist_right_reason_failure.log`, `20260814T151000Z_rehome_right_reason_failure.log`, `20260814T180000Z_registry_wizard_right_reason_failure.log`, `20260814T184500Z_estate_keys_and_connect_estate_right_reason_failure.log`, `20260814T185000Z_5step_wizard_right_reason_failure.log`, `20260815T015421Z_credentials_paste_parser_right_reason_failure.log`, `20260815T015855Z_single_panel_right_reason_failure.log`, `20260818T181034Z_phase0_execute_run.log`, `20260818T181308Z_phase0_execute_retry.log`, `20260818T181631Z_key_only_reharden.log`, `20260818T181742Z_acceptance_run.log`, `20260818T181808Z_vendor_evidence.log`, `20260818T195156Z_link_capacity_measure.log`, `20260818T195156Z_throughput.log`.
- No-LLM-transit hard-rule proof (bootstrap-cycle): `phase0/drill_receipts/20260818T181348Z_no_llm_transit_proof.log`.

**Estate ed25519 keypair · this-cycle live values (rotate on pod restart):**
- Estate public key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGKlcjZE/04clh3FLddGn7Wx69pytk8KJA5j9M6rKVA7 estate@akki`
- Fingerprint: `SHA256:TpJcdNAQ4iSQKK5inwPueOM6Qak5NcsD5XhZpWorZ+c`
- Pod egress IP (live-discovered): `35.225.230.28` (was `104.198.214.223` prior cycle; was `34.170.12.145` cycle before; STATE originally pinned `34.16.56.64` - see FL-P2-09 OPEN).
- Private key at `${ESTATE_KEYS_DIR}/estate_ed25519` mode 0600, never in git, never in return values.

**Attachment status (2026-08-14 · fixture-arrival cycle):** two of three fixtures delivered as files, third arrived as inline owner transcription. All FIXTURE PENDING markers CLEARED at transcription grade (files below). Governance grade distinction (transcription-cleared vs file-cleared) recorded in `notes/fidelity_ledger.md` FL-P1-14 + FL-P1-14a.

| Fixture | On disk at | sha256 | Grade |
|---|---|---|---|
| Akki Prototype v7 Design Brief | `/app/assessment_workspace/fixtures/Akki_Prototype_v7_Design_Brief.md` (18,791 bytes) | `063f2b470d74dcd30ad43b4645c4e656edaa7fb1185198a4116ad5328a9717b4` | file-cleared |
| AISCA GPU Access Guide | `/app/assessment_workspace/fixtures/AISCA_GPU_Access_Guide.pdf` (535,169 bytes) | `0f6b6e0f692494e18a65df655fddf48f45839005dc7aa6b988239b8f90e157f3` | file-cleared (SOP↔Order §6 conflicts A + B ESCALATED per Q2(a) — see `fixtures/aisca_sop_extraction.md` + FL-P2-03 / FL-P2-04) |
| Reference screenshot | `/app/assessment_workspace/fixtures/reference_screenshot_transcription.md` (owner-inline transcription; original image not yet in workspace) | `d3ae9a6cf598a38333b5c11d6d73dc9069dc3671fb31598f2e594dfb002fc949` | **transcription-cleared** (Q1(c) ruling · 2026-08-14 · re-open on image-file arrival if pixels contradict transcription) |
| Screen mockups v7 (Registry brief) | `/app/assessment_workspace/fixtures/screen_mockups_v7.pdf` (195,644 bytes; 5 pages TEXT ONLY - Registry feature & component brief; zero embedded images) | `418ad0e3c087c613be7d7d885a18a3c895b7d51ed253119aff9ba042ee81da8a` | **file-cleared** (spec/rules · owner named this the binding fixture for Registry + Connect wizard grammar 2026-08-14). **DISCREPANCY:** owner said "19 pages" - actual is 5; owner said "plus 4 inline screenshots" - none accessible as job assets. Owner's inline textual description of the screenshots (see DECISIONS.md ruling this cycle and `notes/fidelity_ledger.md` FL-P2-11) stands as the binding visual reference. Inventory: `fixtures/screen_mockups_inventory.md`. |

**Binding acceptance criteria** extracted at `/app/assessment_workspace/fixtures/binding_acceptance_criteria.md` (BAC-1..BAC-13). Every interface item in BUILD_STRATEGY.md now cites the applicable BAC-N in its DoD; `test_four_questions_topline_present` added to every console item's new-invariants list (Build Order 01 §3).

<!-- CONNECT-GPU-PINS -->
## WS-BUILD-CONNECT-GPU — commissioning record pinned outputs
- **host_name:** `aisca-gpu-01`
- **public_ip:** `127.0.0.1`
- **private_ip:** `10.0.0.10`
- **os:** `Ubuntu 24.04`
- **deploy_date:** `2026-08-14`
- **checkpoint_14d_utc:** `2026-08-28T00:00:00Z`
- **hardening_status:** `attested`
- **acceptance_status:** `green`
- **commissioning_record:** `/app/assessment_workspace/phase0/commissioning_records/commissioning_aisca-gpu-01_20260923T122527Z.json`
<!-- CONNECT-GPU-PINS -->


<!-- DATA-CONNECTED-PINS -->
## DATA CONNECTED · Aurora RDS Data API · first two databases (2026-08-19)

Both databases on cluster `db-restore-603-cluster` (eu-west-1) reached over RDS Data API from the pod's boto3 rds-data client (HTTPS, no VPC peering, no IP allowlisting on the DB side). Engine + version + inventory captured for BOTH via `information_schema` only — **zero record contents were read this cycle**.

- **region:** `eu-west-1`
- **cluster_arn:** `arn:aws:rds:eu-west-1:494452543252:cluster:db-restore-603-cluster`
- **secret_arn:** `arn:aws:secretsmanager:eu-west-1:494452543252:secret:rds/data/api/user/secrets-8rZuVc`
- **iam user:** `arn:aws:iam::494452543252:user/api_user` · access key prefix `AKIAXGH5` (custody `/app/backend/estate_keys/data_sources/aws_iam_user_AKIAXGH5.json` mode 0600, git-ignored)
- **engine (both DBs):** `aurora-mysql`
- **engine_version (both DBs):** `8.0.42 (Aurora MySQL 3.10.3)` (captured strings: `@@version='8.0.42'`, `@@version_comment='6252a59a'`, `@@aurora_version='3.10.3'`)
- **channel:** `rds-data-api`
- **actor on declaration:** `aws.rds.db-restore-603-cluster`
- **capabilities:** `[sql_query_https]` · **scope:** `[data.estate]`

| source_id | database | table_count | top row (approx) | receipt sha256 |
|---|---|---|---|---|
| `aws.rds.db-restore-603-cluster.digicow_live` | `digicow_live` | 125 | `ussd_users` ≈ 2,285,264 rows / 747.7 MB | `c6698e22673c7ee8a72f15af7798c58a94b7a558aea3a2942b8c3ef7f816f294` |
| `aws.rds.db-restore-603-cluster.ndume` | `ndume` | 110 | `breedings` ≈ 184,348 rows / 155.8 MB | `572f13108894a60892568e63609b36555cc3ae75fadc47d6d0caa4ba2a95aab7` |

**Data connection records (JSON):**
- `phase0/data_connection_records/data_source_digicow_live_20260819T152513Z_FINAL.json`
- `phase0/data_connection_records/data_source_ndume_20260819T152513Z_FINAL.json`

**Drill receipts:**
- Pipeline pass (production path) — `phase0/drill_receipts/20260819T152331Z_aurora_connect_and_inventory.log` (SELECT 1 YES for both; engine misclassified `unknown` — production defect that motivated FL-P2-24)
- Inventory retry (throwaway script, forced engine=mysql, added `@@aurora_version` probe) — `phase0/drill_receipts/20260819T152509Z_aurora_inventory_mysql.log` (engine-probe strings + top-25 tables per DB + 5 structural reads per DB, `[DONE]` marker)
- Engine-detect fix right-reason failure (banked BEFORE the fix landed) — `phase0/drill_receipts/20260819T153408Z_engine_detect_right_reason_failure.log`
- Engine-detect fix green — `phase0/drill_receipts/20260819T154016Z_engine_detect_green.log`

**Track-a commits (production engine-detect defect fix, FL-P2-24 CLOSED):**
- `8c9304d` Phase 1 tests-first · 7 engine-detect gating assertions using REAL captured strings
- `746dece` Phase 1 implementation · `_probe_engine(client, payload) → (engine, engine_version)` wired into `submit()` and `_write_record()`

**Standing posture on this pipeline (owner note "read access to all records… first pass STRUCTURE ONLY"):**
- First-pass read: `information_schema.schemata` + `information_schema.tables` + `information_schema.columns` only. Zero row-level access exercised this cycle.
- Record-level access (`SELECT ... FROM <schema>.<table>`) requires an explicit owner ruling on data admission + record-matrix binding (Canon 3 / Canon 4). Deferred until that ruling.
<!-- DATA-CONNECTED-PINS -->


<!-- OWNER-ARTIFACTS-2026-08-19 -->
## Owner artifact drop · 2026-08-19 (channel) · four artifacts

Four artifacts delivered this cycle for the v7-prototype ingest + tension-table task (FL-P2-26). Downloaded to `fixtures/` (and `canon/` for the addendum). Hashes below; contents inventoried in this-cycle notes.

| Artifact | Path | sha256 | Kind |
|---|---|---|---|
| `AKKI_Promise_Table.xlsx` | `fixtures/AKKI_Promise_Table.xlsx` (24,534 bytes) | `02817f8a0f637e7af98f1266b2b0423e179387ebb13a75bf77fc92ad7d0c233b` | Function & Promise Registry seed (XLSX) |
| `RMS AI · Akki Prototype v7 (Standalone).html` | `fixtures/RMS_AI_Akki_Prototype_v7_Standalone.html` (1,307,752 bytes) | `07df1d6846841da57ac0405536555262586362ac8d02a7bd682d9f3bebd6be55` | Standalone HTML prototype (behaviour + copy oracle) |
| `files (9).zip` | `fixtures/files_9.zip` (262,021 bytes) | `d063db00a1f1d83adbeb0498e02c824b2c9529731209a780deb9f24e68f8d3ee` | 16 .docx canon-shaped essays (see inventory below) |
| `AKKI_Canon_Addendum_1.docx` | `canon/AKKI_Canon_Addendum_1.docx` (16,794 bytes) | `9f00f7bc20e7c8d8dd7ad7957d0960eb9695f990409dc1292f08907d89f4dedc` | Canon-class amendment to the nine-canon corpus |

**Reclassified FINAL data-source records (FL-P2-24 downstream, this cycle):**

- `phase0/data_connection_records/data_source_digicow_live_20260819T152513Z_FINAL.json` — new sha256 `25b31d46a5455183a7acd71bb8068f3bd1e0bbd1390cd5186d9f2ff37afaaf5f` (prior `c6698e22673c7ee8a72f15af7798c58a94b7a558aea3a2942b8c3ef7f816f294`)
- `phase0/data_connection_records/data_source_ndume_20260819T152513Z_FINAL.json` — new sha256 `7924e8c2295bc429f5d204c62d317617b0047167673a1176c6cdde0327f8305c` (prior `572f13108894a60892568e63609b36555cc3ae75fadc47d6d0caa4ba2a95aab7`)

Reclassification carries an in-band `engine_source` field naming the throwaway origin and citing the production fix; the raw throwaway log stays as history at `phase0/drill_receipts/20260819T152509Z_aurora_inventory_mysql.log`.

<!-- REGISTRY-A4-2026-08-19 -->
## Registry cycle · Owner Order 2026-08-19 · FL-P2-25 CLOSED

- Track-a commits: `12985bd` (tests-first · 15 backend + 10 frontend gating assertions) → `0c417f2` (implementation · services.registry_facts + Registry.jsx rewrite).
- Backend endpoint: `GET /api/registry/facts` — no secrets, no invention, no LLM transit.
- Frontend surface: three-tab Registry per fixture (fluid left + 300px right context panel; Topline + Headliner / Visual + Context / Table + Context bands; content rules §6 honoured).
- Green receipt: `phase0/drill_receipts/20260825T151457Z_registry_facts_green.log` (15/15 registry_facts + 121/121 cohort + 38/38 rehome+registry).
- Journey walk screenshots (6): `phase0/drill_receipts/screenshots/20260819T151700Z_*.jpeg`.
<!-- OWNER-ARTIFACTS-2026-08-19 END -->


<!-- W2-REFLECTION-2026-08-25 -->
## W2 · Compute reflection-before-commit · FL-P2-27 · Doc 12 §B5.1–§B5.6 CLOSED

Owner Order 2026-08-19 "W2 go" · Owner Response 2026-08-25 (plan-confirmation + four additional invariants d/e/f/g). Executed tests-first per T1 with right-reason failure banked BEFORE any implementation landed. Doc12-003 (Promise #11) status **PARTIAL → DONE**. CA1-008 Cost Ledger stays in W6.

**Contract:**
- `POST /api/compute/reflection` — accepts `{proposed_action:{kind, scope_ref, scope_ceiling, budget_ceiling, commissioner, lawful_basis}}`; returns the B4 envelope: `reflection_id · feasibility_verdict · grounding_marker · lawful_basis · budget_ceiling · commissioner · scope_ceiling · price_model_version · measured_quantities · currency_figures · honest_gap · provenance · kind · scope_ref · generated_at_iso`.
- `POST /api/compute/commit` — accepts `{reflection_id, actor, proposed_action}`; refuses with HTTP 422 + plain-sentence reason on: missing reflection_id (`reflection_required`), unknown reflection_id (`reflection_id_unknown`), non-compute kind (`non_compute_kind`), or projection/action drift (`reflection_action_mismatch`). On success returns the run row: `run_id · kind · scope_ref · reflection_id · acknowledged_by · acknowledged_at_iso · committed_at_iso` (no embedded projection content).

**Persistence:**
- Projections at `phase0/reflection_records/refl-<hex12>.json` (identity records; NOT secrets; NOT credentials).
- Committed run rows at `phase0/commit_records/run-<hex12>.json`.
- No rate config on record (`price_model.v0-exploratory.json` is exploratory-status; the loader treats it as absent per Doc 12 §B5.4 non-precedent rule). `currency_figures` therefore renders `{}` and `honest_gap` names the missing ceremony verbatim per the owner grammar.

**Honest-gap sentence (verbatim, from owner):**
> "No rate is on record for this machine — the projection shows measured quantities only (GPU hours, storage touched). Money figures will appear when the cost ledger is in force."

**Ceremony fabric (v7 oracle EXACT per T1):**
Single sage-green **"Freeze & commit"** button after feasibility renders — NO checkbox, NO typed confirmation. The button IS the plain-sentence ack. Server-side gate refuses without a valid reflection_id (the gate is not the UI button state).

**Track-a commits on `programme/track-a`:**
- Tests-first · 12 backend + 7 frontend gating invariants · right-reason receipts:
  - `phase0/drill_receipts/20260825T180239Z_w2_reflection_right_reason_failure.log`
  - `phase0/drill_receipts/20260825T180509Z_w2_frontend_right_reason_failure.log`
- Implementation · `backend/services/compute_seam/{reflection.py, reflection_router.py}` + `pod_shell/frontend/src/components/Registry.jsx` ReflectionPanel + `pod_shell/backend/server.py` router mount.
- Commit SHAs recorded in DECISIONS.md at cycle close.

**Screenshots** (`phase0/drill_receipts/screenshots/`):
- `20260825T180800Z_w2_compute_card_before.jpeg` (panel closed)
- `20260825T180800Z_w2_compute_card_projection.jpeg` (projection rendered; measured quantities with provenance; honest gap; Freeze & commit visible)
- `20260825T180800Z_w2_compute_card_committed.jpeg` (COMMITTED banner · run-da0605a6e0cc · operator@estate · 2026-08-25T18:08:32.621770Z)

**Green receipt (backend 148/148 · frontend 61/61 rehome · 12/12 allowlist):**
`phase0/drill_receipts/20260825T180738Z_w2_reflection_green.log`

**Standing invariants held this cycle:**
- IP allowlist unchanged (`SPINE_ALLOWED_IPS=34.16.56.64`).
- No LLM transit; no HTTP client; no shield reference in reflection module (statically proven).
- No secrets read; no credentials transited.
- Estate ed25519 private key mode 0600 unchanged.
- REFERENCE-NOT-COPY design law honoured across new surface + new records.
<!-- W2-REFLECTION-2026-08-25 END -->


<!-- W3-DATA-SHIELD-2026-08-25 -->
## W3 · Chokepoint · masking tiers · exit gate · residency · Data Shield surface · FL-P2-27 · Doc 01/02 + CA1-007 + CA1-N4 CLOSED

Owner Order 2026-08-25 · "W3 go" (verbatim in DECISIONS.md). Executed tests-first per T1 with right-reason failure banked BEFORE any implementation landed. Scope class **L** confirmed at close (~1957 LOC ≤ 2000).

**Six mechanisms shipped:**
- (a) **Single outbound chokepoint** — `services.chokepoint.register_crossing()` names the sole path; static AST negative-scan build gate refuses any `import boto3 / paramiko / openai / anthropic / google.genai` outside exempted seams.
- (b) **Masking tiers** — governed positive allowlist `services/chokepoint/masking_tier_allowlist.v0.json` (structure_only / attested_command / receipt_only admissible today; t1_full_mask / t2_partial / t3_category DECLARED but admissible_under_env=[]).
- (c) **Exit gate** — two-layer (Doc 01 §A5.5): AST at build + runtime refusal at `register_crossing()`. The gate is the endpoint, never a disabled UI button.
- (d) **CA1-007 dry-run preview** — `POST /api/shield/dry-run` walks the crossing-receipt log by identity (REFERENCE-NOT-COPY). Refuses non-testable free-text declarations per Doc 02 §A5.2. Honest-gap sentence names the missing row-bearing traffic state.
- (e) **CA1-N4 residency** — governed positive allowlist `residency_allowlist.v0.json` (`eu-west-1` on record from Aurora facts; refusal grammar names the specific region + names the CA1-N4 authority for adding one). Silence explicitly refused (`region_not_on_record` sentinel).
- (f) **Data Shield surface** — `/shield` route → `DataShield.jsx` (Trust Center → Data Shield · v7 oracle fabric EXACT per T1). Four sub-surfaces: session timeline · rules-in-force · dry-run panel · refusal example. All render honest facts on disk.

**Real crossings brought under chokepoint (BEFORE any LLM path):**
- `services.connect.rds_data_submit.submit()` — kind='rds_data_api', tier='structure_only', region=eu-west-1.
- `services.compute_seam.seam.execute()` — kind='ssh_seam', tier='attested_command'. Refuses honestly when VM_REGION not set (akki-vm commissioning record does not carry a region field).

**Track-a commits on `programme/track-a`:**
- `ebacd65` · Section B: chokepoint core + masking + residency + exit-gate AST.
- `1a57314` · Sections C+D: dry-run + Shield HTTP router mounted at pod_shell.
- `15dbfc1` · Data Shield surface at /shield + full W3 cohort green.

**Green receipt (backend 169/169 · frontend rehome 69/69 · allowlist 12/12 = 250/250 · zero regressions):**
`phase0/drill_receipts/20260825T183814Z_w3_close_green.log`

**Three screenshots (owner-mandated) at `phase0/drill_receipts/screenshots/`:**
- `20260825T183800Z_w3_data_shield_surface.jpeg` — Shield surface top view.
- `20260825T183800Z_w3_dry_run_preview.jpeg` — dry-run walk complete against real receipts.
- `20260825T183800Z_w3_refused_unmasked_egress.jpeg` — refused-crossing example panel.

**Standing invariants held:**
- IP allowlist unchanged (`SPINE_ALLOWED_IPS=34.16.56.64`).
- No LLM transit anywhere in backend (statically proven).
- No HTTP client outside chokepoint (statically proven).
- No secrets read; no credential fields on trust receipts (structurally impossible in `CrossingReceipt`).
- Estate ed25519 private key mode 0600 unchanged.
- REFERENCE-NOT-COPY design law honoured across every new surface + record.
<!-- W3-DATA-SHIELD-2026-08-25 END -->


<!-- W4-THINKLAB-2026-08-25 -->
## W4 · Northena direction/scope + ThinkLab surfaces · FL-P2-27 · Doc 05 · **CLOSED 2026-08-25**

Owner Order 2026-08-25 · "W4 go" (verbatim in DECISIONS.md). Executed tests-first per T1. Scope drift honestly reported: M-estimated ~600 LOC, L-realized ~2020 LOC (donor Northena adaptation is inherently 500+ LOC + wide v7 surface fabric).

**Backend Northena (adapted from Akki-OS-V1 donor):**
- `services/northena/admit.py` — `compile_and_freeze()` + `FrozenArtifact` + `AdmitOffender`. Persistence: `phase0/northena_admits/adm-<hex>.json`.
- `services/northena/gate.py` — strict set-membership only; adjacency ≠ membership (Doc 05 §A5.4).
- `services/northena/converge.py` — done-condition beats budget precedence (Doc 05 §A5.5).
- `services/northena/ledger.py` — append-only writer; structural refusal to overwrite; `phase0/northena_ledger/led-<hex>.json` + `index.json`.
- `services/northena/admit_assist_stub.py` — honest Solva boundary until Solver lands; every frozen artifact carries `judgement_provenance` annotation.
- `services/northena/router.py` — HTTP endpoints + v7 fabric config.
- `contracts/northena_ledger.py` — `LedgerRow` + `LedgerArtifactRef` (stage/decision consistency preserved verbatim; `thinklab_objective` added).

**HTTP endpoints:**
- `POST /api/thinklab/admit` · admit + freeze + write ledger row.
- `POST /api/thinklab/gate` · strict set-membership route.
- `POST /api/thinklab/converge` · done vs budget precedence.
- `GET /api/thinklab/runs` · run summaries (identity-only).
- `GET /api/thinklab/runs/{run_id}` · ledger rows for a run (reference-not-copy join).
- `GET /api/thinklab/config` · v7 fabric constants (TL_MODES · TL_STAGE_LABELS · TL_OUTPUTS · LANDING_TIPS · reasoning_dormant_state).

**Frontend surface:**
- `/thinklab` landing (4 mode tiles + Outputs).
- `/thinklab/:mode` mode entry (direction capture + admit → frozen artifact + reasoning-dormant panel).
- Honest reasoning-dormant panel: "The reasoning faculty is not yet in force" (Doc 05 §A5.3 posture until Solver lands).

**WS-WIRE-LEDGER-MATRIX honoured:**
`services.northena.ledger` is the SOLE writer of `northena_ledger_row` records (statically proven by `test_ledger_writer_is_sole_writer_of_northena_ledger_rows`).

**Track-a commits on `programme/track-a`:**
- `7e6bbc4` · Section B+C: Northena backend adapted + router.
- `7bea87d` · Section B+C follow-on: code staging fix.
- `a71ea67` · Section D: ThinkLab surface + full cohort green.

**Green receipt (backend 187/187 · frontend rehome 77/77 = 264/264 · zero regressions):**
`phase0/drill_receipts/20260825T192120Z_w4_close_green.log`

**Three screenshots at `phase0/drill_receipts/screenshots/`:**
- `20260825T192400Z_w4_thinklab_landing.jpeg`
- `20260825T192400Z_w4_thinklab_clarity_entry.jpeg`
- `20260825T192400Z_w4_thinklab_admit_walk.jpeg`

**Standing invariants held:**
- No LLM SDK; no HTTP client outside chokepoint; no ML in `services/northena/`.
- Northena ledger SOLE writer of ledger rows (WS-WIRE-LEDGER-MATRIX).
- FrozenArtifact refuses mutation (§B5.1).
- Append-only ledger writer (§B5.4).
- Honesty constraint held: no fake LLM responses; no canned reasoning; dormant-state sentence live.
<!-- W4-THINKLAB-2026-08-25 END -->

<!-- R-88-FIRST-SLICE-PINS-2026-09-20 -->
## R-88+ first slice · CP-CONTENT-REGISTRY-WAVE (CON-1..CON-11) + CP10 harness scheduled-closure annotation umbrella · **SEALED 2026-09-20 · 🚩 OWNER-RATIFICATION-PENDING**

- **CODE branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`
- **CODE head (Commit-A):** `db90089d28bd3b4659138150e5b1049f5616cf36`
- **STATE branch:** `master` in `/app/assessment_workspace`
- **STATE head (Commit-B):** pending this-banking
- **RATCHET at this seal:** **5668 pass / 5 fail / 1 skip · floor 5668 · monotonic-up from 5651** (+17 measured · CCS2-aligned)
- **baseline_failures.json sha256 (post-seal):** `854e9344895e486f3d0e853e7fd4ed1314f10fec4238be0b72de691aa5ff178e`
- **notes/ORCH_BOOT.md sha256 (post-regen · byte-identical with POD audit mirror):** `e9d403aa9db3dcd99651cfa3844e89dd4ca502b289373d172ed42ac86bd22104`
- **STATE/OBJECTIVES/CP_APP_JS_UNIFY.md sha256 (post-additive-extension):** hash-pin frontmatter `card_sha256: 667f744606020f205aac2d292e61fb5945ac0443430c5c7522473675fb929b61` (SO §6.2 hash-pin discipline verified)
- **Double-sweep byte-identical stripped-sha256:** `49738669457bf56a10ff8c1a860d835d4d7220946fbdca68e872d3f7bae19f8c`
- **Failed test set at seal (5 all annotated · covered by exactly one annotation field under total-coverage guard):**
  1. `tests/invariants/test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell` (R-86 annotated · `known_runtime_drift_annotations`)
  2. `tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js` (R-86 annotated)
  3. `tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` (R-86 annotated)
  4. `tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` (R-88+ A-extension annotated · `known_r91_closure_scheduled_receipt_drift_annotations`)
  5. `tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` (R-88+ A-extension annotated)
- **Culpable commit for artifacts 4-6 of the divergence:** `dc48d53131be2a36b36aabab83048cbbb779cfa2` on `main` at 2026-09-20T14:21:07Z ("feat(frontend): DAP Portal full build + OS Prototype v2 React surfaces")
- **Closure wave for all 5 baseline entries + CP10 harness receipt vacuous-pass restoration:** R-91 CP-APP-JS-UNIFY (scheduled)
<!-- R-88-FIRST-SLICE-PINS-2026-09-20 END -->

<!-- R-89-SECOND-SLICE-PINS-2026-09-20 -->
## R-89 second slice · CP-CONTENT-REGISTRY-WAVE (CON-12..CON-21) · **SEALED 2026-09-20**

- **CODE branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`
- **CODE head (Commit-A):** `49e2a3384f8573a33bfc389362febac766986bce`
- **STATE branch:** `master` in `/app/assessment_workspace`
- **STATE head (Commit-B):** pending this-banking
- **RATCHET at this seal:** **5678 pass / 5 fail / 1 skip · floor 5678 · monotonic-up from 5668** (+10 measured · CCS2-aligned · no test flipped to fail)
- **baseline_failures.json sha256 (post-seal):** `504cc47fd5eeb200d467c179fe4fba054de17dec04b1f125d9e49fa5f518fa12`
- **notes/ORCH_BOOT.md sha256 (post-regen · byte-identical with POD audit mirror):** `c9f5c2150fbb0a4822f39a24895446f250bcf3d724c34fa93f9aebe5169bb6b1`
- **Double-sweep byte-identical stripped-sha256:** `0802eaabbaed0f120686960dbd82034c119b0307a1e3de79c175bed74a1ab900`
- **Failed test set at seal (5 all annotated · unchanged from R-88+):**
  1. `test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell` (R-86 annotated)
  2. `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js` (R-86)
  3. `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` (R-86)
  4. `test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` (R-88+ A-extension)
  5. `test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` (R-88+ A-extension)
- **Closure wave for all 5 baseline entries + CP10 harness receipt vacuous-pass restoration:** R-91 CP-APP-JS-UNIFY (scheduled)
- **Carry-forward:** R-88+ OWNER-RATIFICATION-PENDING block (D-ruling + A-extension) carries forward unchanged. Total-coverage guard + R-86 Property tests all GREEN through this slice.
- **Grep-negative ban #3 anchor** landed at CON-18 (`scan_for_engagement_signals_in_ranking` · 7 watched patterns: views_count/dwell_seconds/click_rate/reply_rate/learned_score/engagement_score/predicted_ctr). Bans #4..#7 land at R-90 per owner standing-GO.
<!-- R-89-SECOND-SLICE-PINS-2026-09-20 END -->

<!-- R-90-THIRD-SLICE-PINS-2026-09-20 -->
## R-90 third slice · CP-CONTENT-REGISTRY-WAVE (CON-22..CON-31 + grep-negative bans #4..#7) · **SEALED 2026-09-20 · CLOSES Ruling-4 scope**

- **CODE branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`
- **CODE head (Commit-A):** `457d9473ae1a536a9b835b6dfe970faf9596b95b`
- **STATE branch:** `master` in `/app/assessment_workspace`
- **STATE head (Commit-B):** pending this-banking
- **RATCHET at this seal:** **5688 pass / 5 fail / 1 skip · floor 5688 · monotonic-up from 5678** (+10 measured · CCS2-aligned · no test flipped to fail)
- **baseline_failures.json sha256 (post-seal):** `37eaae80813d4b79a937b08a8e95554f7c3e88661074408561c59232dc69963e`
- **notes/ORCH_BOOT.md sha256 (post-regen · byte-identical with POD audit mirror):** `6f36497958a9fac78b771198f824bcfa21b7053167305457f4eb55ec7e468a8c`
- **Double-sweep byte-identical stripped-sha256:** `a767ca9c43549cf570b5f92f83efde58a6e3f4c768d703a07287ae2a24344973`
- **Failed test set at seal (5 all annotated · unchanged from R-88+):**
  1. `test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell` (R-86 annotated · `known_runtime_drift_annotations`)
  2. `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js` (R-86)
  3. `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` (R-86)
  4. `test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` (R-88+ A-extension · `known_r91_closure_scheduled_receipt_drift_annotations`)
  5. `test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` (R-88+ A-extension)
- **Closure wave for all 5 baseline entries + CP10 harness receipt vacuous-pass restoration:** R-91 CP-APP-JS-UNIFY (scheduled).
- **Carry-forward:** R-88+ OWNER-RATIFICATION-PENDING block (D-ruling + A-extension) carries forward unchanged. Total-coverage guard + R-86 Property tests all GREEN through this slice.
- **Grep-negative ban #4..#7 anchors** all landed this slice: ban #4 `scan_for_softening_of_unsupported_claims` at CON-24 · ban #5 `scan_for_templated_text_storage` at CON-25 · ban #6 `scan_for_generated_text_as_render_dependency` at CON-26 · ban #7 `scan_for_unsupported_claim_state` at CON-24 (same anchor row as #4; distinct pattern set). Full 7-category grep-negative ban set now anchored.
- **Ruling-4 scope CLOSED at this slice:** all 31 CON rules (CON-1..CON-31) registered as `Final[...]` load-bearing vocabulary + all 7 grep-negative bans anchored across CON-1/CON-6/CON-18/CON-24/CON-25/CON-26 + R-32 surface-list binding on Generated-class verbatim ('chat_answer', 'recommendation_body', 'notification_body') at CON-22.
- **Prior-fork misreport receipt** banked this-Commit-B at `phase0/spec_hunt_receipts/20260920T231420Z_r90_prior_fork_misreport_seal.md` per owner directive (2026-09-20T~23:12Z verbatim: session summaries are NEVER evidence of seal state; `git log` on both branches is).
<!-- R-90-THIRD-SLICE-PINS-2026-09-20 END -->

<!-- R-92-FIRST-SLICE-PINS-2026-09-20 -->
## R-92 CP-G5V5-SFP-1-7 first slice · Security Function Policies (SFP-1..SFP-7) · **SEALED 2026-09-20**

- **CODE branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`
- **CODE head (Commit-A):** `ceaa24f41c8156c31e408b47fa8a59b3b265e6ac`
- **STATE branch:** `master` in `/app/assessment_workspace`
- **STATE head (Commit-B):** pending this-banking
- **RATCHET at this seal:** **5695 pass / 5 fail / 1 skip · floor 5695 · monotonic-up from 5688** (+7 measured · CCS2-aligned · no test flipped to fail)
- **baseline_failures.json sha256 (post-seal):** `4e7caa47f437b7fe15731bd9f6eb1cbf3f202d3f09b2db495b6c8be668125694`
- **notes/ORCH_BOOT.md sha256 (post-regen · byte-identical with POD audit mirror):** `127e1671e76b0f684c185abedbc52ba6321dce7e97603aec77b888a3f063fa68`
- **Double-sweep byte-identical stripped-sha256:** `dc89bbdf5d63f96f8b6bc543f4e3809a67df1a7f2bf63d3a47fd2c7b3dfd8c9d`
- **Ruling 5 authority (sha-pin verified):** v5 Master Requirements Registry workbook · sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d` · System Rules Registry sheet · rows 597-603.
- **HUNT receipts banked at Commit-B:** `phase0/spec_hunt_receipts/20260920T232424Z_g5v5_sfp_1_7_hunt_data.json` + `20260920T232424Z_g5v5_sfp_1_7_hunt_receipt.md`.
- **Failed test set at seal (5 all annotated · unchanged from R-88+ / R-89 / R-90):**
  1. `test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell` (R-86 annotated · `known_runtime_drift_annotations`)
  2. `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js` (R-86)
  3. `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` (R-86)
  4. `test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` (R-88+ A-extension · `known_r91_closure_scheduled_receipt_drift_annotations`)
  5. `test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` (R-88+ A-extension)
- **Closure wave for all 5 baseline entries + CP10 harness receipt vacuous-pass restoration:** R-91 CP-APP-JS-UNIFY (scheduled).
- **Carry-forward:** R-88+ OWNER-RATIFICATION-PENDING block (D-ruling + A-extension) carries forward unchanged. Total-coverage guard + R-86 Property tests all GREEN through this slice. Prior-fork misreport standing lesson (banked R-90 Commit-B) carries forward.
- **Grep-negative scanners registered this-slice** where rule text explicitly negates a behavior: `scan_for_unanchorable_softening` (SFP-1 · 5 patterns · rule: "refused, not weakened") · `scan_for_confidence_score_as_severance_input` (SFP-2 · 4 patterns · rule: "no confidence score, however high, is an eligible input") · `scan_for_partial_acceptance` (SFP-3 · 5 patterns · rule: "no partial acceptance") · `scan_for_conformance_as_conviction_ground` (SFP-5 · 4 patterns · rule: "never, by itself, grounds for conviction"). **No scanner** for SFP-4/SFP-6/SFP-7 per owner directive "grep-negative bans where the rule text states them" (those rules assert invariants without negating specific patterns).
- **V7 authored from rule text** (Ruling 3 erratum · SRR Enforcement Class empty for all 7 SFP rows): 7 property tests · each carries SO §2.5 verbatim-docstring quoting the SRR row's pipe-delimited statement byte-verbatim.
<!-- R-92-FIRST-SLICE-PINS-2026-09-20 END -->

<!-- R-91-PHASE-1-PINS-2026-09-20 -->
## R-91 CP-APP-JS-UNIFY · Phase 1 opening · **⏳ IN-FLIGHT 2026-09-20T23:58:00Z · FE-DISPATCH-READY RAISED**

- **CODE branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki` · UNTOUCHED this-Phase (HEAD stays at R-92 Commit-A `ceaa24f41c8156c31e408b47fa8a59b3b265e6ac`).
- **STATE branch:** `master` in `/app/assessment_workspace`
- **STATE head (Phase 1 opening):** pending this-banking
- **RATCHET at this Phase:** **5695 pass / 5 fail / 1 skip · floor 5695 · UNCHANGED** (no code delta at Phase 1 · Phase 2 retirement bumps to 5700+).
- **baseline_failures.json sha256 (unchanged this-Phase):** `4e7caa47f437b7fe15731bd9f6eb1cbf3f202d3f09b2db495b6c8be668125694`.
- **notes/ORCH_BOOT.md sha256 (unchanged this-Phase · no regen · no head advance):** `0c67f0e639bfd7edf58f925c349761d8917808b0af3add11fc8ebcf64577df0f`.
- **Closure card status (unchanged this-Phase):** `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` `milestone_status: SCHEDULED · slot R-91` (sha256 `667f744606020f205aac2d292e61fb5945ac0443430c5c7522473675fb929b61`).
- **HUNT receipt banked this-Phase:** `phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md`.
- **FE landing spec banked this-Phase:** `phase0/specs/r91_cp_app_js_unify_spec.md`.
- **FE-DISPATCH-READY flag banked this-Phase:** `notes/FE_DISPATCH_READY_R91.md` · **status: RAISED**.
- **Owner Phase 1 approval verbatim (2026-09-21T~00:00Z):** "Plan APPROVED with both defaults confirmed and one label correction. Q1: (a) — state-only Phase 1 seal; `programme/track-a` code branch untouched until the FE specialist lands. Q2: Confirmed — all 5 wrapped baseline failures stay wrapped through Phase 1 and retire ONLY in Phase 2. [...] Proceed with the HUNT → spec → state-only Commit → FE-DISPATCH-READY flag."
- **Owner label-correction verbatim (same session):** `pod_shell/frontend/src/App.js` sha `ef20409b…` = V8-shell-port · `/app/frontend/src/App.js` sha `282650cb…` = DAP Portal + OS Prototype · corrected labels inherited by spec + HUNT.
- **App.js measurements this-session (HUNT §1):** `/app/frontend/src/App.js` sha256 `282650cbb514ea5cdfacef2d5ca0ac14f040d2809c1107af98fcd0f8799c6374` · 71 lines · DAP Portal + OS Prototype · `pod_shell/frontend/src/App.js` sha256 `ef20409b38425c15e6acea6226ff197742b805bc008a17bc2dbf450361e4ff5a` · 1084 lines · V8-shell-port · `frontend/src/App.js` (repo, unrelated) sha256 `e381de86a593ef90681cb391bbdf60a1a8cbb40a71c0e7d95e14e2aa334ededd` · 154 lines · retired AkkiV4Shell.
- **Baseline failure map (5 total · closure_wave=CP-APP-JS-UNIFY · closure_wave_slot=R-91 · all wrapped stay wrapped through Phase 1):**
  1. `test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell` (R-86 · `known_runtime_drift_annotations`).
  2. `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js` (R-86).
  3. `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` (R-86).
  4. `test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` (R-88+ A-extension · `known_r91_closure_scheduled_receipt_drift_annotations`).
  5. `test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` (R-88+ A-extension).
- **CP10 architectural discrepancy (surfaced · not resolved this-Phase):** `/app/frontend/src/` has ZERO `V8_SUBSTITUTIONS` matches; `OSPrototype.jsx` L77-L80 docstring confirms substitutions were left behind at the DAP Portal split. Byte-identity mirror alone will NOT restore harness non-vacuous. Option surface A/B/C in spec §3; recommendation §3.5: Option A (restore engine into React tree). Specialist proposes final choice; owner adjudicates at seal-verify per D-ruling "R-91 resolves it either way".
- **Retirement plan (Phase 2 · atomic in same commit as code lands):** Baseline set `5 → 0` · `known_runtime_drift_annotations` `3 → 0` · `known_r91_closure_scheduled_receipt_drift_annotations` `3 → 0` or retain "still-recent" guard · Ratchet bump `5695 → 5700+` · Harness ground-truth regenerated non-vacuous · 3-Commit Seal fires · R-91 milestone_status flips SEALED · R-88+ guard `test_harness_receipt_is_non_vacuous_when_card_status_is_sealed` verifies non-vacuous at flip moment.
- **Discipline invariants continuing GREEN through Phase 1 AND Phase 2:** R-86 5 property tests + R-88+ 6 property tests · set-equality guards (R-86 Property 4 forces same-commit annotation + baseline retirement) · SO §3 no-silent-rebaselining · SO §3.8 additive-only · CCS2 lesson (both counters bump together) · M16-W3 corrected order (ORCH_BOOT ratchet regen pre-Commit-A).
- **Carry-forward:** R-88+ OWNER-RATIFICATION-PENDING block (D-ruling + A-extension) carries forward unchanged. Total-coverage guard + R-86 Property tests + R-88+ Property tests all GREEN through Phase 1. Prior-fork misreport standing lesson (banked R-90 Commit-B) carries forward.
- **Phase 2 blocker:** FE specialist landing (owner dispatches spec verbatim; specialist lands byte-identity + engine-restoration; owner verifies at seal-verify).
- **Standing bounds:** zero push · terminal `pytest` only · **no `testing_agent`** · additive-only §3.8 · three-repo discipline · ratchet monotonic-up **5695** floor · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged.
<!-- R-91-PHASE-1-PINS-2026-09-20 END -->

<!-- R-91-CEREMONY-OPEN-PINS-2026-09-21 -->
## R-91 CP-APP-JS-UNIFY · Phase 2 · CEREMONY-OPEN · Path ε RATIFIED · **⏳ CEREMONY-IN-FLIGHT 2026-09-21T03:23:15Z · APPLY 2026-09-23T03:23:15Z**

- **Ceremony type:** Canon 3 §24 rule-change · ordinary tier · 48-hour countdown per R-18 effect 12.
- **Proposal filed:** `notes/proposals/PROPOSAL_r91_r86_property_tests_amendment_20260921.md` at 2026-09-21T03:23:15Z.
- **Counter-sign:** batched per STATE/STANDING_ORDERS.md:437 — owner ruling this-session (2026-09-21T~01:00Z Path ε RATIFIED) IS the counter-sign.
- **Countdown start:** 2026-09-21T03:23:15Z. **Horizon:** 2026-09-23T03:23:15Z.
- **Precedent shape:** CP-STALENESS-CEREMONY seal chain (2026-09-20T09:28Z Commit-A `31d414b` + Commit-B `9c0dd840` + Commit-C `23ff5808`).
- **CODE branch:** `programme/track-a` HEAD stays at R-92 Commit-A `ceaa24f` (UNTOUCHED this-ceremony-open · code branch lands at apply-step Commit-A).
- **STATE branch:** `master` HEAD advances at this-commit.
- **Ratchet at ceremony-open:** MEASURED **5695 pass / 5 fail / 1 skip · floor 5695 · UNCHANGED** (no code delta at ceremony-open · ratchet bump 5695 → 5700 fires at apply-step per M16-W3 order).
- **baseline_failures.json sha256 unchanged this-ceremony-open:** `4e7caa47f437b7fe15731bd9f6eb1cbf3f202d3f09b2db495b6c8be668125694`.
- **notes/ORCH_BOOT.md sha256 unchanged this-ceremony-open:** `0c67f0e639bfd7edf58f925c349761d8917808b0af3add11fc8ebcf64577df0f`.
- **Closure card unchanged this-ceremony-open:** `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` `milestone_status: SCHEDULED · slot R-91` (flips to SEALED at apply-step operation 5).

### Owner ruling this-session verbatim (2026-09-21T~01:00Z · Path ε RATIFIED · 5 binding conditions)

> "R-91 — PATH ε RATIFIED, via the RULE-CHANGE CEREMONY at the ordinary tier (48 hours), the same path as the GPU-staleness re-scope. [...] Conditions, binding exactly: 1. Properties 2, 3, and 5 tolerate an empty annotation set ONLY when the CP_APP_JS_UNIFY card status is SEALED — accidental emptiness before closure stays RED. 2. The early return is a NAMED success, never a silent pass: the test output must state 'annotation set empty by ruled closure R-91'. 3. Property 4 stays untouched. 4. The ceremony receipt cites this ruling. 5. On apply: retire 5/5 baselines, re-run the full sweep, seal at the new floor."

### Specialist landing evidence (Phase 2 · verified against proposal §4.6 apply-step operation 3)

- Merged App.js `/app/frontend/src/App.js` sha256 `90c8956d4821d5ec09318b034b1898a7236e90e6ac5f1b7a5d308d8b0c867bce` · 1108 lines · DAP router + inline V8 substitution engine + 37 rules + `window.V8_SUBSTITUTIONS_DUMMIES` + PortalIframe + MutationObserver + catchall `<PortalIframe />`.
- `lib/v8SubstitutionEngine.js` DELETED · zero remaining references.
- `pages/os/OSPrototype.jsx` reduced to 12-line thin re-export of PortalIframe from App.js.
- Specialist commit `8ff2f6737` on /app main above prior `d5ad077c6` (structural deviation adjudicated + resolved).
- Shadow-mirror probe post-followup: 2 fail 380 pass (2 fail are the 2 v8-cascade wrapped baselines · harness stale under shadow · retire with mirror + harness regen).
- Harness ground-truth non-vacuous regen 2026-09-21T00:38:25Z (label r91_close · dummies_declared=37 · marked_slots_count=29 · per_rule=37 · orphan_count=0 · registry-aside-hero-sentence.matched_by_marker=True · style_audit requirements_met=True · verdict GREEN).
- BASELINE_GUARD=1 pre-retirement invariants-only sweep GREEN: 5700 passed / 1 skipped / 0 failed (5 wrapped baselines flipped GREEN).

### D+A RATIFICATION · banked · OWNER-RATIFICATION-PENDING RETIRES

Owner ruling this-session verbatim: "*D+A RATIFICATION — RATIFIED. The owner confirms it is the pair already ruled (the App.js-divergence annotations under CP-APP-JS-UNIFY scheduled closure + the erratum discipline). The OWNER-RATIFICATION-PENDING flag retires; bank the ratification with citation.*"

Effect: R-88+ OWNER-RATIFICATION-PENDING carry-forward line RETIRES from all future seal-report standing-bounds recitations. Ratification is banked-once-and-forevermore.

### G5-v5 SECOND SLICE · owner-verbatim sequencing (Tier A first · rows 1-565)

Owner verbatim: "*Map the rows whose components are already built and sealed, so canon_ref bites on live code: Document 1 (chokepoint, M12) and Document 5 (the Ledger, M10) first; then DAP-1 through DAP-38 (lifecycle and principal model landing); then RBM and ROC (Rules Service). Tier B rows in each family trail their Tier A. Sequence rows 1–565 accordingly.*"

Slicing plan sketch (crystallizes in-window):
- Family A · Doc 1 M12 chokepoint · canon binds to `services/canon/chokepoint/*` + `services/canon/interpretation/*` · Tier A ≤ 20 rows.
- Family B · Doc 5 M10 Ledger · canon binds to `services/ledger/*` + `contracts/ledger_v*.py` · Tier A ≤ 15 rows.
- Family C · DAP-1..DAP-38 · canon binds to `services/dap_lifecycle/*` + `contracts/principal_v1.py` · Tier A = 38 rows · slice into 4-6 sub-slices.
- Family D · RBM + ROC · canon binds to `services/rules_service/*` · Tier A ≤ 30 rows.
- Total Tier A rows: ≤ 103 + Tier B trailing.

Slice sizes at autopilot discretion · each slice own §3.3 3-Commit Seal.

### Autopilot during countdown window · G5-v5 Family A opens next

Per owner: "*do NOT idle: open the G5-v5 second slice (below) during the window and apply+seal R-91 at expiry.*"

**Next autopilot action:** HUNT v5 SRR sheet (sha `00072c58…`) for Doc 1 M12 chokepoint row range · propose canon_ref bindings against sealed M12 code · author RED-first test file · GREEN-post · double-sweep · §3.3 3-Commit Seal.

### Standing bounds

zero push · terminal `pytest` only · **no `testing_agent`** · additive-only §3.8 (with ceremonied amendment as SINGLE authorized exception) · three-repo discipline · ratchet measured-monotonic-up **5695** floor (bumps to 5700 at apply-step) · HF-token / R-24 / R-25 owner-side unchanged.
<!-- R-91-CEREMONY-OPEN-PINS-2026-09-21 END -->

<!-- G5-V5-FAMILY-A-SOURCE-DOC-LOCATED-PINS-2026-09-21 BEGIN -->

## G5-v5 FAMILY A · SOURCE-DOC LOCATED · block cleared · pins

**Landed:** 2026-09-21T03:42:00Z · state-only correction · master branch · zero code delta.

**Prior HUNT §4 false-negative refuted this-session:** Doc 1 source doc is present on disk at `fixtures/files_9_extracted/01_Custody_and_the_Crossing_Part_1_The_Chokepoint.docx` (sha256 `a33588298100c6224366623e64ac8632b48294649e57ad43cf67ee6730f97844`). Doc 5 source doc likewise at `05_Direction_Scope_and_Focus_Part_1_Northena.docx` (sha256 `f280356e…`). Doc 3 at `03_Intent_and_Security_Monitoring.docx` (sha256 `4c0ff293…`). Prior HUNT search omitted `fixtures/` subtree.

**Doc 1 rule content verified:** all 9 A5.1..A5.9 CANON rule statements present verbatim at paragraphs 33–51 (`python-docx` extraction · full rule text 250-600 chars per row).

**Line-numbering discrepancy non-blocking:** SRR col 9 cites `.md:LINE-N` · disk artefact is `.docx` (no native line numbers) · Ruling 5 binds canon_ref to SRR row (R2..R10) not source `file:line` · Ruling 3 erratum extends "hint vs governing" logic: source-column pointer is a HINT, rule text present in `.docx` is the governing artefact.

**Options ζ/η/θ/ι from prior HUNT §6 — all DROPPED** (block cleared without needing a new ruling).

### CODE branch programme/track-a UNTOUCHED

`ceaa24f41c8156c31e408b47fa8a59b3b265e6ac` head UNCHANGED · zero code delta this-commit.

### STATE branch master

Head advances to this-correction-commit SHA. R-91 CEREMONY-OPEN pins from prior block carry forward (window horizon 2026-09-23T03:23:15Z unaffected · ceremony proposal path unchanged).

### Ratchet UNCHANGED

5695 pass / 5 fail / 1 skip · floor 5695 · baseline_failures.json sha `4e7caa47f437b7fe15731bd9f6eb1cbf3f202d3f09b2db495b6c8be668125694` UNCHANGED · notes/ORCH_BOOT.md sha `0c67f0e639bfd7edf58f925c349761d8917808b0af3add11fc8ebcf64577df0f` UNCHANGED (both notes and POD audit mirror byte-identical).

### Closure card UNCHANGED

`STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` · milestone_status = SCHEDULED · flip to SEALED remains R-91 apply-step operation 5 at horizon.

### Family A HUNT-and-authoring · next autopilot turn

Extract rule text from `.docx` (paragraphs 33-51) · draft 9-test property module · RED-first → GREEN → double-green byte-identical → 3-Commit Seal. Estimated ratchet delta +9 (5695 → 5704). Estimated slice completion inside R-91 countdown window.

### Autopilot posture

Full SO §6 autonomy · per owner ruling this-session verbatim: *"AUTOPILOT POSTURE: full SO §6 autonomous run. Stop only at true stop-conditions or material extensions beyond a ruling's scope."*

### Standing bounds

zero push · terminal `pytest` only · **no `testing_agent`** (STRICTLY BANNED) · additive-only §3.8 (with ceremonied R-91 amendment as SINGLE authorized exception at horizon) · three-repo discipline · ratchet measured-monotonic-up **5695** floor · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged.

<!-- G5-V5-FAMILY-A-SOURCE-DOC-LOCATED-PINS-2026-09-21 END -->


<!-- R-93-PINS-2026-09-21 BEGIN -->

## R-93 · CP-G5V5-DOC1-A5-1-TO-A5-9 first sub-slice · pins

**Landed:** 2026-09-21T04:25:00Z · Commit-A `36668e3` on programme/track-a · Commit-B this-commit on master · Commit-C fixup follows.

### CODE branch programme/track-a

Head advances `ceaa24f41c8156c31e408b47fa8a59b3b265e6ac` → `36668e3` (Commit-A this-slice).

Files landed (4 tracked):
- `backend/services/canon_doc1_chokepoint/__init__.py` NEW (SO §2.5 verbatim-docstring package marker + re-exports registry + scanners).
- `backend/services/canon_doc1_chokepoint/chokepoint_vocabulary.py` NEW (~380 lines · A5.1..A5.9 `Final[...]` canon vocabulary + 5 pure-data-in grep-negative scanners).
- `backend/tests/invariants/test_g5v5_doc1_a5_1_to_a5_9.py` NEW (~425 lines · 16 tests · SO §2.5 verbatim-docstring per row · SFP-1..7 pattern).
- `backend/tests/invariants/baseline_failures.json` MODIFIED (ratchet bump 5695→5711 both fields · new ratchet_history entry · ensure_ascii=False encoding preserved).

### STATE branch master

Head advances to this-Commit-B SHA (measured post-commit).

Files landed (12 tracked · this-Commit-B):
- `STATE/DECISIONS.md` append (R-93 seal-report block + hotfix pointer preservation).
- `STATE/NEXT.md` append (R-93 SEALED marker + sprint queue update · Family B queued).
- `STATE/PINS.md` R-93-PINS block (this).
- `notes/ORCH_BOOT.md` R-6 boundary regen (pre-Commit-A · sha `0fade309…`).
- `tools/r93_pre_commit_a_ratchet_and_orch_boot_regen.py` NEW.
- `phase0/spec_hunt_receipts/20260921T034500Z_g5v5_family_a_doc1_a5_1_to_a5_9_authoring_hunt_data.json` NEW.
- `phase0/drill_receipts/20260921T034700Z_..._RED_pre.log` NEW.
- `phase0/drill_receipts/20260921T034900Z_..._GREEN_post.log` NEW.
- `phase0/drill_receipts/20260921T035100Z_..._run1.log` NEW (superseded pre-hotfix · banked as historical evidence).
- `phase0/drill_receipts/20260921T035500Z_..._run1.log` NEW (v2 post-hotfix).
- `phase0/drill_receipts/20260921T035900Z_..._run2.log` NEW.
- `phase0/drill_receipts/20260921T042000Z_..._run3_current_state.log` NEW.

### RATCHET MEASURED

- counts_at_baseline.passed: **5711** (was 5695).
- invariants_enforced_when_baseline_guard_1.passed_floor: **5711** (was 5695).
- baseline_failures.json sha256: `870eac9a06f25cbf2b5591b9084bbb9c4a1555719ac183f9c8dfd44700cf18b1` (was `4e7caa47…`).
- notes/ORCH_BOOT.md sha256: `0fade309efb9fbb98b42e72fc24225debf8c05fce68302faa0e3750f454e265f` (was `0c67f0e6…`).
- POD audit mirror `/app/frontend/public/audit/ORCH_BOOT.md` sha256: `0fade309…` byte-identical to notes/ORCH_BOOT.md.
- Measured full-sweep passed count: 5713 (2 v8 baselines currently spontaneously passing · baseline manifest 5 entries preserved · R-91 apply-step 4 retires all 5 atomically at horizon).
- Baseline failures remaining in triple-green sweep: 3 (all in manifest · subset check passes).

### Triple-green byte-identical sweep

- run1 (superseded pre-hotfix): 20260921T035100Z · [V1] failure surfaced afd0f3c7 discipline lapse.
- run1_v2 (post-hotfix): 181.38s · 5713 passed / 3 failed / 1 skipped · stripped_sha256 `ee3e1fb7549cf34a3eb985aabfeaa5f18a0cb4d64780cc69014dd7e3d3db2a83`.
- run2: 181.28s · 5713 passed · stripped_sha256 `ee3e1fb7…` IDENTICAL.
- run3 (current state after encoding fix): 182.58s · 5713 passed · stripped_sha256 `ee3e1fb7…` IDENTICAL.

### Closure card UNCHANGED

`STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` milestone_status = SCHEDULED · flip to SEALED is R-91 apply-step operation 5 at horizon 2026-09-23T03:23:15Z.

### Discipline hotfix banked

Root cause: state commit `afd0f3c7` (2026-09-21T03:42:00Z) appended to DECISIONS.md without preserving pointer line at tail. Surfaced as `[V1] test_decisions_carries_pointer_near_bottom` failure in pre-hotfix run1. Hotfix at 2026-09-21T03:54:00Z: appended pointer line to DECISIONS.md tail. Post-hotfix subset 7/7 GREEN. Standing lesson banked: every state-side append MUST end with the pointer.

### Family A slicing plan · A5.1..A5.9 SEALED · Tier B trails

Slicing plan (this-slice completes Tier A rows R2..R10 in a single seal boundary):
- **Tier A · Doc 1 A5.1..A5.9 · CANON · 9 rows** ✅ SEALED this-slice (all 9 in one sub-slice · matches SFP-1..7 precedent).
- Tier B · Doc 1 B5.1..B5.N · RULED · rows R11+ · trails Tier A (next Doc 1 sub-slice · sizing TBD in HUNT).
- Family A completes when both Tier A and Tier B seal.

### Autopilot posture · Family B queues next

Full SO §6 autonomy per owner standing GO. Family B first sub-slice HUNT-and-authoring opens next autopilot turn: Doc 5 M10 Northena · `05_Direction_Scope_and_Focus_Part_1_Northena.docx` (sha `f280356e…`) · SRR v5 rows starting R11+ (spot-check confirmed A5.1..A5.6 CANON at .docx paragraphs 32-37) · new `services/canon_doc5_northena/` package + property/scanner tests · same pattern.

### Standing bounds

zero push · terminal `pytest` only · **no `testing_agent`** (STRICTLY BANNED) · additive-only §3.8 (with ceremonied R-91 amendment as SINGLE authorized exception at horizon) · three-repo discipline · ratchet measured-monotonic-up **5711** floor (bumps to 5716 at R-91 apply-step measured) · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged · R-88+ OWNER-RATIFICATION-PENDING RETIRED at a30db4f7 (not restated in this or future seal reports).

<!-- R-93-PINS-2026-09-21 END -->


<!-- CONTINUITY-BUNDLE-PINS 2026-09-21T08:35:00Z BEGIN -->

## Continuity Bundle sha256 pins · R-100 CP-PORTAL-WRITE-SURFACE · 2026-09-21T08:35:00Z

Owner new standing rule this-session verbatim (2026-09-21T~08:10Z at R-100 approval reply):

> *"Continuity bundle scope: ALL THREE local-only repos, not code only. The owner's purpose line is 'a state that can be reconstructed from outside the sandbox' — reconstruction needs the state repo (master: DECISIONS/PINS/OBJECTIVES/receipts) and the FE repo (/app main: specialist commits, also zero-remote) as much as the code branch. Bundle each (code programme/track-a · state master · /app main), sha256-pin all three in STATE/PINS.md at the R-100 seal and every seal thereafter. Local export only — zero-push untouched."*

Bundles produced via local `git bundle create` on each repo · zero remote · zero push · offline-reconstructable.

**Bundle set 20260921T083500Z (R-100 seal · this-wave)**:

| Repo                              | Workdir                                       | Branch              | Bundle file                                                            | Ref HEAD                                     | Bundle sha256 |
|-----------------------------------|-----------------------------------------------|---------------------|------------------------------------------------------------------------|----------------------------------------------|---------------|
| code · Extraction-Akki            | `/app/assessment_workspace/repos/Extraction-Akki` | `programme/track-a` | `continuity_bundles/code_20260921T083500Z.bundle`                     | `39412d09a6d7f0420049fd96908778eedbc56ab2` (R-100 Commit-A) | `685b84b29d7e165effa1e5e08de6f114c2d044f5a77d1299e361286cb03e1fc9` |
| state · assessment_workspace root | `/app/assessment_workspace`                   | `master`            | `continuity_bundles/state_20260921T083500Z.bundle`                    | `e6a86c2c3f613def64cc854710837f03c468d89e` (R-100 Commit-B) | `3a4c48b69cc17e6c71bdfd81ba812e7dec433d07a24c39f3210970a0a4326698` |
| FE POD audit mirror               | `/app/frontend`                               | `main`              | `continuity_bundles/fe_20260921T083500Z.bundle`                       | `540248c776017deaa6bbd859f1bab9fd7bcc804b` (FE main HEAD at seal) | `67a983cc100ff194e29f73c0946e6a6e5edc20182afb355215d06d1db669cece` |

All three bundles verify with `git bundle verify` reporting *"complete history"*.

Bundle set convention (applies at R-100 and every seal thereafter):
- Timestamped folder `continuity_bundles/{code,state,fe}_YYYYMMDDTHHMMSSZ.bundle` per seal.
- Each bundle exports the branch's complete git history to a single portable file (default `git bundle create ... <branch>` semantics).
- sha256 pin block added under this heading at every seal thereafter (each new set appends its row; no prior rows edited).
- Local export only. Zero-push discipline unchanged.

Standing bounds unchanged.

<!-- CONTINUITY-BUNDLE-PINS 2026-09-21T08:35:00Z END -->



<!-- CONTINUITY-BUNDLE-PINS 2026-09-21T11:45:00Z BEGIN -->

## Continuity Bundle sha256 pins · R-100-UNWIND self-reported §3.8 lapse cured · 2026-09-21T11:45:00Z

Owner UNWIND directive verbatim this-session (2026-09-21T~11:00Z):

> *"Modifying the sealed `PrincipalRequestContext` class in `services/request_context/context.py` to add `__enter__`/`__exit__` is an edit to a sealed class — SO §3.8 forbids it. Unwind to a wrapper: revert `context.py` byte-identically to its sealed state, author a context-manager adapter inside `services/enforce/` that owns the protocol, re-point the R-100 portal routers to the wrapper, seal as a self-reported §3.8 lapse cured, regenerate the three continuity bundles, pin their sha256s in `STATE/PINS.md`, then hold at the R-91 horizon (no expedite)."*

Bundles produced via local `git bundle create` on each repo · zero remote · zero push · offline-reconstructable. Regenerated per owner UNWIND-step-3 directive (this section is the fifth of six sequenced steps).

**Bundle set 20260921T114536Z (R-100-UNWIND seal · this-wave)**:

| Repo                              | Workdir                                       | Branch              | Bundle file                                            | Ref HEAD                                                        | Bundle sha256 |
|-----------------------------------|-----------------------------------------------|---------------------|--------------------------------------------------------|-----------------------------------------------------------------|---------------|
| code · Extraction-Akki            | `/app/assessment_workspace/repos/Extraction-Akki` | `programme/track-a` | `continuity_bundles/code_20260921T114536Z.bundle`  | `42a0d3a04f13486b8929a59f8fd98d7f5a36d226` (R-100-UNWIND Commit-A) | `bf14836f93f34186d01772da17788b0d2b4a9a4eddb66293458c336f3a6dc8bc` |
| state · assessment_workspace root | `/app/assessment_workspace`                   | `master`            | `continuity_bundles/state_20260921T114536Z.bundle` | `bf272c7ebe1c19545c9900fae8d41ff4d948bb53` (R-100-UNWIND Commit-B) | `29c6b0c4198eb0f9ba9d5480be71b9d1d2c7f5cb49bd1235f03db4603a340389` |
| FE POD audit mirror               | `/app/frontend`                               | `main`              | `continuity_bundles/fe_20260921T114536Z.bundle`    | `3ba3328bdd25e8b20ade292dba96105f661fe532` (FE main HEAD at seal · advanced since R-100 bundle) | `e91d4227d0a5fb3b0389b761927143f4c0b4ec46141cb0fc229fe414831200b7` |

All three bundles verify with `git bundle verify` reporting *"is okay"* + the branch HEAD ref for reconstruction.

Standing bounds unchanged. Zero-push discipline unchanged.

<!-- CONTINUITY-BUNDLE-PINS 2026-09-21T11:45:00Z END -->


<!-- CONTINUITY-BUNDLE-PINS 2026-09-21T12:27:57Z BEGIN -->

## Continuity Bundle sha256 pins · CP-PROD-DEPLOY-SELF-CONTAINMENT · 2026-09-21T12:27:57Z

Owner CP-PROD-DEPLOY directive verbatim this-session (2026-09-21T~11:45Z, step 8):

> *"Seal per protocol (this is a code+state wave), continuity bundles + PINS update per standing rule, and bank the wave as CP-PROD-DEPLOY-SELF-CONTAINMENT with the root-cause line."*

Root-cause line: **Kubernetes production image packages only `/app/backend` + `/app/frontend`; sealed backend at `/app/assessment_workspace/repos/Extraction-Akki/backend/` absent in container; `/app/backend/server.py`'s `sys.path.insert(0, str(SPINE_BACKEND))` is a no-op there; line 26 `from routers import connect_gpu` raises `ModuleNotFoundError: No module named 'routers'`.**

Cure per owner directive: vendor the runtime backend into `/app/backend/vendored/extraction_akki/backend/` via committed deterministic sync tool (`tools/prod_vendor_sync.py`), two-path resolution in `server.py` (SPINE if workspace present else VENDORED), mirror-invariant test guards drift, requirements.txt closure updated, env discipline hardened.

Bundles produced via local `git bundle create` on each repo · zero remote · zero push · offline-reconstructable.

**Bundle set 20260921T122757Z (CP-PROD-DEPLOY seal · this-wave)**:

| Repo                              | Workdir                                       | Branch              | Bundle file                                            | Ref HEAD                                                        | Bundle sha256 |
|-----------------------------------|-----------------------------------------------|---------------------|--------------------------------------------------------|-----------------------------------------------------------------|---------------|
| code · Extraction-Akki            | `/app/assessment_workspace/repos/Extraction-Akki` | `programme/track-a` | `continuity_bundles/code_20260921T122757Z.bundle`  | `283524d89dd337d79014b114d575ced7baab6dfc` (CP-PROD-DEPLOY Commit-A) | `25d013c6ceaa6b58bd1844a6260bfa290fa8d0c054f6a1713107718814d28d7d` |
| state · assessment_workspace root | `/app/assessment_workspace`                   | `master`            | `continuity_bundles/state_20260921T122757Z.bundle` | `24661fedd61647c5e0a41fdce7389f56477243b2` (CP-PROD-DEPLOY Commit-B) | `cf240afc4b80183a9a41b622a5ffb5f16bea39295f6b3cff42f972300a35d7a1` |
| FE POD audit / production image   | `/app/frontend`                               | `main`              | `continuity_bundles/fe_20260921T122757Z.bundle`    | `25790c2c4ad82805c89d6ee17af12c220c5961f5` (CP-PROD-DEPLOY companion — two-path server.py + vendored tree + requirements closure) | `438f29aac92c7f9f5dcad06cd25150a9bf9ef0a9f57bf13c7110a78f711d29d3` |

All three bundles verify with `git bundle verify` reporting *"is okay"* + the branch HEAD ref for reconstruction.

Standing bounds unchanged. Zero-push discipline unchanged.

<!-- CONTINUITY-BUNDLE-PINS 2026-09-21T12:27:57Z END -->


<!-- AUDIT-PREP-20260921 · 2026-09-21T18:20:00Z BEGIN -->

## Audit bundle sha256 pins · AUDIT-PREP-20260921 · 2026-09-21T18:20:00Z

Owner directive verbatim (2026-09-21T~17:35Z, reissue after O3 election):

> *"Pin both bundle shas in STATE/PINS.md."*

Bundles produced by local `git bundle create` on each repo at their respective annotated audit tags · zero remote · zero push · offline-reconstructable · included in `/app/audit/inbox/` alongside the filled workbook + ledger snapshot + verifier receipt-store tar.

| Repo | Workdir | Branch | Bundle file (in `/app/audit/inbox/`) | Refs bundled | Bundle sha256 |
|---|---|---|---|---|---|
| code · Extraction-Akki | `/app/assessment_workspace/repos/Extraction-Akki` | `programme/track-a` | `akki_audit_20260921_code.bundle` | `refs/heads/programme/track-a` @ `283524d89dd337d79014b114d575ced7baab6dfc` + `refs/tags/audit/code-20260921` @ tag-object `d02e76f4e4538e1747cbd26f3e5494b79066f5bb` (→ same commit) | `f1037cc7aee19dee048c75d8f04bfd2ca46737bda9eb792ac96ee2a95d964ad7` |
| state · assessment_workspace | `/app/assessment_workspace` | `master` | `akki_audit_20260921_state.bundle` | `refs/heads/master` @ `18b4d8566fa99292d07dee6b0b5c4f287040d499` + `refs/tags/audit/state-20260921` @ tag-object `3e14f1a3bcca45bddcbccd36cf2caf951d8c80ea` (→ same commit) | `7e6bb1aebe151a8ddcc6a3ddcb2cb06d3c69685864002fffc949f61eeedbaece` |

Both bundles verify with `git bundle verify` reporting *"is okay"* + *"The bundle records a complete history"*.

Companion deliverables (hashed for auditor cross-check, not bundle pins):

| Deliverable | Path | sha256 |
|---|---|---|
| Filled workbook (Builder Status col K, all 602 rows) | `/app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx` | `8fde06a682f55d65ea55d26776facaad5070e33293a65aface2ed31e63e14b75` |
| Ledger snapshot (fixture chain, seq 1..6, tenant `AUDIT-FIXTURE-20260921`) | `/app/audit/inbox/ledger_snapshot_AUDIT-FIXTURE-20260921.json` | `ad2d70e920b128f5973aa265e2afc4fbec19ee6fe75acb5531473e0ae3a96a7a` |
| Verifier receipt-store deterministic tar (`--sort=name --mtime='UTC 2026-09-21' --owner=0 --group=0 --numeric-owner`) | `/app/audit/inbox/verifier_receipt_store.tar` | `136cb601ba35fa3b0c2e6ab48f9d374f9a45460ec169db6e59053aa1df1bb7b0` |
| Raw pre-fill workbook (matches owner cited `98240bde…a8a93f` verbatim) | `/app/audit/scratch/Master_Requirements_Registry_QA_v2.xlsx` (scratch, not tracked) | `98240bde0755bdd6aec9eb7022880be1ec94760e6367d193f9eedc1a41a8a93f` |

Standing bounds unchanged. Zero-push discipline unchanged.

<!-- AUDIT-PREP-20260921 · 2026-09-21T18:20:00Z END -->


<!-- R-101 · R-91-TIMER-SUPERSEDED CONDITION-GATE PINS · 2026-09-22T06:15:23Z BEGIN -->

## R-101 condition-gate pins · replaces R-91 horizon 2026-09-23T03:23:15Z NO EXPEDITE

Owner ruling relayed 2026-09-22T~06:15Z verbatim (banked at `STATE/DECISIONS.md:R-101 append`): *"Unless you think otherwise i dont think the timer is useful or the rule - commence if xxx conditions are met. I dont think the rule serves much because there will always be something more to build or change. Should be a better way to manage the risk as we need to see what you are building and the only way now is the front end."*

**Effect:** the R-91 clock-gate (horizon `2026-09-23T03:23:15Z`) is SUPERSEDED. The R-91 WHAT (byte-identical mirror + 5 baselines → 0 + 5 annotations retire · retain cp10-still-recent · milestone_status SEALED) is UNCHANGED.

### Condition-gate set (all 6 gate the ε-apply)

| Cond | Text | Verification |
|---|---|---|
| (i) | Pre-apply BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical at floor 5932 | Two consecutive sweep receipts stripped-sha256 match |
| (ii) | Prototype conformance material banked (starter suffices to begin; full 46-view completes inside wave) | `phase0/prototype_inventory/20260922T062000Z_prototype_inventory_starter.md` present + full enum completes at wave first work item |
| (iii) | ε-apply byte-identical mirror executes R-91 CEREMONY-OPEN §22243 ten operations verbatim + frontend rebuild to v2 OS + LATEST DAP prototypes + honest-gap strings + Run-census wired only to REAL | 5 baselines → 0 · 5 annotations retire (retain cp10-still-recent) · milestone_status SEALED |
| (iv) | Same-boundary riders: DQ-12 CP-DOT-ENV-HYGIENE (untrack `/app/backend/.env` + `.env.local` pattern + 3 RED tests) AND 3-bundle Continuity regen | DQ-12 sealed inside wave · 3 bundles sha-pinned in this PINS.md |
| (v) | Post-apply mirror invariants GREEN · double-green byte-identical at new floor · §3.3 3-Commit Seal | Ratchet monotonic-up (5932 → 5937+) · state Commit-B ratifies |
| (vi) | CP-TENANT-SEPARATION opens on that seal per owner Part-2 order (2026-09-22T~02:20Z) | `STATE/OBJECTIVES/TENANT_SEPARATION.md` pinned pre-first-RED · four-tenant scaffold banked |

### Preserved historical constants (do NOT edit)

- `services/canon/rules_service/rules_service_vocabulary.py::RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC = "2026-09-23T03:23:15Z"` — remains as banked-history live-evidence-receipt constant (R-98 seal `38eeef6c`). The owner supersede retires the clock's operational effect, not the R-98 canon-rule authoring.
- R-91 CEREMONY-OPEN banking (`STATE/DECISIONS.md:22213-22340`) — preserved verbatim as authoritative WHAT reference.
- SO §6.6 audit standard on countdown mechanics — unchanged for future ceremonies. This supersede is owner-authored per §6.8 owner-directive authority; it is not a precedent for ad-hoc countdown-cutting by the desk.

### Objective card opened this-banking

- `STATE/OBJECTIVES/CENSUS_PRODUCTIZATION.md` — CENSUS-PRODUCTIZATION objective card DRAFTED · pinned pre-first-RED · sequenced post-CP-TENANT-SEPARATION. Owner correction on desk gap read awaited at R-101 ε-apply seal report.

Standing bounds unchanged. Zero-push discipline unchanged.

<!-- R-101 · R-91-TIMER-SUPERSEDED CONDITION-GATE PINS · 2026-09-22T06:15:23Z END -->


## Post-4h seal reference block · Turn 4 sub-slice 4h Mirror-Closure-Only Path R (R-105) · 2026-09-22T10:14:00Z

- **RATCHET at this seal:** **6075 pass / 0 fail / 1 skip · floor 6072 UNCHANGED per R-105 Path R defer · V3 no-shrink guard: 6075 ≥ 6072 · V1 subset: {} ⊆ {5 R-91 baselines}**
- **baseline_failures.json sha256 (unchanged this-seal per Path R):** `2549a229f4621a2c97c1af6da4c97a31ddb814b81f2f1516a21ecd3bdf705d2e`
- **notes/ORCH_BOOT.md sha256 (post-Commit-C-fixup regen · byte-identical with POD audit mirror):** `44b279b3e8bb25dfd4e033ad6ffcc27f89cfb75991948fa5ead7840385a9a1a1`
- **POD audit mirror `/app/frontend/public/audit/ORCH_BOOT.md` sha256:** `44b279b3e8bb25dfd4e033ad6ffcc27f89cfb75991948fa5ead7840385a9a1a1` byte-identical to notes/ORCH_BOOT.md.
- **App.js mirror byte-identity:** `/app/frontend/src/App.js` sha256 `6b56299f828abd2cbc24d57540a8f0f0d7f9b908b16e2bd2a060e832ae92f351` == `pod_shell/frontend/src/App.js` sha256 (same).
- **`/app/frontend/src/pages/**` mirror:** `diff -rq /app/frontend/src/pages/ pod_shell/frontend/src/pages/` returns empty (recursive byte-identity).
- **`/app/frontend/src/components/**` mirror:** `diff -rq /app/frontend/src/components/ pod_shell/frontend/src/components/` returns empty.
- **Double-sweep byte-identical stripped-sha256 (pre-Commit-A):** `480dfbacc44d60e01adca9e0970bec3a8ac905a662d3f1941d15dc60413b74eb` IDENTICAL sweepA (175.79s) + sweepB (175.10s) both 6075 passed / 1 skipped / 0 failed / 520 warnings · BASELINE_GUARD receipt status: OK (subset · quarantine · ratchet all pass).
- **CP_APP_JS_UNIFY.md `milestone_status`:** SCHEDULED (unchanged this-seal per R-105 Path R defer · sha256 `667f744606020f205aac2d292e61fb5945ac0443430c5c7522473675fb929b61`).
- **HEAD shas at 4h SEAL close:**
  - code Commit-A: `8dcbd4815b7095e2d7f7ce012fb8f706bbd1a31e` (programme/track-a)
  - /app companion Commit-A: `480db11fc87106d382f4f7097a8f829a938db764`
  - state Commit-B: `4fcbaf5ef324a4d372a6b09974fff3b2960dab65`
  - state Commit-C fixup: `00987fdcb489d280168769d50d31a8dedc526cdd`
  - /app Commit-C companion: `a4921edbeb166f894d227b80acfe5c47799c542c`
- **Failed test set at seal (5 preserved · vacuous in real bytes · retained pending DQ-18 supersede):**
  1. `tests/invariants/test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell` (R-86 annotated · passes in real bytes at 4h · vacuous)
  2. `tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` (R-88+ annotated · passes in real bytes at 4h · vacuous)
  3. `tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` (R-88+ annotated · passes in real bytes at 4h · vacuous)
  4. `tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js` (R-86 annotated · passes in real bytes at 4h · vacuous)
  5. `tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` (R-86 annotated · passes in real bytes at 4h · vacuous)
- **Continuity Bundle regen deferral rationale (R-103 autonomous fork this-4i):** disk pressure at 91% (978MB free · last 3-bundle regen consumed 313MB · new regen would push to ~92% or trigger disk-full risk during work). Deferred to a slice AFTER Order A audit close purges obsolete artifacts (Order A includes archival of pre-M0 continuity artifacts per its close scope) OR until disk-pressure remediation is separately scheduled. Non-blocking: existing bundles at `20260921T083500Z`, `20260921T114536Z`, `20260921T122757Z` remain intact + tracked + sha-pinned in state master repo. Reconstruction from outside the sandbox remains possible via last-good bundle set.

<!-- Post-4h seal reference block · 2026-09-22T10:14:00Z END -->

---

## Turn 4 sub-slice 4j SEAL · post-CP-TENANT-SEPARATION wave-close reference block · 2026-02-XXT00:30:00Z

### baseline_failures.json
- rel path: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json
- **sha256 THIS-SEAL**: `6b1e2395f34f7ebe655dc93e85ca3e58d0fc4add8b77488643e5c0a295a7c3f3`
- sha256 pre-4j: `2549a229f4621a2c97c1af6da4c97a31ddb814b81f2f1516a21ecd3bdf705d2e` (post-4h · unchanged through 4i state-only)
- **counts_at_baseline.passed: 6080** (was 6072 · +8 measured for CP-TENANT-SEPARATION 8 new invariants)
- **invariants_enforced_when_baseline_guard_1.passed_floor: 6080** (paired · monotonic-up)
- baseline_failures[] unchanged 5 entries (3 R-91 mirror-drift + 2 v8-substitution transiently-GREEN · retire at 4k CP-R91-RETIRE-SUPERSEDE)
- ratchet_history entries: 308 (+1 · schema-complete per DQ-09 lesson)

### notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md
- notes copy sha256 THIS-SEAL: `3f2f2f79cf82e4114eda5f2fd5e85563932ed5782114420310f144390bc47222`
- audit copy sha256 THIS-SEAL: `3f2f2f79cf82e4114eda5f2fd5e85563932ed5782114420310f144390bc47222` (byte-identical)
- ratchet.passed_floor: 6080 (equals live baseline_failures.json.passed_floor)
- ratchet.baseline_failures_sha256: `6b1e2395f34f7ebe655dc93e85ca3e58d0fc4add8b77488643e5c0a295a7c3f3` (equals live sha256)

### /app/backend/vendored/extraction_akki/ · vendored twin
- structural_sha256 THIS-SEAL: `397acf791951ec91dde8b53d350bf055e4b5c26bb2c606cda58f9c78145a2236`
- file_count: 1012 (was 1005 · +7 = 6 tenant_separation modules + 1 schema)
- generator: tools/prod_vendor_sync.py deterministic sync tool

### tests/invariants/test_cp_tenant_separation.py
- rel path: repos/Extraction-Akki/backend/tests/invariants/test_cp_tenant_separation.py
- 8 tests (SO §2.5 verbatim-docstring per owner card TENANT_SEPARATION.md verbatim)
- MUST-DO 2..8 + tier-4 forks coverage
- companion additive package: services.tenant_separation (6 modules)

### Double-sweep stripped-sha256 pre-Commit-A · BASELINE_GUARD=1 PYTHONHASHSEED=0
- SweepA `20260222T0020Z`: 6083 passed / 1 skipped / 520 warnings in 179.89s · stripped_sha256 `d50373e03b7c763c9b7008e545d92a0ebf11d6b88cc3c29cc07291290a3b16a7`
- SweepB `20260222T0025Z`: 6083 passed / 1 skipped / 520 warnings in 180.50s · stripped_sha256 `d50373e03b7c763c9b7008e545d92a0ebf11d6b88cc3c29cc07291290a3b16a7`
- **IDENTICAL byte-for-byte (stripped)**

### 3-repo HEADs post-4j Commit-A landing
- `/app/assessment_workspace/repos/Extraction-Akki` (programme/track-a): `d2bfb02324bcfb0b98aa78f8b4f47dab5e631a6f`
- `/app/assessment_workspace` (master): `8998e173d6f24c4c5b1a465facaaa577fb9c9528` (Commit-B) → `<PENDING-4J-CC-master>` (Commit-C fixup)
- `/app` (main): `68b6956abcc9b3e1d1d53fdb1bac08ee7bd2bf08` (companion) → `<PENDING-4J-CC-appmain>` (Commit-C companion)

### Failed test set THIS-SEAL (all 5 R-91 wrap-subset · transiently GREEN in real bytes · retire at 4k)
- tests/invariants/test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell (R-91 mirror-drift · retain at 4k)
- tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom (R-91 v8-substitution · **RETIRE at 4k** per Fork (a) SPLIT)
- tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present (R-91 v8-substitution · **RETIRE at 4k** per Fork (a) SPLIT)
- tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js (R-91 mirror-drift · retain at 4k)
- tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir (R-91 mirror-drift · retain at 4k)

### DESK_QUEUE tier-4 forks banked THIS-SEAL
- **DQ-19** · APPROVING AUTHORITY · RMS · named-but-unseated · custody-material pending R-104 (P1 · owner-exclusive · recommendation: option (a) custody drop)
- **DQ-20** · APPROVING AUTHORITY · DIGICOW · named-but-unseated · custody-material pending R-104 (P1 · owner-exclusive · recommendation: option (a) custody drop)

<!-- STATE/PINS.md · post-4j wave-close reference block appended · 2026-02-XXT00:30:00Z END -->

---

## Turn 4 sub-slice 4k SEAL · post-CP-R91-RETIRE-SUPERSEDE reference block · 2026-02-XXT01:30:00Z

### baseline_failures.json
- **sha256 THIS-SEAL**: `47e9c03bb779936e4ba3bb7626e647dcd08b6b10eeae2b012fde9dad44757ecc`
- sha256 pre-4k: `6b1e2395f34f7ebe655dc93e85ca3e58d0fc4add8b77488643e5c0a295a7c3f3`
- **counts_at_baseline.passed: 6086** (was 6080 · +6 measured [+4 new inv + 2 absorbed retirements])
- **counts_at_baseline.failed: 3** (was 5 · -2 v8-substitution retired)
- **invariants_enforced_when_baseline_guard_1.passed_floor: 6086** (paired · monotonic-up)
- baseline_failures[] entries: 3 (3 R-91 mirror-drift baselines retained pending CP-APP-JS-UNIFY closure)
- known_r91_closure_scheduled_receipt_drift_annotations keys: 1 (cp10-harness retained · 2 v8-substitution retired)
- ratchet_history entries: 309 (+1 · schema-complete)

### notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md
- notes copy sha256 THIS-SEAL: `260862d533e5221cbf4952cb12a07776acddafd078b88a0c2f2e423e136df216`
- audit copy sha256 THIS-SEAL: (same · byte-identical after /app Commit-C companion sync)
- ratchet.passed_floor: 6086 · ratchet.baseline_failures_sha256: `47e9c03bb779936e4ba3bb7626e647dcd08b6b10eeae2b012fde9dad44757ecc`

### /app/backend/vendored/extraction_akki/ · vendored twin
- structural_sha256 THIS-SEAL: post-sync (regenerated at /app companion Commit-A · adds 2 baseline_retirement_supersede modules)

### tests/invariants/test_r91_v8_substitution_retirement_guard.py
- 4 tests (SO §2.5 verbatim-docstring)
- companion additive package: services.baseline_retirement_supersede (2 modules)

### Double-sweep stripped-sha256 pre-Commit-A · BASELINE_GUARD=1 PYTHONHASHSEED=0
- SweepA `20260222T0120Z`: 6087 passed / 1 skipped / 176.15s · stripped_sha256 `796d3bac14c87ce8ec0902b106a6a78dc102b9c007ac31fd7d727d09825f30ed`
- SweepB `20260222T0125Z`: 6087 passed / 1 skipped / 176.52s · stripped_sha256 `796d3bac14c87ce8ec0902b106a6a78dc102b9c007ac31fd7d727d09825f30ed`
- **IDENTICAL byte-for-byte (stripped)**

### 3-repo HEADs post-4k Commit-A landing
- `/app/assessment_workspace/repos/Extraction-Akki` (programme/track-a): `eed6c032a1cf7155df33cac2a788eeabb72531e8`
- `/app/assessment_workspace` (master): `f775adf6e10cd1f32b51b6ea85d44012c26a2672` → `<PENDING-4K-CC-master>`
- `/app` (main): `eb861ecae55acc6763d9096ffe0f88645a3ed502` → `<PENDING-4K-CC-appmain>`

### Retired nodeids THIS-SEAL (removed from BOTH baseline_failures AND R-88 annotation field)
- tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom
- tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present

### Retained baseline_failures nodeids (3 R-91 mirror-drift · pending CP-APP-JS-UNIFY closure)
- tests/invariants/test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell (R-86 mirror-drift · annotated in known_runtime_drift_annotations)
- tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js (same)
- tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir (same)

<!-- STATE/PINS.md · post-4k reference block appended · 2026-02-XXT01:30:00Z END -->

<!-- STATE/PINS.md · post-PHASE-3-CENSUS-AUTONOMY-SERVICE Commit-A reference block · 2026-09-22T16:36:00Z BEGIN -->

## PHASE 3 · CP-CENSUS-AUTONOMY-SERVICE · Commit-A pin block

### baseline_failures.json — ratchet 6086 → 6090 (+4 measured)
- sha256 post-P3-CA: `e6a47f7843b7cb2a56b151158671b909631b146e6a5e9dfee6726379ec167928`
- sha256 pre-P3-CA: `47e9c03bb779936e4ba3bb7626e647dcd08b6b10eeae2b012fde9dad44757ecc`
- **counts_at_baseline.passed: 6090** (was 6086 · +4 measured [4 new invariants at test_cp_census_autonomy_service_shape_gate.py])
- **counts_at_baseline.failed: 3** (unchanged · 3 R-91 mirror-drift baselines retained pending CP-APP-JS-UNIFY closure)
- **invariants_enforced_when_baseline_guard_1.passed_floor: 6090** (paired · monotonic-up)
- ratchet_history entries: 310 (+1 · schema-complete · commit=PENDING-P3-CA)

### notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md
- notes copy sha256 THIS-SEAL: `afb5862133a254fee2850ce733bc639680e3565eac6c40034b8e61af7f3fcc1c`
- audit copy sha256 THIS-SEAL: (same · byte-identical after /app companion Commit-A sync)
- ratchet.passed_floor: 6090 · ratchet.baseline_failures_sha256: `e6a47f7843b7cb2a56b151158671b909631b146e6a5e9dfee6726379ec167928`

### /app/backend/vendored/extraction_akki/ · vendored twin
- structural_sha256 THIS-SEAL: `6ff44254890532ebcff2ca5f8f7296ea12565305dfce9339606e38e4ca999ee3` (was `b467153f026a63ad7c1f5832e7147fea041727917adaa0903eb99f1788656077`)
- file_count 1014 → 1020 (+5 services.census_autonomy modules + 1 supervisord conf)

### tests/invariants/test_cp_census_autonomy_service_shape_gate.py
- 4 tests (SO §2.5 verbatim-docstring · SO §3.10-α closed-vocab paired-equality)
- companion additive package: services.census_autonomy (5 modules)
- companion supervisord conf: backend/scripts/census_scheduler.supervisord.conf

### Triple-green stripped-sha256 pre-Commit-A · BASELINE_GUARD=1 PYTHONHASHSEED=0
- Initial sweep `20260922T135406Z`: 6091 passed / 1 skipped / 174.07s · stripped_sha256 `5c1192fff22f22579aad4f93235064b065d5e1ae7ac7780fd7f89b6af81c46c5`
- Fresh-gate SweepA `20260922T162252Z`: 6091 passed / 1 skipped / 205.99s · stripped_sha256 `5c1192fff22f22579aad4f93235064b065d5e1ae7ac7780fd7f89b6af81c46c5`
- Fresh-gate SweepB `20260922T162628Z`: 6091 passed / 1 skipped / 188.80s · stripped_sha256 `5c1192fff22f22579aad4f93235064b065d5e1ae7ac7780fd7f89b6af81c46c5`
- **IDENTICAL byte-for-byte (stripped) across all three sweeps**

### 3-repo HEADs post-PHASE-3-CA Commit-A landing
- `/app/assessment_workspace/repos/Extraction-Akki` (programme/track-a): `c3e6725c1896b11bf1de8ca881562a57c9a53540`
- `/app/assessment_workspace` (master): `cf7c5fcae70007e4042374c8cc7e0711232f8e34` → `<PENDING-P3-CC-master>`
- `/app` (main): `9537adb71ffa2538afbbe515a8c2b7e9926d0de0` → `<PENDING-P3-CC-appmain>`

### R-106 §8(c) closed-vocab pins (Final constants in service_shape.py · paired-equality)
- `CENSUS_SCHEDULER_SUPERVISORD_PROGRAM_NAME = "census_scheduler"` (owner-verbatim)
- `TENANT_SCOPE_ENFORCEMENT_ANCHOR = "services.tenant_separation.tenant_registry:CANONICAL_TENANT_IDS"` (sealed 4j carrier)
- `REFUSAL_PATH_CLOSED_VOCAB` (6-tuple · R-106 §4 + §7): `BLOCKED_SURFACE_UNREACHABLE`, `DEFERRED_GPU_HOST_UNREACHABLE`, `BLOCKED_AWAITING_RESPONSE`, `BLOCKED_LAWFUL_BASIS_MISSING`, `BLOCKED_TENANT_SCOPE_MISMATCH`, `DEFERRED_BUDGET_EXCEEDED`
- `NO_AGENT_DEPENDENCY_ANCHOR = "services.census_autonomy.scheduler_program:main"` (supervisor entry-point · zero pytest/testing_agent imports)

<!-- STATE/PINS.md · post-PHASE-3-CENSUS-AUTONOMY-SERVICE Commit-A reference block · 2026-09-22T16:36:00Z END -->

<!-- STATE/PINS.md · post-PHASE-3-CONTINUATION-A' Commit-A reference block · 2026-09-22T17:15:00Z BEGIN -->

## PHASE 3 continuation A' · CP-CENSUS-AUTONOMY-ROUTER · Commit-A pin block

### baseline_failures.json — ratchet 6090 → 6097 (+7 measured)
- sha256 post-A': `eb377b5c7627b5e06c12db68ba0a84a76003ac2a5503e6e3c233422aeca9ea3d`
- sha256 pre-A': `e6a47f7843b7cb2a56b151158671b909631b146e6a5e9dfee6726379ec167928`
- counts_at_baseline.passed: 6097 (was 6090 · +7 measured)
- counts_at_baseline.failed: 3 (unchanged · 3 R-91 mirror-drift baselines · pending CP-APP-JS-UNIFY closure)
- passed_floor: 6097 (paired · monotonic-up)
- ratchet_history entries: 311 (+1 · schema-complete · commit=PENDING-P3-CA-PRIME)

### notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md
- ratchet.passed_floor: 6097 · ratchet.baseline_failures_sha256: `eb377b5c7627b5e06c12db68ba0a84a76003ac2a5503e6e3c233422aeca9ea3d`

### /app/backend/vendored/extraction_akki/ · vendored twin
- structural_sha256 THIS-SEAL: `082210b5bd609a7e0d23fc842c05f017d9778ad396215f900694d95101c2e56a` (was `6ff44254890532ebcff2ca5f8f7296ea12565305dfce9339606e38e4ca999ee3`)
- file_count 1020 → 1022 (+2 · state_reader.py + portal_census_autonomy.py)

### tests/invariants/test_cp_census_autonomy_router_a_prime.py
- 7 tests (SO §2.5 verbatim-docstring · SO §3.10-α closed-vocab paired-equality)
- companion additive files: `services/census_autonomy/state_reader.py` (NEW) · `routers/portal_census_autonomy.py` (NEW)
- server.py 2-line additive `include_router` inserted in all 3 assemblers (repo + pod_shell + runtime · Ship-Manifest DoD parity)

### Double-green stripped-sha256 pre-Commit-A · BASELINE_GUARD=1 PYTHONHASHSEED=0
- SweepA v3 (`20260922T170423Z`): 6098 passed / 1 skipped / 189.13s · stripped_sha256 `acf5963382c139d65d81e545a34d5a0c23830cf203e2c5867af5d486cad43d4f`
- SweepB (`20260922T170741Z`): 6098 passed / 1 skipped / 189.20s · stripped_sha256 `acf5963382c139d65d81e545a34d5a0c23830cf203e2c5867af5d486cad43d4f`
- **IDENTICAL byte-for-byte (stripped)**

### 3-repo HEADs post-PHASE-3-A' Commit-A landing
- `/app/assessment_workspace/repos/Extraction-Akki` (programme/track-a): `55ffc389cb5845f3c42801911cb7806455eeb7da`
- `/app/assessment_workspace` (master): `f34db5efcf970651dfe321bb6f87dd05dbd9310e` → `<PENDING-P3-AP-CC-master>`
- `/app` (main): `1de84fb06e7ad1de39eedacc89bb03980f8f9ed2` → `<PENDING-P3-AP-CC-appmain>`

### Endpoint pins (SO §3.10-α Final constants · paired-equality)
- `ON_DEMAND_RUN_ROUTE_PATH = "/api/portal/census/run"` (POST · JWT-gated · 202)
- `RUN_STATE_ROUTE_PATH_TEMPLATE = "/api/portal/census/runs/{census_run_id}/state"` (GET · JWT-gated · 200 real state | 404)
- `CENSUS_RUN_STATE_CODES = ("PENDING","COMPLETE","REFUSED")` (state_reader · Final closed vocab)

### Owner "REAL scheduler state only" enforcement (state_reader source-level guard · invariant 6)
Banned synthesis markers in state_reader.py: `progress_percent` · `estimated_completion` · `fake_progress` · `mock_state` · `random.random` · `random.randint`

### R-106 §8 ops-proof (folded into A' Commit-A same-slice cure)
- `20260922T164451Z_ops_proof_a_kill_backend_v2.log` · **PASS · scheduler independence proof** (backend pid 9558→9612 · scheduler pid 9552 UNCHANGED throughout backend restart)
- `20260922T164534Z_ops_proof_b_akki_test_e2e.log` · **PASS · AKKI-TEST end-to-end zero-agent** (agent enqueued cr-30eb39ba5562 at t=0 · scheduler picked up at t=+45s · result receipt written · pending removed · zero agent involvement between enqueue and completion · R-106 §5 auto-flow + §8 exit both satisfied)

### Same-slice cure: harness_ground_truth/latest.json refresh
- Refresh timestamp: 2026-09-22T17:00:08Z (was 2026-09-22T04:45:51Z · aged 12.22h past 12h threshold)
- Refresh method: `tools/wave_g5_realchrome_verification_harness.py --label a_prime_refresh` (GREEN · dummies absent · expected present · styled-element-anchor spans intact)
- Receipt: `phase0/eyeball_proxies/20260922T165941Z_wave_g5_realchrome_a_prime_refresh_*.png`

<!-- STATE/PINS.md · post-PHASE-3-CONTINUATION-A' Commit-A reference block · 2026-09-22T17:15:00Z END -->

<!-- STATE/PINS.md · post-PHASE-3-CONTINUATION-A'' Commit-A reference block · 2026-09-22T18:20:00Z BEGIN -->

## PHASE 3 continuation A'' · CP-CENSUS-AUTONOMY-UI-DRAWER · Commit-A pin block

### baseline_failures.json — ratchet 6097 → 6103 (+6 canonical measured)
- sha256 post-A'': `aea4469a8c64012cf92743ba47b6dff9203af0714db288387e08019669d53a28`
- sha256 pre-A'':  `eb377b5c7627b5e06c12db68ba0a84a76003ac2a5503e6e3c233422aeca9ea3d`
- counts_at_baseline.passed: 6103 (was 6097 · +6 canonical measured; +8 new invariants − 2 collection-drift)
- counts_at_baseline.failed: 3 (unchanged · 3 R-91 mirror-drift baselines RETAINED per R-86 property 4 anchor · transiently GREEN post-A'' twin sync but list preserved · explicit retirement deferred to future CP-APP-JS-UNIFY)
- passed_floor: 6103 (paired · monotonic-up)
- ratchet_history entries: 312 (+1 · schema-complete · commit=PENDING-P3-CA-DPRIME → resolves at Commit-C fixup)

### notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md
- ratchet.passed_floor: 6103 · ratchet.baseline_failures_sha256: `aea4469a8c64012cf92743ba47b6dff9203af0714db288387e08019669d53a28`
- both twins md5 `55f89354ace6698f3bb11b75e4d8da62`

### /app/backend/vendored/extraction_akki/ · vendored twin
- UNCHANGED this seal (A'' backend scope limited to `tests/` which is excluded from vendored mirror per `prod_vendor_sync.py` INCLUDED_TOP_DIRS convention).
- Vendored mirror invariant `test_vendored_tree_byte_identical_mirror_of_spine` RE-VERIFIED GREEN post-Commit-A.

### tests/invariants/test_cp_census_autonomy_ui_a_double_prime.py
- 8 RED-first invariants (SO §2.5 verbatim-docstring · owner directive quoted verbatim in module docstring)
- companion additive files: `pod_shell/frontend/src/components/portal/CensusAutonomyDrawer.jsx` (NEW) · `pod_shell/frontend/src/hooks/useCensusRunState.js` (NEW)
- `pod_shell/frontend/src/App.js` 2-line additive: `import CensusAutonomyDrawer from "@/components/portal/CensusAutonomyDrawer";` at line 22 + `<CensusAutonomyDrawer />` overlay mount at line 1339 inside `<div className="App">` after `</BrowserRouter>`
- byte-identical twin at `/app/frontend/src/` per Ship-Manifest DoD parity

### Byte-identity mirror md5s (this-Commit-A)
- App.js:  `250dc6e55e02cdce1ad53a50c5b12f0e` (/app/frontend/src == pod_shell/frontend/src)
- Hook:    `2fd945d3548f31c34ce90de7887eafb7` (both trees)
- Drawer:  `76ce932b61c5c8a4161d3d1e5cb62aa2` (both trees)

### Double-green stripped-sha256 pre-Commit-A · BASELINE_GUARD=1 PYTHONHASHSEED=0
- SweepA3 (2026-09-22T18:03Z · 189.96s): 6106 passed / 1 skipped / 0 failed · stripped_sha256 `0b3a2d3c94f8b3aa07f9fdaf9db7cd863b3e369994207a2ac334bc5b439b7fc2`
- SweepB3 (2026-09-22T18:06Z · 189.91s): 6106 passed / 1 skipped / 0 failed · stripped_sha256 `0b3a2d3c94f8b3aa07f9fdaf9db7cd863b3e369994207a2ac334bc5b439b7fc2`
- **IDENTICAL byte-for-byte (stripped)**. Full receipts at `phase0/drill_receipts_cp_census_autonomy_a_double_prime/sweep_A3_2026-09-22.{log,stripped}` + `sweep_B3_2026-09-22.{log,stripped}` + `double_green_sha256_final.txt`.

### 3-repo HEADs post-PHASE-3-A'' Commit-A landing
- `/app/assessment_workspace/repos/Extraction-Akki` (programme/track-a): `527d09bf1948a6b32068769d5dcde6c9abcc192c`
- `/app/assessment_workspace` (master): `f34db5efcf970651dfe321bb6f87dd05dbd9310e` → `<PENDING-P3-APP-CB-master>` → `<PENDING-P3-APP-CC-master>`
- `/app` (main): `dd8ba7303` → `<PENDING-P3-APP-CC-appmain>`

### UI element pins (SO §3.10-α Final constants + verbatim button labels)
- `CENSUS_RUN_STATE_CODES = ["PENDING", "COMPLETE", "REFUSED"]` (drawer top-level Final closed vocab)
- Button label verbatim: "Run census" (invariant 7 gates presence)
- Data-testids: `census-autonomy-open-drawer`, `census-autonomy-drawer`, `census-autonomy-close-drawer`, `census-autonomy-tenant-id`, `census-autonomy-source-descriptor`, `census-autonomy-lawful-basis`, `census-autonomy-submit-run`, `census-autonomy-submit-error`, `census-autonomy-new-run`, `census-autonomy-running-card-{pending,complete,refused,unknown,invalid}`
- Hook poll interval: `POLL_INTERVAL_MS = 5000`
- Hook target endpoint: `${REACT_APP_BACKEND_URL}/api/portal/census/runs/{censusRunId}/state` (encodeURIComponent applied)
- Drawer submit endpoint: `${REACT_APP_BACKEND_URL}/api/portal/census/run`
- JWT source: `window.localStorage.getItem("jwt")`

### Owner "REAL scheduler state only" enforcement (drawer + hook · invariant 6 · six banned synthesis markers)
- `progress_percent` · `estimated_completion` · `fake_progress` · `mock_state` · `Math.random` · `random.random`

### −2 collection-drift anomaly
- Documented at `phase0/drill_receipts_cp_census_autonomy_a_double_prime/anomaly_note.md`
- Effect: nominal +11 expected (8 new + 3 mirror-drift cures) but observed +9 in `passed` and +6 in `collected`
- Root cause candidates (deferred to future desk-lane forensics per SO §6.4 NOTHING-BEYOND):
  (1) prior-seal `counts_at_baseline` arithmetic possibly inconsistent (legacy_conditional_skips accounting)
  (2) dynamic-collection parametrize test whose parameter cardinality reads a filesystem directory affected by A'' drill-receipts folder growth
- Ratchet compliance: 6106 real passed ≥ 6103 floor ✓; 0 failed ⊆ 3 baseline_failures ✓; 1 skipped ≤ 1 max ✓

### RED-first ordering evidence
- Test authored at 17:25Z with pod_shell mirror empty → 8/8 RED (paths absent, App.js unmounted)
- Mirror sync + App.js twin edit at 17:35Z → 8/8 GREEN
- Evidence banked at `phase0/drill_receipts_cp_census_autonomy_a_double_prime/red_first_ordering.md`

<!-- STATE/PINS.md · post-PHASE-3-CONTINUATION-A'' Commit-A reference block · 2026-09-22T18:20:00Z END -->

<!-- STATE/PINS.md · post-PHASE-3-CONTINUATION-A''' Commit-A reference block · 2026-09-22T18:50:00Z BEGIN -->

## PHASE 3 continuation A''' · CP-CENSUS-AUTONOMY-GPU-SPEND · Commit-A pin block

### baseline_failures.json — ratchet 6103 → 6109 (+6 canonical measured)
- sha256 post-A''': `b4237e36dc075e839ecad8d31e9c294692ce1a4fba549fcb4a6cc66d8f7e1da3`
- sha256 pre-A''':  `aea4469a8c64012cf92743ba47b6dff9203af0714db288387e08019669d53a28`
- counts_at_baseline.passed: 6109 (was 6103 · +6 measured)
- counts_at_baseline.failed: 3 (unchanged · 3 R-91 mirror-drift baselines RETAINED per R-86 anchor)
- passed_floor: 6109
- ratchet_history entries: 313 (+1 · commit=PENDING-P3-CA-TPRIME → resolves at Commit-C fixup)

### notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md
- ratchet.passed_floor: 6109 · ratchet.baseline_failures_sha256: `b4237e36dc075e839ecad8d31e9c294692ce1a4fba549fcb4a6cc66d8f7e1da3`
- both twins md5 `fb78231ceb2ed2abfe9dd2b3f5317845`

### /app/backend/vendored/extraction_akki/ · vendored twin
- structural_sha256 THIS-SEAL: `88dad1bdba27584fb1b60b5242487b533e0f0ad1ade86e1fe97b4875e8aa297f` (was earlier post-A' `082210b5bd...`; A'' UNCHANGED vendored; A''' +1 file)
- file_count 1022 → 1023 (+1 · gpu_spend_capture.py)

### tests/invariants/test_cp_census_autonomy_gpu_spend_a_triple_prime.py
- 6 RED-first invariants (SO §2.5 verbatim-docstring · owner directives quoted verbatim in module docstring)
- companion additive file: `services/census_autonomy/gpu_spend_capture.py` (NEW · thin adapter over sealed ssh_seam)
- sealed carrier imports: `services.training_runner.ssh_seam.{execute_remote_command, current_mode, is_mock, list_hosts}` (READ-ONLY · identity discipline · invariant 5)

### Double-green stripped-sha256 pre-Commit-A · BASELINE_GUARD=1 PYTHONHASHSEED=0
- Sweep A (2026-09-22T18:40Z · 191.17s): 6112 passed / 1 skipped / 0 failed · stripped_sha256 `bd2010df9cd70e7294cf92a04eaf2ae7a2a6ee08de9a2209ba813b7af2e4a8ac`
- Sweep B (2026-09-22T18:43Z · 191.36s): 6112 passed / 1 skipped / 0 failed · stripped_sha256 `bd2010df9cd70e7294cf92a04eaf2ae7a2a6ee08de9a2209ba813b7af2e4a8ac`
- **IDENTICAL byte-for-byte (stripped)**

### 3-repo HEADs post-PHASE-3-A''' Commit-A landing
- `/app/assessment_workspace/repos/Extraction-Akki` (programme/track-a): `c3807d7c72c9599db4e692ee88e44c8378ee1873`
- `/app/assessment_workspace` (master): `6d654a66` → `<PENDING-P3-ATP-CB-master>` → `<PENDING-P3-ATP-CC-master>`
- `/app` (main): `615ac44ac` → `<PENDING-P3-ATP-CC-appmain>`

### GPU_SPEND_CAPTURE closed-vocab (SO §3.10-α Final tuple)
- `GPU_SPEND_CAPTURE_STATE_CODES = ("CAPTURED", "HONEST_GAP_UNREACHABLE", "HONEST_GAP_MOCK_MODE")`
- `NVIDIA_SMI_QUERY = "nvidia-smi --query-gpu=timestamp,name,index,power.draw,utilization.gpu,memory.used --format=csv,noheader"`
- `CAPTURE_PURPOSE = "census_autonomy_gpu_spend_capture"` (banked in every ssh_seam receipt)

### Owner "NO GPU-spend fabrication" enforcement (source-level guard · invariant 4 · 6 banned markers)
- `fake_gpu` · `mock_gpu_spend` · `synthesized_watts` · `random.random` · `random.randint` · `random.choice`

### Mode dispatch record shapes
- **HONEST_GAP_MOCK_MODE**: `{status, captured_at_utc, mode, note}` (no numeric fields — invariant 6 bans watts / gpu_load_percent / memory_used_mib)
- **HONEST_GAP_UNREACHABLE**: `{status, captured_at_utc, mode, unreachable_hosts, reason_per_host, note}` (per STOP condition #2 · zero fabricated telemetry)
- **CAPTURED**: `{status, captured_at_utc, mode, hosts_captured, per_host_raw, query}` (per_host_raw = dict host_slug → redacted nvidia-smi stdout verbatim from sealed ssh_seam)

### Owner-exclusive open (new)
- **DQ-GPU-SSH-KEYS** — **P1** · Owner-side SSH credentials for `akki-vm` (41.173.184.244) + `akki-vm-ii` (41.173.184.247) needed to flip `GPU_CONNECT_MODE=real` and unlock live nvidia-smi capture. Currently sealed ssh_seam has no configured hosts under real mode → mock-mode returns HONEST_GAP_MOCK_MODE per owner directive (no fabrication).

<!-- STATE/PINS.md · post-PHASE-3-CONTINUATION-A''' Commit-A reference block · 2026-09-22T18:50:00Z END -->

<!-- STATE/PINS.md · OWNER CORRECTION 2026-09-22T18:55Z · DQ-GPU-SSH-KEYS SELF-RESOLVED · state-only mini-bank · 2026-09-22T19:00:00Z BEGIN -->

## OWNER CORRECTION 2026-09-22T18:55Z · DQ-GPU-SSH-KEYS SELF-RESOLVED · GPU live-lane flipped

**Owner correction**: DQ-GPU-SSH-KEYS was mis-classified as an owner-ask in the A''' Commit-A seal report; custody key was already banked and proven working this session. Owner corrective action: probe key against both hosts; if authenticated (expected), flip GPU_CONNECT_MODE=real, close DQ as self-resolved with the probe receipt.

### Custody key pins (verbatim · unchanged since 2026-08-28)
- Path: `/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu`
- Mode: `0600`
- Fingerprint: `SHA256:M3Dre1A1I1ZQFo0FDsfzbWPwn5z+oxmZ02y1eZwFy1A`
- Pubkey: `/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu.pub`
- Comment: `akki-gpu-hosts-seam-key-20260828T162217Z` (ED25519)
- Provenance: `phase0/keypair_hardening_receipts/20260828T162217Z_step1_keygen.json`

### GPU-host lane pins (post-flip)
- `akki-vm` — public IP `41.173.184.244` · port 22 · user `ubuntu` · 2× NVIDIA H200 · driver `570.211.01` · 143771 MiB VRAM/GPU
- `akki-vm-ii` — public IP `41.173.184.247` · port 22 · user `ubuntu` · 2× NVIDIA H200 · driver `570.211.01` · 143771 MiB VRAM/GPU
- Total: **4× H200 · 575084 MiB VRAM total across both hosts**

### `/app/backend/.env` runtime state (gitignored · not committed)
- `GPU_CONNECT_MODE=real`
- `AKKI_GPU_HOSTS=akki-vm,akki-vm-ii`
- `AKKI_VM_HOST=41.173.184.244` · `AKKI_VM_PORT=22` · `AKKI_VM_USERNAME=ubuntu` · `AKKI_VM_HOSTNAME_EXPECTED=akki-vm` · `AKKI_VM_SSH_PRIVATE_KEY_PATH=<custody_key_path>`
- `AKKI_VM_II_HOST=41.173.184.247` · `AKKI_VM_II_PORT=22` · `AKKI_VM_II_USERNAME=ubuntu` · `AKKI_VM_II_HOSTNAME_EXPECTED=akki-vm-ii` · `AKKI_VM_II_SSH_PRIVATE_KEY_PATH=<custody_key_path>`
- `AKKI_*_SSH_PASSWORD`: intentionally UNSET (server-side password auth dead per 2026-08-28 hardening; key-only is the only working method).

### E2E CAPTURED proof (in-process)
- Call: `services.census_autonomy.gpu_spend_capture.capture_gpu_spend()`
- Return: `{"status": "CAPTURED", "mode": "real", "hosts_captured": ["akki-vm", "akki-vm-ii"], "per_host_raw": {<live redacted nvidia-smi stdout>}, "query": "nvidia-smi --query-gpu=timestamp,name,index,power.draw,utilization.gpu,memory.used --format=csv,noheader"}`
- Sealed ssh_seam auto-banked receipts:
  - `phase0/gpu_receipts/20260922T190000Z_akki_vm_census_autonomy_gpu_spend_capture_gpurcp-c84016689c3f.log` (rc=0 · 3.196s · 2 H200 rows)
  - `phase0/gpu_receipts/20260922T190003Z_akki_vm_ii_census_autonomy_gpu_spend_capture_gpurcp-bf9ebb8b431c.log` (rc=0 · 3.049s · 2 H200 rows)
- Probe receipt: `phase0/gpu_probes/20260922T190000Z_GPU_LANE_REVERIFY_A_TRIPLE_PRIME.json`

### DQ closure
- `DQ-GPU-SSH-KEYS` status: **SELF_RESOLVED** (was P1 · mis-classified as owner-ask in the A''' seal report; owner correction 2026-09-22T~18:55Z clarified · closure receipt above)
- **Removed** from `RESUME.md §7 OWNER-EXCLUSIVE OPEN` list; anchored here in PINS for cold-reader continuity.

### Order B audit dependency (owner correction 2026-09-22T~18:55Z)
- `phase0/drill_receipts_cp_census_autonomy_a_double_prime/anomaly_note.md` amended with Order B audit dependency section: the −2 collection-drift forensic MUST resolve before the Order B audit passes over the 6097 → 6103 → 6109 ratchet range. Three resolution paths documented in the note.

<!-- STATE/PINS.md · OWNER CORRECTION 2026-09-22T18:55Z · DQ-GPU-SSH-KEYS SELF-RESOLVED · state-only mini-bank · 2026-09-22T19:00:00Z END -->

<!-- STATE/PINS.md · post-PHASE-3-CONTINUATION-A'''-cont-A Commit-A reference block · 2026-09-22T19:15:00Z BEGIN -->

## PHASE 3 continuation A'''-cont-A · CP-CENSUS-AUTONOMY-RESPONSE-REQUIRED-QUEUE · Commit-A pin block

### baseline_failures.json — ratchet 6109 → 6118 (+9 canonical measured)
- sha256 post-A'''-cont-A: `88ce4652d26e4adf5aaae225d0092d7bed55c3289dcea68a6e8138afbd7a58eb`
- sha256 pre-A'''-cont-A:  `b4237e36dc075e839ecad8d31e9c294692ce1a4fba549fcb4a6cc66d8f7e1da3`
- counts_at_baseline.passed: 6118 · counts_at_baseline.failed: 3 (unchanged)
- passed_floor: 6118 · ratchet_history entries: 314 (+1)

### notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md
- ratchet.passed_floor: 6118 · ratchet.baseline_failures_sha256: `88ce4652...`

### /app/backend/vendored/extraction_akki/ · vendored twin
- structural_sha256 THIS-SEAL: `458c224f9583dc1970d7933bb619e39c01e1461d0e15fcc1fba1c047cc5f113f`
- file_count 1023 → 1025 (+2 · response_required_queue.py + portal_census_response_required.py)

### tests/invariants/test_cp_census_autonomy_response_required_a_triple_prime_cont_a.py
- 9 RED-first invariants · SO §2.5 verbatim-docstring · owner directive quoted verbatim in module docstring
- companion additive files: `services/census_autonomy/response_required_queue.py` (NEW · fs-cursor-backed queue) + `routers/portal_census_response_required.py` (NEW · 2 JWT-gated routes)
- sealed carrier imports: `services.auth.{dependencies, identity}` + `services.enforce.principal_context_adapter` (READ-ONLY)

### Router pins (SO §3.10-α · Final constants)
- `LIST_ROUTE_PATH = "/api/portal/census/response-required-items"`
- `RESOLVE_ROUTE_PATH_TEMPLATE = "/api/portal/census/response-required-items/{item_id}/resolve"`

### Module pins (SO §3.10-α · Final constants + closed vocab)
- `RESPONSE_REQUIRED_ITEM_STATE_CODES = ("PENDING", "RESOLVED_ACCEPTED", "RESOLVED_REJECTED")`
- `RESPONSE_REQUIRED_DIR = CENSUS_STATE_DIR / "response_required"` (Final Path off env)
- Public exceptions: `ItemNotFound` · `InvalidResolvedState`

### Server.py mounts (spine + pod_shell + runtime · byte-identical Ship-Manifest DoD)
- Spine `backend/server.py` line 279-286: additive import + `app.include_router(portal_census_response_required_router.router)`
- Pod_shell `pod_shell/backend/server.py`: byte-identical with runtime `/app/backend/server.py` md5 `19055c84140536c87bab24ada03fcd5f`

### Double-green stripped-sha256 pre-Commit-A · BASELINE_GUARD=1 PYTHONHASHSEED=0
- Sweep A (2026-09-22T19:11Z · 192.09s): 6121 passed / 1 skipped / 0 failed · stripped_sha256 `31ba5011dcff95542b4844c73b9aaa5662dba8579ae8bb7ac7a012b02f386805`
- Sweep B (2026-09-22T19:14Z · 191.66s): 6121 passed / 1 skipped / 0 failed · stripped_sha256 `31ba5011dcff95542b4844c73b9aaa5662dba8579ae8bb7ac7a012b02f386805`
- **IDENTICAL byte-for-byte (stripped)**

### 3-repo HEADs post-PHASE-3-A'''-cont-A Commit-A landing
- `/app/assessment_workspace/repos/Extraction-Akki` (programme/track-a): `a0dcc0626fa80ec357dd8a56adc7fc2a21104669`
- `/app/assessment_workspace` (master): `b06b1cac` → then post-DQ-GPU mini-bank `f4399ea0` → `<PENDING-P3-CA-TPRIME-CONT-A-CB-master>`
- `/app` (main): `739ac5e4a4d1ae2e15d1fdf1cec5d3081d244d8a` → `<PENDING-P3-CA-TPRIME-CONT-A-CC-appmain>`

### Queue infra semantics
- Queue is ORIGIN-EMPTY at mount time (no baked-in items)
- Production writers into queue DEFERRED to future slice (engine-refusal-bank bridge or drawer-owner-in-the-loop button)
- UI response-required-badge component DEFERRED to A'''-cont-B slice

<!-- STATE/PINS.md · post-PHASE-3-CONTINUATION-A'''-cont-A Commit-A reference block · 2026-09-22T19:15:00Z END -->

<!-- P4-C-III-PINS-2026-02-23 BEGIN -->

## PHASE 4 (c-iii) · CP-SKILLS-LAYER-A18-3 + A18-5 · **SEALED 2026-02-23T00:17:00Z**

- **CODE branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`
- **CODE head (Commit-A):** `dafb45c8b004bad233439920c85cfae0847c6800`
- **/app companion Commit-A:** `b312ec870a58a39b557b39e7c34437a8d9e485a1`
- **STATE branch:** `master` in `/app/assessment_workspace`
- **STATE head (Commit-B):** pending this-banking
- **RATCHET at this seal:** **6183 pass / 3 fail (baseline · all transient GREEN in current sweep) / 1 skip · floor 6183 · monotonic-up from 6171** (+12 canonical measured)
- **baseline_failures.json sha256 (post-seal):** `81e790bbbc42cc13aa178c178c6a84d73001d83150ebfba880bd317351759a88`
- **notes/ORCH_BOOT.md sha256 (post-regen · byte-identical with /app audit mirror):** `27414c1e572f5f5edea18e745049bfe440546806a9ec848d777f262ebea17a9d`
- **Double-sweep byte-identical stripped-sha256:** `32d6e0969064b9fd947be0e1f91c9f46d042393b6044b3a40640cccd1e521739`
- **Vendored MANIFEST.json:** file_count 1030→1032 · structural_sha256 `141cac1c27e7df8bf3d1570478f91e6a19ca592077f75082832df3a1f1f4e59e`
- **New backend files:**
  1. `backend/contracts/skill_call_governance_envelope_v0.py` (A18.3 Pydantic 7-field frozen envelope)
  2. `backend/tests/invariants/skill_call_governance_envelope_v0.contract_snapshot.json` (parity snapshot)
  3. `backend/services/skill_call_scope_resolver.py` (A18.5 server-side scope resolver + refusal exceptions)
  4. `backend/tests/invariants/test_cp_skills_layer_a18_3_a18_5_phase_4_c_iii.py` (12 pins · 6 A18.3 + 6 A18.5)
- **Modified backend files:**
  1. `backend/tests/invariants/test_frozen_contract_snapshot_parity.py` (+1 line additive CONTRACT_TO_SNAPSHOT entry)
  2. `backend/tests/invariants/baseline_failures.json` (ratchet 6171→6183)
- **Sealed carriers UNCHANGED per SO §3.8:**
  - `contracts/skill_provisioning_record_v0.py` (A18.1 Slice 1)
  - `services/skill_provisioning_persistence.py` (A18.2 Slice 2) — imported READ-ONLY via `get_by_skill_id` public callable
  - `services/skill_files/persistence.py` (A18.7 buyer-facing)
  - `services/auth/engineer_key_grant.py` (secondary carrier · cited in docstring, never modified)
  - All PHASE 3 sealed chain + P4-a + P4-b-i + P4-c-i + P4-c-ii
- **Owner directive verbatim (2026-02-23T~00:03Z via ask_human reply):**
  > "§6.8 — (a) Y, proceed exactly as scoped. (b) The Doc-18 §A18-3 / §A18-5 anchors suffice; if the sealed gate infrastructure you pin over carries its own canon anchors (e.g., MOAC/agent-containment gate rules), cite those secondarily in the docstring so the drift-detector names the carrier it guards — disk-verifiable, your call on the exact IDs. (c) No owner action has landed: DQ-17 rotation still pending owner-side, −2 drift forensic still queued pre-Order-B, no new drops. Boundary unchanged. Boot sequence + lessons discipline as you stated. Go — and per §6.8.6, future turn-ends report-and-continue rather than Y/N menus."
- **Banked Lesson #10 first-appearance this-slice** (NEW Pydantic contract requires same-slice CONTRACT_TO_SNAPSHOT map additive entry alongside parity snapshot).

<!-- P4-C-III-PINS-2026-02-23 END -->

<!-- P4-C-IV-PINS-2026-02-23 BEGIN -->

## PHASE 4 (c-iv) · CP-SKILLS-LAYER-A18-8 · **SEALED 2026-02-23T00:32:00Z**

- **CODE branch:** `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`
- **CODE head (Commit-A):** `ee505425feea114acb057f87c0125f75baa6d085`
- **/app companion Commit-A:** `047c1b49eb5f29ef6bb1fbc678b63cff557e75ff`
- **STATE branch:** `master` in `/app/assessment_workspace`
- **STATE head (Commit-B):** pending this-banking
- **RATCHET at this seal:** **6194 pass / 3 fail (baseline · transient GREEN) / 1 skip · floor 6194 · monotonic-up from 6183** (+11 canonical measured)
- **baseline_failures.json sha256 (post-seal):** `ec58438f667cd17686b7ffcf29a58225e1bef88c2b4371f1347e2baa4b70a1ac`
- **notes/ORCH_BOOT.md sha256 (post-regen · byte-identical /app audit mirror):** `52d56a120eab3493d5e7e07cfe38540ac5c6582a7df40bdebc991dff8e6c1084`
- **Double-sweep byte-identical stripped-sha256:** `dfb8d45637954398db152812311e6036873591c80dc126b44b3fe390e3f8ed80`
- **Vendored MANIFEST.json:** file_count 1032→1033 · structural_sha256 `358f9b0e24ca8929bced5f8b4c10953db640fc852cc89130dc6ef54ac4d3bb8b`
- **New backend files:**
  1. `backend/services/skill_donor_provenance.py` (A18.8 Final manifest · donor sha256 + line counts frozen · 356-line canon anchor · REMAINING_SCOPE_HONEST_GAP declared verbatim)
  2. `backend/tests/invariants/test_cp_skills_layer_a18_8_phase_4_c_iv.py` (11 RED-first pins)
- **Sealed donor code UNCHANGED per SO §3.8 (drift-detector Invariant 6 sha256-asserts each sweep):**
  - `backend/contracts/callable_skill_provisioning_v0.py` · 101 lines · sha256 `d61a446c9ba130347320085b3de95f198c2e5bb7d1503c3af524a7b1535fa391`
  - `backend/services/transform_forms/callable_skill_gate.py` · 144 lines · sha256 `02d5674517a804eb93ba5c8b1ab1d64368294650294a3a32a6164396c99b3871`
  - `backend/services/transform_forms/callable_skill_persistence.py` · 111 lines · sha256 `0590339f1efe1bb5944aeba57037f9fa27dae71cb7eb116565f1792227a5c428`
  - TOTAL 356 lines · matches canon §A18.8 verbatim word-for-word.
- **Donor repos (from STATE/PINS.md · byte-identical three-way verified):**
  - RMS-IQ-Core-2 · main · `ea5aa019521eee22ad4f8ea29efdfa2af357be3b`
  - Akki-OS-V1 · main · `8c361903cdd319bfdc0709de3f4392f5bfa3956b`
- **Owner LIFT ruling verbatim (this-session):**
  > "One rule for the donor-code LIFT from RMS-IQ-Core-2 / Akki-OS-V1: lifted code enters through the same additive discipline as new code — cite the donor repo + path + commit in the module docstring (provenance per §A18.8), run the lifted surface through RED-first pins exactly as if authored fresh, and no donor code touches sealed carriers."
- **QUEUED owner correction (mid-Slice-4)** — CP-CENSUS-TENANT-ADMISSION-CORRECTION opens post-seal · full verbatim in DECISIONS.md.

<!-- P4-C-IV-PINS-2026-02-23 END -->


## CP-AIP-9-COMMISSION-VIEW + R-91-EPSILON-RETIREMENT · **SEAL BOUNDARY 2026-02-23T~10:20Z**

<!-- CP-AIP-9-PINS-2026-02-23 BEGIN · SO §6.9(5)-AMENDED bundle-based continuity FIRST APPLICATION -->

### Milestone-seal continuity bundle pins (SO §6.9.5 AMENDED 2026-02-23 · bundle-based)

**Mechanism:** per SO §6.9.5 (amended 2026-02-23 · verbatim owner drop banked at `STATE/OWNER_DROPS/so_6_9_clause_5_bundle_amendment_20260223/DROP.md`), every milestone seal emits a git bundle of BOTH `programme/track-a` and `master`, sha256-pinned here, deposited at the pod-local deliverables endpoint `/app/assessment_workspace/continuity_bundles/`. No credentials, no push, nothing public. The pod stays the working store; the bundle is the off-pod copy the platform's artefact mechanism fetches at session close.

**Code bundle — programme/track-a at Code Commit-A HEAD:**
- **Path:** `continuity_bundles/code_20260923T104129Z_CP_AIP_9.bundle`
- **Size:** 19,182,116 bytes (18.3 MiB)
- **sha256:** `054fcd3c876d84912850ae710b7fd8e6f9e5208d3175ea071b5441ee5047a672`
- **Refs:** `refs/heads/programme/track-a` → `30f8ccdead956977cd6608e5d30907c23c428190` (= CP-AIP-9 Code Commit-A HEAD)
- **Verify:** `git bundle verify` → "is okay" · **records a complete history** · hash algorithm: sha1
- **Emitted at:** 2026-02-23T~10:41Z pre-Commit-B (Code-A already landed)

**State bundle — master at seal-tail HEAD:**
- **Path:** `continuity_bundles/state_20260923T105456Z_CP_AIP_9.bundle`
- **Size:** 217,316,135 bytes (207.3 MiB)
- **sha256:** `0535fcba168e5bab10ace37ce12a447158a33a1b6f0f0f4cd5a2b7674eff2366`
- **Refs:** `refs/heads/master` → `2fc7dd3f78a67c3c27f229e8e932e9b308e72a3a` (= CP-AIP-9 State Commit-C fixup HEAD · the seal's state-tail before mini-bank)
- **Verify:** `git bundle verify` → "is okay" · **records a complete history** · hash algorithm: sha1
- **Emitted at:** 2026-02-23T~10:55Z post-Commit-C-fixup
- **Pin lock-in:** State mini-bank commit finalizes both bundle pins (this file · same commit).

**One-sentence protected objective:** the sealed record survives its environment (pod crash, session compaction, audit-inbox rotation) without depending on push credentials or repo visibility.

### Retirement — Private-visibility check + `PRIVATE-MIRROR-REMOTE-MISSING` honest-gap

- **Retired at this boundary** per SO §6.9(5) AMENDED. Prior text preserved additively in `STANDING_ORDERS.md §6.9.5` above the SUPERSEDED-BY block per SO §3.8.
- **Named objective the retired gate failed to protect:** continuity of the sealed record across environment loss.
- **Why withdrawn per §6.9 doctrine:** the visibility gate would refuse-correctly on public repos and yet a refusal here protects nothing — continuity is met by the sha-pinned bundle regardless of remote visibility.
- **Historical banking preserved without edit** (additive-only per SO §3.8): `STATE/OWNER_DROPS/na7p4_park_proceed_autonomously_mirror_probe_20260223/DROP.md` (case (c) probe result stands as historical record).

### `AKKI-OS-ROOT-PUBLIC-EXPOSURE` — new P0-security honest-gap · non-blocking

- **Recorded at this boundary** per owner drop 2026-02-23 banked at `STATE/OWNER_DROPS/akki_os_root_public_exposure_20260223/DROP.md`.
- **Named objective:** customer connector hostnames must not be exposed on a public repo.
- **Pod-side probe result:** cannot flip `bramuel-syni/Akki-OS-Root` visibility from this pod — no `gh` CLI installed, no admin token env var, repo not on-disk in this pod.
- **Owner-action-required (any one path sufficient):** GitHub UI Settings → Danger Zone → Change visibility → Make private; OR `gh repo edit bramuel-syni/Akki-OS-Root --visibility private`; OR REST API PATCH with admin PAT.
- **Non-blocking status (owner-directed):** in-flight CP-AIP-9 5-commit seal continues without pause.

### 3-repo HEADs at seal boundary (pre-mini-bank tip)

- **Code (programme/track-a):** `30f8ccdead956977cd6608e5d30907c23c428190` (Code Commit-A — CP-AIP-9 + R-91 ε retirement)
- **State (master):** `cf62339e31b0fb7243ae4cd78cb44c68f6c315dc` (OWNER-Q3 fold-in · pre-Commit-B tip · Commit-B lands next)
- **/app (main):** `4d57db1a67a9752b5d63acbde07c8b691cc7e5f7` (/app Commit-A companion of Code-A)

### Milestone-seal REPORT-AND-CONTINUE receipt line (this-seal · FINAL post-mini-bank)

`CP-AIP-9 seal COMPLETE · code bundle sha256 054fcd3c876d84912850ae710b7fd8e6f9e5208d3175ea071b5441ee5047a672 (18.3 MiB · programme/track-a @ 30f8ccd) · state bundle sha256 0535fcba168e5bab10ace37ce12a447158a33a1b6f0f0f4cd5a2b7674eff2366 (207.3 MiB · master @ 2fc7dd3f) · SO §6.9(5) AMENDED bundle-based continuity FIRST APPLICATION LANDED · PRIVATE-MIRROR-REMOTE-MISSING RETIRED · AKKI-OS-ROOT-PUBLIC-EXPOSURE recorded (P0-security · owner-action-required · non-blocking) · CP-AIP-ASSIST cards PRE-APPROVED BY CONSTRUCTION under §6.8 · Track-5 pre-build checkpoint REMOVED · RUN-TO-COMPLETION mandate ACTIVE.`

### CP-AIP-9 5-commit seal chain (FULL SHA TABLE · POST-MINI-BANK)

| # | Commit | SHA | Branch | Purpose |
|---|---|---|---|---|
| 1 | Code Commit-A | `30f8ccdead956977cd6608e5d30907c23c428190` | `programme/track-a` | 1 new module + 8 RED-first pins + baseline_failures ratchet 6317→6325→6313 via env_drift_reset + 12 skip decorators + drill receipts |
| 2 | /app companion A | `4d57db1a67a9752b5d63acbde07c8b691cc7e5f7` | `main` | notes/audit ORCH_BOOT R-6 regen + Extraction-Akki gitlink advance dba4499→30f8ccd |
| 3 | State Commit-B | `79a2ff0b683ca4ae982c3d79bdf16014483f416f` | `master` | Objective card + queued-delete + comprehensive receipt + THREE fold-in owner drops (SO §6.9(5) amendment · Akki-OS-Root · ASSIST pre-approval) + STANDING_ORDERS §6.9.5 amended + PINS code-bundle-pin + GAPS_FIXED_LEDGER 10 entries + EXECUTION_ORDER 5.11 wave + RESUME rewrite + `.gitignore` bundle-ignore + DECISIONS entries |
| 4 | State Commit-C fixup | `2fc7dd3f78a67c3c27f229e8e932e9b308e72a3a` | `master` | R-6 boundary regen advancing heads_last_sealed to State-B + Code-A + state mini-bank rows 1-3 |
| 5 | /app companion C | `d8d954639...` | `main` | byte-identical audit twin mirror of State-B + State-C fixup |
| 6 | State mini-bank | *(this commit)* | `master` | RESUME rewrite + PINS state-bundle-pin final + full 5-commit SHA table |

<!-- CP-AIP-9-PINS-2026-02-23 END -->


## CP-AIP-10-TRAINING-RUNS · **SEAL BOUNDARY 2026-02-23T~11:45Z · LAST BY CONSTRUCTION**

<!-- CP-AIP-10-PINS-2026-02-23 BEGIN · SO §6.9(5) AMENDED bundle-based continuity · 2nd application -->

### Milestone-seal continuity bundle pins (SO §6.9.5 AMENDED 2026-02-23 · bundle-based)

**Mechanism:** per SO §6.9.5 (amended 2026-02-23 · verbatim owner drop banked at `STATE/OWNER_DROPS/so_6_9_clause_5_bundle_amendment_20260223/DROP.md`), every milestone seal emits a git bundle of BOTH `programme/track-a` and `master`, sha256-pinned here, deposited at the pod-local deliverables endpoint `/app/assessment_workspace/continuity_bundles/`. No credentials, no push, nothing public.

**Code bundle — programme/track-a at Code Commit-A HEAD (this-seal · 2nd bundle application):**
- **Path:** `continuity_bundles/code_20260923T114743Z_CP_AIP_10.bundle`
- **Size:** 19,141,578 bytes (18.3 MiB)
- **sha256:** `48b2c169e5d04985f1754ff17d9ca0ce9688bd9c6067ba1dc9ca1252c7b08a41`
- **Refs:** `refs/heads/programme/track-a` → `8ef25c10ba28fbf09255396281a619a4be819612` (= CP-AIP-10 Code Commit-A HEAD)
- **Verify:** `git bundle verify` → "is okay" · **records a complete history** · hash algorithm: sha1
- **Emitted at:** 2026-02-23T~11:47Z pre-Commit-B (Code-A already landed)

**State bundle — master at seal-tail HEAD:**
- **Path:** `continuity_bundles/state_20260923T115815Z_CP_AIP_10.bundle`
- **Size:** 217,420,678 bytes (207.4 MiB)
- **sha256:** `137e04215dad2f20de0185ca986e3e31a22defa3bd4171c417f15e99171b523d`
- **Refs:** `refs/heads/master` → `53f0bfb1478903335beb3c5f7a6c0f39e9c276e5` (= CP-AIP-10 state Commit-C fixup HEAD · the seal's state-tail before mini-bank)
- **Verify:** `git bundle verify` → "is okay" · **records a complete history** · hash algorithm: sha1
- **Emitted at:** 2026-02-23T~11:58Z post-Commit-C-fixup
- **Pin lock-in:** this state mini-bank commit finalizes both bundle pins (this file · same commit).

**One-sentence protected objective:** the sealed record survives its environment (pod crash, session compaction, audit-inbox rotation) without depending on push credentials or repo visibility.

### 3-repo HEADs at seal boundary (pre-mini-bank tip · State-B in flight)

- **Code (programme/track-a):** `8ef25c10ba28fbf09255396281a619a4be819612` (Code Commit-A — CP-AIP-10-TRAINING-RUNS)
- **State (master):** `0684f5977c1b3d69bd42a6a5ff88a54ce27b7f9c` (CP-AIP-9 state mini-bank · pre-CP-AIP-10 State-B tip · Commit-B lands next)
- **/app (main):** `a47b3ab038f7771011b158a1621bafe7d4d01b9b` (/app Commit-A companion of Code-A)

### Post-seal ratchet + baseline pin (measured)

- **Ratchet floor post-seal:** `6321` (was `6313` pre-CP-AIP-10 · +8 canonical measured AIP v1.0 §11.6 P189a + §11.6 P190a-e + §11.5 P185a + §11.5 P187 + Ruling (b) verbatim pod-never-data-path + §1.2 no-redeclaration + §1.4 heavy-fine-tune-deferred-posture).
- **`baseline_failures.json` sha256 post-bump:** `0c7968cdf19694f301e67dc28fee7180e693b0e1f7053fbd3e8226fef5490abd`.
- **Double-green sweep stripped_sha256:** `92d09b7d7f27897fdc7827bbcde23f584cdcb46c3f8be56f4cb23e150ecc7378` IDENTICAL sweep_A (~201s) + sweep_B (~198s) both 6330 passed / 13 skipped / 0 failed / 520 warnings / 12458 stripped bytes.

### Ruling (b) AKKI-RUNS-IT posture markers (this-seal)

- `POD_IS_NEVER_DATA_PATH_POSTURE` Final marker present in `training_run_boundary_v1` per owner Ruling (b) verbatim 2026-02-23.
- `HEAVY_FINETUNE_DEFERRED_TO_COMMISSIONED_JOB_POSTURE` Final marker present per §1.4 measured cost/compute receipt discipline.
- `register_training_run_as_census_autonomy_job` boundary structurally refuses `pod://` and `/app/` prefixed refs.

### Milestone-seal REPORT-AND-CONTINUE receipt line (this-seal · FINAL post-mini-bank)

`CP-AIP-10 seal COMPLETE · code bundle sha256 48b2c169e5d04985f1754ff17d9ca0ce9688bd9c6067ba1dc9ca1252c7b08a41 (18.3 MiB · programme/track-a @ 8ef25c1) · state bundle sha256 137e04215dad2f20de0185ca986e3e31a22defa3bd4171c417f15e99171b523d (207.4 MiB · master @ 53f0bfb1) · SO §6.9(5) AMENDED bundle-based continuity 2nd application LANDED · AIP v1.0 §11.6 Training-Runs commissioned-job compose-boundary GREEN + §11.5 per-example-provenance-through-training enforced structurally + Ruling (b) AKKI-RUNS-IT verbatim Census-Autonomy-Service-registration-seam + pod-never-data-path structural refusal + heavy fine-tune DEFERRED to commissioned-job per §1.4 measured cost/compute receipt · training_run_boundary_v1 §1.2 modality-extension composing sealed CP-AIP-8 S&R + sealed CP-AIP-7 planner + sealed CP-M6-7-3 CostQuoteWithCI + sealed CP-AIP-4 pretraining_contract_v1 posture pattern · 8 RED-first invariant pins ALL GREEN post-authorship · Ratchet 6313 → 6321 · double-green stripped_sha256 92d09b7d7f27897fdc7827bbcde23f584cdcb46c3f8be56f4cb23e150ecc7378 IDENTICAL both sweeps · GAPS_FIXED_LEDGER 8 invariant-seat entries additive at CP-AIP-10 boundary · 0 honest-gaps opened · Sealed carriers UNCHANGED per SO §3.8 additive-only · CP-AIP-10 LAST BY CONSTRUCTION for AIP-plane · REPORT-AND-CONTINUE into Item 5.11 wave (SO-6.9-LID · ENT-16 seeds · census three waves · tenant separation · Track-4 autonomy wiring · CP-AIP-ASSIST-CENSUS · CP-AIP-ASSIST-TRAINING · OWNER_RETURN_REPORT + BUILD_JOURNAL as FINAL deliverable) per RUN-TO-COMPLETION mandate 2026-02-23 · HALT ONLY on SPEC-CONFLICT-<n> · hard custody/gate violation · completion.`

### CP-AIP-10 5-commit seal chain (FULL SHA TABLE · POST-MINI-BANK)

| # | Commit | SHA | Branch | Purpose |
|---|---|---|---|---|
| 1 | Code Commit-A | `8ef25c10ba28fbf09255396281a619a4be819612` | `programme/track-a` | 1 new module `training_run_boundary_v1.py` (~347 lines) + 8 RED-first pins + baseline_failures ratchet 6313→6321 + drill receipts |
| 2 | /app companion A | `a47b3ab038f7771011b158a1621bafe7d4d01b9b` | `main` | notes/audit ORCH_BOOT pre-Commit-A regen 6313→6321 + Extraction-Akki gitlink advance 30f8ccd→8ef25c1 + code bundle emitted |
| 3 | State Commit-B | `5780899b997ae1cd3ef81691fb9297146fbaa365` | `master` | Objective card promoted + queued-delete + ASSIST cards restored to queued/ + comprehensive receipt + GAPS_FIXED_LEDGER 8 entries + PINS CP-AIP-10 pin block + EXECUTION_ORDER Item 5.10 IN-FLIGHT + DECISIONS opening |
| 4 | State Commit-C fixup | `53f0bfb1478903335beb3c5f7a6c0f39e9c276e5` | `master` | R-6 boundary regen advancing heads_last_sealed to State-B + Code-A + state mini-bank rows 1-3 |
| 5 | /app companion C | `2ce6309ab353859b4274eb9237ea4a8f1f138e47` | `main` | byte-identical audit twin mirror of State-B + State-C fixup + vendored/extraction_akki/MANIFEST.json advance (file_count 1059→1060 · training_run_boundary_v1.py added) |
| 6 | State mini-bank | *(this commit)* | `master` | RESUME rewrite + PINS state-bundle-pin final + full 5-commit SHA table + milestone-seal REPORT-AND-CONTINUE receipt line |

<!-- CP-AIP-10-PINS-2026-02-23 END -->


## CP-SO-6.9-LID-WAVE · **SEAL BOUNDARY 2026-02-23T~12:30Z · SO §6.9 LID RATIFICATION verbatim**

<!-- CP-SO-6-9-LID-WAVE-PINS-2026-02-23 BEGIN · SO §6.9(5) AMENDED bundle-based continuity · 3rd application -->

### Milestone-seal continuity bundle pins (SO §6.9.5 AMENDED 2026-02-23 · bundle-based)

**Code bundle — programme/track-a at Code Commit-A HEAD (this-seal · 3rd bundle application):**
- **Path:** `continuity_bundles/code_20260923T122933Z_CP_SO_6_9_LID_WAVE.bundle`
- **Size:** 19,235,396 bytes (18.3 MiB)
- **sha256:** `c312d8cfcf611f59e8d3008df7be5cc27569d867931b1837dfe43ffb4def193f`
- **Refs:** `refs/heads/programme/track-a` → `d4eae498984abd7da16b1d36692178f513ad10b5` (= CP-SO-6.9-LID-WAVE Code Commit-A HEAD)
- **Verify:** `git bundle verify` → "is okay" · complete history · hash algorithm: sha1
- **Emitted at:** 2026-02-23T~12:29Z pre-Commit-B (Code-A already landed)

**State bundle — master at seal-tail HEAD:**
- **Path:** *(pending emission at post-Commit-C-fixup boundary · to be sha-pinned by state mini-bank commit)*

### LID model registration acts (SO §6.9 LID RATIFICATION §4 verbatim)

| Model entry | Licence | Weight sha256 | Licence file | Pull provenance |
|---|---|---|---|---|
| `whisper-lid-v1-mit` | MIT | `[pinned at Track-4 pull]` | `phase0/lid_registration_20260223/licences/whisper_lid_MIT.txt` | `phase0/lid_registration_20260223/pull_provenance/whisper_lid.json` |
| `speechbrain-voxlingua107-apache-2-0` | Apache-2.0 | `[pinned at Track-4 pull]` | `phase0/lid_registration_20260223/licences/voxlingua107_APACHE_2_0.txt` | `phase0/lid_registration_20260223/pull_provenance/voxlingua107.json` |

**Weight-file pulls DEFERRED** to Track-4 Census Autonomy Service jobs per Ruling (b) AKKI-RUNS-IT verbatim — pod is NEVER training host or data path. Anti-token pull wrapper (`HuggingFacePullWrapperAntiToken_v1`) structurally refuses any bearer-like header; env scrubbed of `HF_TOKEN` / `HUGGINGFACEHUB_API_TOKEN` / `HUGGING_FACE_HUB_TOKEN` before headers built (SO §6.9 clause 3).

### Admission gate + TENANT-LABELS status

- **DEFAULT_THRESHOLD_PENDING:** `0.90` tagged `pending` (owner may retune before promotion).
- **Ground truth corpus:** `google-transcripts/datasets/{kik,ebu,swa,luo,kln,guz,mer,bxk,kam,mrg,lwg,mas}/{audio,transcript}` (12-language labelled).
- **TENANT-LABELS-PENDING RESOLVED** for: kik, ebu, swa, luo, kln, guz, mer, bxk, kam, mrg, lwg, mas (12 languages).
- **TENANT-LABELS-PENDING RETAINED** as honest-gap for: **English + Sheng + code-switched** (3 languages) per SO §6.9 LID RATIFICATION §5-§6.

### Rejected options bookkeeping (per owner drop §7 verbatim)

- **fastText LID.176** → `WAITING-ON-TRANSCRIPTS` (parked, NOT registered).
- **Silero language classifier** → `LICENCE-REVIEW-REQUIRED C5.4` (parked, NOT registered).

### 3-repo HEADs at seal boundary (pre-mini-bank tip · State-B in flight)

- **Code (programme/track-a):** `d4eae498984abd7da16b1d36692178f513ad10b5` (Code Commit-A — CP-SO-6.9-LID-WAVE)
- **State (master):** `d7319fee58e0ec7eba3ea190dabe74380355319e` (CP-AIP-10 state mini-bank · pre-CP-SO-6.9-LID-WAVE State-B tip · Commit-B lands next)
- **/app (main):** `0e90b8c3dcef0bb5b2169cd2d6ce0eb492bf1059` (/app Commit-A companion)

### Post-seal ratchet + baseline pin (measured)

- **Ratchet floor post-seal:** `6332` (was `6321` pre-CP-SO-6.9-LID-WAVE · +11 canonical measured).
- **`baseline_failures.json` sha256 post-bump:** `468340729cd16eb9f544453f4d18e33a6069cce79b1ec3aa638975daa20ce314`.
- **Double-green sweep stripped_sha256:** `b71bead1574966208bf999b2f59477324c7f0c8c20381ce98d6ecccc2240650a` IDENTICAL sweep_A (~199s) + sweep_B (~200s) both 6341 passed / 13 skipped / 0 failed / 520 warnings / 12458 stripped bytes.

### Milestone-seal REPORT-AND-CONTINUE receipt line (this-seal · state bundle pin pending mini-bank)

`CP-SO-6.9-LID-WAVE seal 5-commit chain IN FLIGHT (Code-A + /app-A landed · State-B in progress) · SO §6.9 LID RATIFICATION verbatim §1-§9 · Whisper-LID MIT + VoxLingua107 Apache-2.0 registration acts (6-field verbatim shape) + OverlayLidDetection_v1 marker/regime structural invariants + LID_DO_NOT_FLOW_INTO_COUNTED_MEASURE_POSTURE Final marker (B5.4) + admission gate DEFAULT ≥ 0.90 pending scored against google-transcripts/ 12-language labelled corpus + regime promotion by receipted act canon 8 §4 W2 + LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE Final marker + anti-token HF pull wrapper SO §6.9 clause 3 + TENANT_LABELS_PENDING_HONEST_GAP English/Sheng/code-switched + 12 languages RESOLVED · lid_wave_overlay_and_admission_v1 §1.2 modality-extension of sealed CP-M6-1-1 language_identifier.py · code bundle sha256 c312d8cfcf611f59e8d3008df7be5cc27569d867931b1837dfe43ffb4def193f (18.3 MiB · programme/track-a @ d4eae498) · state bundle emission pending post-Commit-C-fixup · SO §6.9(5) AMENDED continuity 3rd application · Additive-only per SO §3.8 · Ruling (b) AKKI-RUNS-IT verbatim honored — E1 wires seam; weight-file pulls DEFERRED to Track-4 Census Autonomy Service jobs · REPORT-AND-CONTINUE not idle-halt per §6.9 cadence amendment · RUN-TO-COMPLETION mandate ACTIVE 2026-02-23.`

### CP-SO-6.9-LID-WAVE 5-commit seal chain (IN FLIGHT · partial · full table lands at mini-bank)

| # | Commit | SHA | Branch | Status |
|---|---|---|---|---|
| 1 | Code Commit-A | `d4eae498984abd7da16b1d36692178f513ad10b5` | `programme/track-a` | ✅ LANDED (2026-02-23T~12:30Z) |
| 2 | /app companion A | `0e90b8c3dcef0bb5b2169cd2d6ce0eb492bf1059` | `main` | ✅ LANDED (2026-02-23T~12:35Z) |
| 3 | State Commit-B | *(this commit)* | `master` | 🟡 IN PROGRESS |
| 4 | State Commit-C fixup | *(pending)* | `master` | 🟡 PENDING |
| 5 | /app companion C | *(pending)* | `main` | 🟡 PENDING |
| 6 | State mini-bank | *(pending)* | `master` | 🟡 PENDING |

<!-- CP-SO-6-9-LID-WAVE-PINS-2026-02-23 END -->

