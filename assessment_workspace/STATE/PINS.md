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
- **commissioning_record:** `/app/assessment_workspace/phase0/commissioning_records/commissioning_aisca-gpu-01_20260922T034412Z.json`
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
