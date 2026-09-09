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

Nine `.docx` documents, source archive: `https://customer-assets-v7afamib.emergentagent.net/job_a963bf18-f7d3-42c9-b8dd-aba51af40caf/artifacts/96u2c488_files%20%288%29.zip` (236,005 bytes). Extracted to plain text via `python-docx` at `/app/assessment_workspace/canon/text/`.

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

Prototype: `/app/assessment_workspace/prototype/prototype.html` (v6 Standalone, 626,618 bytes, 395 lines).

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
- **commissioning_record:** `/app/assessment_workspace/phase0/commissioning_records/commissioning_aisca-gpu-01_20260909T125022Z.json`
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
