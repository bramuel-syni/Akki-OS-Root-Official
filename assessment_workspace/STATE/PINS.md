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

**Pod public egress IP** (for AISCA VM allowlist): **`34.170.12.145`** as of 2026-08-14 stop-order cycle (verified live via ifconfig.me · icanhazip.com · api.ipify.org · checkip.amazonaws.com; no IPv6 egress). Previously pinned as `34.16.56.64` (fidelity-ledger FL-P2-09 OPEN for owner disposition — pod egress has rotated). **The IP `34.16.56.64` remains in `SPINE_ALLOWED_IPS` per owner's strict stop-order directive; pod egress is NOT self-allowlisted.**

**Access mechanism (Owner stop-order 2026-08-14 · minted-credential pattern retired estate-wide).** Source-IP allowlist middleware live on BOTH FastAPI backend and CRA dev-server. Config in `/app/backend/.env`: `SPINE_ALLOWED_IPS` (comma-separated /32s) + `SPINE_TRUSTED_PROXY_HOPS=2`. Refusal grammar: HTTP 403 `text/plain` `"This surface answers allowlisted addresses only."`. Trust boundary: `xff.split(',')[-3]` per empirically discovered Cloudflare-worker + Cloudflare-edge + Google-Cloud-LB topology (FL-P2-10 CLOSED). No shared bearer token exists anywhere on the estate; `spine_auth.py` and `.owner_credentials` retired.

**Two-week checkpoint deadline:** **provisioning day + 14 — AWAITING PROVISIONING DATE** (per Build Order 01 §6). Update this pin to the actual UTC deadline once the VM is provisioned.

**Phase-1 A0/A1 tests-first evidence:** 26/26 gating tests pass (`phase0/A0-A1_report.md` + drill receipt `phase0/drill_receipts/20260814T120336Z_declaration_refusal_firing.log`).

**WS-BUILD-CONNECT-GPU + IP allowlist + re-home gating (Owner stop-order cycle 2026-08-14):** 99/99 total gating tests green on programme/track-a HEAD `acc25a8` = 78 backend python + 12 frontend allowlist node --test + 9 frontend re-home node --test. Right-reason failure receipts banked BEFORE each implementation lands:
- `phase0/drill_receipts/20260814T145500Z_ip_allowlist_right_reason_failure.log` (16/16 tests failed with ModuleNotFoundError before middleware landed).
- `phase0/drill_receipts/20260814T151000Z_rehome_right_reason_failure.log` (6/9 tests failed right-reason before implementation landed).
- Green receipt: `phase0/drill_receipts/20260814T151500Z_lockdown_and_rehome_green.log`.

**Attachment status (2026-08-14 · fixture-arrival cycle):** two of three fixtures delivered as files, third arrived as inline owner transcription. All FIXTURE PENDING markers CLEARED at transcription grade (files below). Governance grade distinction (transcription-cleared vs file-cleared) recorded in `notes/fidelity_ledger.md` FL-P1-14 + FL-P1-14a.

| Fixture | On disk at | sha256 | Grade |
|---|---|---|---|
| Akki Prototype v7 Design Brief | `/app/assessment_workspace/fixtures/Akki_Prototype_v7_Design_Brief.md` (18,791 bytes) | `063f2b470d74dcd30ad43b4645c4e656edaa7fb1185198a4116ad5328a9717b4` | file-cleared |
| AISCA GPU Access Guide | `/app/assessment_workspace/fixtures/AISCA_GPU_Access_Guide.pdf` (535,169 bytes) | `0f6b6e0f692494e18a65df655fddf48f45839005dc7aa6b988239b8f90e157f3` | file-cleared (SOP↔Order §6 conflicts A + B ESCALATED per Q2(a) — see `fixtures/aisca_sop_extraction.md` + FL-P2-03 / FL-P2-04) |
| Reference screenshot | `/app/assessment_workspace/fixtures/reference_screenshot_transcription.md` (owner-inline transcription; original image not yet in workspace) | `d3ae9a6cf598a38333b5c11d6d73dc9069dc3671fb31598f2e594dfb002fc949` | **transcription-cleared** (Q1(c) ruling · 2026-08-14 · re-open on image-file arrival if pixels contradict transcription) |

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
- **commissioning_record:** `/app/assessment_workspace/phase0/commissioning_records/commissioning_aisca-gpu-01_20260814T151243Z.json`
<!-- CONNECT-GPU-PINS -->
