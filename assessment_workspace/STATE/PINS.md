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

- `/app/assessment_workspace/tools/citation_audit.py` — mechanical citation checker; must run clean before every deliverable submission. Latest run: **100/100 file · 462/462 canon · 0 failures**.
- Other analysis scripts: `extract_docx.py`, `repo_tree.py`, `services_overlap.py`, `service_diff.py`, `file_type_table.py`.
