# files (9).zip — inventory + diff vs the nine canons

Source: `fixtures/files_9.zip` (sha256 `d063db00a1f1d83adbeb0498e02c824b2c9529731209a780deb9f24e68f8d3ee`, 262,021 bytes). Unzipped into `fixtures/files_9_extracted/`; full text dump at `/tmp/v7_ingest/files9_dump.txt` (1,385 lines).

## Contents — 16 .docx files, ordered by prefix

| # | Filename (verbatim) | Size (bytes) |
|---|---|---|
| 01 | `01_Custody_and_the_Crossing_Part_1_The_Chokepoint.docx` | 20,363 |
| 02 | `02_Custody_and_the_Crossing_Part_2_Confidentiality_and_Dual_File.docx` | 19,457 |
| 03 | `03_Intent_and_Security_Monitoring.docx` | 22,812 |
| 04 | `04_Reasoning_Grounding_and_the_Solver.docx` | 19,932 |
| 05 | `05_Direction_Scope_and_Focus_Part_1_Northena.docx` | 17,249 |
| 06 | `06_Direction_Scope_and_Focus_Part_2_Progressive_Disclosure.docx` | 15,154 |
| 07 | `07_Context_Preservation_Part_1_Shrinkage.docx` | 15,156 |
| 08 | `08_Context_Preservation_Part_2_Memory_and_Retrieval.docx` | 16,203 |
| 09 | `09_Estate_Registry_Part_1_Connection_and_Census.docx` | 18,382 |
| 10 | `10_Estate_Registry_Part_2_Comprehensive_Registry.docx` | 15,309 |
| 11 | `11_Cost_and_Compute_Part_1_Local_First_and_Levers.docx` | 18,411 |
| 12 | `12_Cost_and_Compute_Part_2_Locality_and_Transparency.docx` | 16,351 |
| 13 | `13_Targeting_Training_Part_1_Autonomous_Training_and_Shaping.docx` | 18,050 |
| 14 | `14_Targeting_Training_Part_2_Model_Ecosystem.docx` | 18,639 |
| 15 | `15_Platform_Orchestration_and_Governance_Ceremony.docx` | 21,006 |
| 16 | `16_Cross_Cutting_Orchestration.docx` | 23,358 |

## Diff against the previously-held nine canons

The nine canons already inventoried (Chunk-1, `notes/canon_{1..9}_requirements.md`) are the umbrella-titled documents:

| Canon slot | Umbrella title (Chunk-1) |
|---|---|
| Canon 1 | Akki — The Custody Platform |
| Canon 2 | The Conditioned Ideation Faculty |
| Canon 3 | Akki Governance Engines |
| Canon 4 | Akki Operating Engines |
| Canon 5 | Akki Interface Architecture |
| Canon 6 | Akki User Journeys |
| Canon 7 | Integration Service and Quality Rulebook |
| Canon 8 | The Watch |
| Canon 9 | The Mkondo Charter |

The files (9).zip package is a **different corpus with the same subject matter** — 16 numbered essays that partition the same territory more granularly. Cross-referencing the AKKI_Promise_Table.xlsx's "Doc" column (which points to Docs 1–16) confirms **this 16-doc corpus IS what the Promise Table cites** — not the umbrella nine.

**Mapping the 16 essays onto the nine canons (best-fit, based on titles + first-paragraph reads):**

| Essay | Best-fit umbrella canon | Notes |
|---|---|---|
| 01 Custody & Crossing Pt 1 (Chokepoint) | Canon 1 (Custody Platform) | Doc 1 — Chokepoint, masked crossings, receipts (Promise #1 primary source) |
| 02 Custody & Crossing Pt 2 (Confidentiality & Dual File) | Canon 1 | Doc 2 — DPO declaration + two-item dual-file custody (Promises #2, #4) |
| 03 Intent and Security Monitoring | Canon 3 or Canon 8 | Doc 3 — The Watch / Grey Mirror mechanism (Promises #6, #7) |
| 04 Reasoning, Grounding, and the Solver | Canon 4 or Canon 2 | Doc 4 — Solva, evidence floor, reasoning trace (Promises #8, #29, #31) |
| 05 Direction, Scope, Focus Pt 1 (Northena) | Canon 4 | Doc 5 — Northena, Admit/Gate/Converge/Ledger (Promise #16, #18) |
| 06 Direction, Scope, Focus Pt 2 (Progressive Disclosure) | Canon 4 | Doc 6 — Minimal-sufficient context (Promise #17) |
| 07 Context Preservation Pt 1 (Shrinkage) | Canon 4 | Doc 7 — Five-ring normalised unit (Promise #19) |
| 08 Context Preservation Pt 2 (Memory & Retrieval) | Canon 4 | Doc 8 — Warm/fresh fork, targeted retrieval (Promises #20, #21) |
| 09 Estate Registry Pt 1 (Connection & Census) | Canon 5 or Canon 1 | Doc 9 — Connect wizard, census, per-source profile (Promises #12, #13, #15) |
| 10 Estate Registry Pt 2 (Comprehensive Registry) | Canon 5 | Doc 10 — Estate table, Opportunity Briefs, linkages (Promise #14) |
| 11 Cost & Compute Pt 1 (Local-First & Levers) | Canon 4 or Canon 1 | Doc 11 — Cost ladder, deflation law (Promise #9) |
| 12 Cost & Compute Pt 2 (Locality & Transparency) | Canon 1 | Doc 12 — In-perimeter execution, reflection-before-commit (Promises #10, #11) |
| 13 Targeting/Training Pt 1 (Autonomous Training) | Canon 4 or Canon 6 | Doc 13 — Targeta, six-criterion acceptance (Promises #22, #23) |
| 14 Targeting/Training Pt 2 (Model Ecosystem) | Canon 4 | Doc 14 — Baseline curation, exceptional runs, LLM market (Promises #24, #25, #30) |
| 15 Platform Orchestration & Governance Ceremony | Canon 3 or Canon 9 | Doc 15 — Watch exception, ceremony taxonomy, handoff (Promises #26, #27, #32) |
| 16 Cross-Cutting Orchestration | Canon 5 or Canon 6 | Doc 16 — Composite claims (Promises #5, #29) |

## Verdict

- The 16 essays are a **more granular decomposition** of what the umbrella nine canons already cover — no new subject matter is introduced.
- The Promise Table cites the **essays by number (1–16)**, not the umbrella canons.
- The Canon Addendum (fourth artifact this drop) speaks the **same essay-numbered language** ("Amendment to Document 4, Promise #8" etc.), so the essays are the effective canon-of-record for this cycle, with the umbrella nine covering the same territory at a coarser grain.

**Practical binding:** every requirement extracted from the umbrella nine in Chunk-1 still holds; the 16 essays extend/refine some of them. A prudent Chunk-3 assessment should double-index — reference the essay number alongside the umbrella canon number.

**No new canon-class material** is introduced by this zip. New canon material arrives via the separate Canon Addendum 1 artifact.
