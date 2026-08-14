# NEXT.md — Exact next actions

**Last updated:** 2026-08-14, after Ruling 2.

## Cold-reader-executable next actions

Anyone reading this without memory of the session executes the following in order.

### 1. Enumerate work items — DONE

`/app/assessment_workspace/notes/row_to_item_index.md` written and updated with Ruling-2 promotions (4 new WIRING items). 591 canon rows mapped, 89 items total (34 Part-1, 55 Part-2), 0 named gaps.

### 2. Estimation discipline — DONE

Defined once at top of `/app/assessment_workspace/notes/strategy_items_part1.md` per Ruling 2 §1. Hard thresholds:
- S = 1 component, 0 new contracts, ≤1 integration surface.
- M = 1-2 components, OR 1 new/changed contract, ≤2 integration surfaces.
- L = 3+ components, OR new register/console, OR a data migration.
- XL = new engine/authority, OR estate-wide wiring.
Every XL carries one-paragraph defence.

### 3. Draft Part-1 item tables — IN PROGRESS

`/app/assessment_workspace/notes/strategy_items_part1.md` — 47 items in classes MODIFY / PARTIAL / RE-POINT / HARVEST / RETIRE / RENAME / WIRING / REBUILD / CONTRADICTION (Ruling 3 raised the count from 34 → 47 via interface reclassification). Seven fields per item. §I contains the Extraction-Akki menu-to-app mapping table.

### 4. Fidelity ledger — IN PROGRESS

`/app/assessment_workspace/notes/fidelity_ledger.md` — opens alongside Part 1, appended during Part 2, frozen at assembly.

### 5. Draft Part-2 item tables (BUILD, 55 items covering 148 rows) — LATER CHUNK

Do NOT start Part 2 in this chunk. Wait for owner sign-off on Part 1 shape first.

### 6. Citation audit

Before any submission: run `/app/assessment_workspace/tools/citation_audit.py`. Latest run: **102/102 file citations verified · 814/854 canon citations verified · 40 failed (all inherited Chunk-1 drift, disclosed in `fidelity_ledger.md` FL-P1-20)**. Fix by re-reading source, never by silent deletion. A systematic re-mapping pass is recommended.

### 7. Update STATE/ at every material step

Rule (Ruling 1 preamble effect): STATE/ files are updated AFTER each ruling received, each section drafted, each finding. An out-of-date STATE/ = "not having lawfully happened."

### 8. Deliverable path

Final Chunk-4 deliverable: `/app/assessment_workspace/BUILD_STRATEGY.md` — assembled from the two `strategy_items_part[12].md` files + this state pack + Rulings 1-2 + `fidelity_ledger.md`.
