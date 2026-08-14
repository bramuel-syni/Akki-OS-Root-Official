# Chunk 1 — Summary and Entry Point

Session: canon ingest + repo ingest + prototype inventory. NO production
code written in any repo. Every file below is under
`/app/assessment_workspace/`.

## Deliverables produced (durable — Chunks 2/3 depend on these)

- `notes/repo_summaries.md` — repo table, file-type counts, top-level trees, `backend/services/` listing per repo, BUILD_JOURNAL/close_reports/audits presence.
- `notes/cross_repo_overlap.md` — presence matrix, per-service delta measurements (file counts, LOC, per-path last-commit dates), identical-across-3-cores group, `synisense`-in-4-repos analysis, single-repo services.
- `notes/canon_1_requirements.md` — 75 rows.
- `notes/canon_2_requirements.md` — 66 rows.
- `notes/canon_3_requirements.md` — 61 rows.
- `notes/canon_4_requirements.md` — 68 rows (MOAC criteria C4-037a–f enumerated as sub-rows).
- `notes/canon_5_requirements.md` — 70 rows.
- `notes/canon_6_requirements.md` — 62 rows.
- `notes/canon_7_requirements.md` — 35 rows + 26 defect-class rows (D-taxonomy).
- `notes/canon_8_requirements.md` — 72 rows.
- `notes/canon_9_requirements.md` — 50 rows.
- `notes/prototype_inventory.md` — nav constants, screen inventory, component fabric, Canon-5 gap notes.
- `notes/_raw_*` files (repo trees, services listing, service diffs) — data these notes were compiled from.
- `tools/*.py` — small analysis scripts (extract_docx, repo_tree, services_overlap, service_diff, file_type_table).

## Row ID scheme (stable through Chunk 3)

- `C1-###` … `C9-###` — canonical requirement id per canon.
- `C7-D##` — defect classes from the Quality Rulebook.
- `C4-037a … C4-037f` — MOAC sub-criteria.

Chunk-3's REUSE_ASSESSMENT.md will use these IDs as row keys.

## Repo pinned SHAs (do not re-clone; re-check against these)

| Repo | Pinned HEAD SHA | Branch | Last commit ISO |
|---|---|---|---|
| RMS-IQ-Core-2 | `ea5aa019521eee22ad4f8ea29efdfa2af357be3b` | `main` | 2026-08-01T08:10:07+00:00 |
| Akki-OS-V1 | `8c361903cdd319bfdc0709de3f4392f5bfa3956b` | `main` | 2026-08-14T05:30:51+00:00 |
| Extraction-Akki | `b150c21c1ac6fae8d052332aaff56ae952daae25` | `main` | 2026-08-14T05:27:40+00:00 |
| Akki-Executive-Core | `5844eee95d5faffea0dcab98bd4fe5e8d1419f32` | `main` | 2026-07-08T13:46:49+00:00 |

## Explicit non-findings / open items for Chunk 3

- Canon-5 conformance SCORING is deferred (Chunk 3). This chunk only inventories the prototype and lists obvious gaps.
- REUSE / MODIFY / RE-POINT / BUILD / RETIRE assignment against each of the 585+ requirement rows is deferred.
- Verification of BUILD_JOURNAL / close-report / audit CLAIMS (as opposed to their presence) is deferred.
- Interpretation of which of the four repos is "authoritative" for any service is deferred — only measurement done here.
- `Akki-Executive-Core` operates on a materially different service surface and lacks BUILD_JOURNAL/close_reports/audits; when Chunk 3 assigns rows it must diff both `synisense` implementations and treat the rest of Executive-Core as a separate assessment lane.

## Method disclosures

- All docx→text extraction via `python-docx` (`tools/extract_docx.py`). Tables rendered as pipe-separated rows so nothing is silently dropped. Paragraph styles preserved as `[Style]` prefixes.
- All cross-repo overlap comparisons use SHA-256 file content hashes and `git log -1 --format=%cI -- <path>` for per-path last-commit dates. No content-similarity heuristics.
- All prototype facts extracted by direct string search over `prototype.html`. The bundle is a single-file self-unpacking application; all state lives in inline JS constants.
- No file inside any of the four repos was modified.
