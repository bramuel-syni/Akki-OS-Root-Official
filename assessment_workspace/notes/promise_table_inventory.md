# AKKI_Promise_Table.xlsx — inventory

Source: `fixtures/AKKI_Promise_Table.xlsx` (sha256 `02817f8a0f637e7af98f1266b2b0423e179387ebb13a75bf77fc92ad7d0c233b`, 24,534 bytes). Read via `openpyxl`; full dump at `/tmp/v7_ingest/promise_table_dump.txt` (62 lines).

## Sheet 1 — "Canon Promises" (32 rows × 7 columns)

Columns: `#`, `Doc`, `Promise`, `Implementation Status`, `Where It Lives / Notes`, `System Features`, `User Requirements — User can…`.

**32 rows: 1 header + 31 canon promises** — the 31 promises the platform makes as extracted verbatim from Documents 1–16, with each row's build-side status classified. Status distribution:

- **Present:** #1, #3, #6, #7, #8, #10, #11, #12, #13, #14, #15, #16, #18, #22, #23, #29 = **16**
- **Present (strong):** #22, #27, #31 = **3** (subset of Present)
- **Partial:** #2, #9, #32 = **3**
- **Partial → completed:** #30 = **1**
- **Absent → added:** #4, #17, #19, #20, #21, #24, #25, #26 = **8** (these are the ones the Canon Addendum §1 confirms as build-only closures)
- **By design:** #5, #29 (as "Composite claims") = **2**

Row map (`#` → `Doc`):
| # | Doc | Promise (one-line synopsis) |
|---|---|---|
| 1 | 1 | Confidential material never leaves in exposable form |
| 2 | 2 | DPO declares confidentiality without engineering help |
| 3 | 1 | Purpose survives redaction |
| 4 | 2 | Two-item custody split (never one merged blob) |
| 5 | 16 (composite) | "All data in Akki is safe" — grounded in #1, #6/#7, #18, #27 |
| 6 | 3 | Watch: intended-not-just-allowed, machine-speed containment |
| 7 | 3–4 | Reconciliation of declared vs demonstrated conduct |
| 8 | 4 | Ungrounded assertion boundary + structured refusal |
| 9 | 11 | Local-first cost economics, Cost Ledger |
| 10 | 12 | Compute is brought to the data (in-perimeter) |
| 11 | 12 | Reflection-before-commit: cost & budget at decision time |
| 12 | 9 | Connect to any store without migration |
| 13 | 9 | Honest, dated, method-carrying estate census |
| 14 | 10 | One comprehensive Registry per source + Opportunity Briefs |
| 15 | 9 | Audio as first-class citizen; timestamp-span grounding |
| 16 | 5 | Scope-and-stop discipline; Admit/Gate/Converge/Ledger loop |
| 17 | 6 | Minimal-sufficient context for every step |
| 18 | 5 | Objective is frozen; a change is a new run |
| 19 | 7 | Meaning survives shrinkage into five-ring unit |
| 20 | 8 | Model reads from distilled memory, not raw DB |
| 21 | 8 | Targeted fresh-fetch for what memory doesn't hold |
| 22 | 13 | Six-criterion model acceptance (no human in the path) |
| 23 | 13 | Frame/shape/state/reflect loop before committing training |
| 24 | 14 | Licence-verified baseline curation |
| 25 | 14 | Exceptional-run white paper drafting |
| 26 | 15 | No app operates above governance; Watch is the singular exception |
| 27 | 15 | Rules authored in plain language via open ceremony |
| 28 (#30) | 14 | Reach every LLM under one license (registry + rights posture) |
| 29 (#31) | 4 | Genuine reasoning: tension, load-bearing set, trace |
| 30 (#32) | 15 | Registered handoff contract for cross-app crossings |
| 31 (#29) | 15 (composite) | "Adaptive, superintelligent, yet contained" |

## Sheet 2 — "Beyond Canon (A1–A8)" (9 rows × 4 columns)

Eight items already built in the v7 prototype but NOT written into the nine canons:
- A1 Board 360 (submission traceability)
- A2 Exco 360 (goal/recommendation traceability)
- A3 Documents suite (governed artefact inheritance + Exposure Site Map)
- A4 Rule Books Library (governed template adoption, ISO 27001 Annex A mapped)
- A5 Collab group (universal shielding, HR Stuff aggregate-only)
- A6 Spend Requests (threshold-gated commitment routing)
- A7 ThinkLab → Task Manager (cross-app governed hand-off)
- A8 "Walk this →" (universal claim-to-evidence trace)

The Canon Addendum §3 formalises A1–A8 as new promise candidates with full user-facing text.

## Sheet 3 — "New Promise Candidates" (6 rows × 2 columns)

Five items with no canon presence AND no built instance yet:
1. Retention enforced and attested (not only declared)
2. Time-boxed breach / incident notification path
3. Individual's own access-and-erasure request
4. Explicit data residency / cross-border transfer control
5. Continuity guarantee for the governed record itself

Formalised in the Canon Addendum §3 as **N1–N5**.

## Sheet 4 — "Enhancements" (7 rows × 2 columns)

Six enhancement suggestions (later formalised as Canon Addendum §2 amendments to Docs 2, 4, 11, 13, 15 twice):
- Dry-run preview for #2 declarations (Doc 2)
- Cost Ledger surface for #9 (Doc 11)
- Generalised handoff receipt for #32 (Doc 15)
- Self-expiring "lower the standard" refusal for #8 (Doc 4)
- Standing re-check date per in-service model for #22 (Doc 13)
- Watch staleness-flagging extended to rulebooks/baselines for #27 (Doc 15)

## Reconciliation shape

The Promise Table is a **build-audit register** cross-referencing the 31 canon promises + 8 beyond-canon built items + 5 new candidates + 6 enhancements = **50 rows** the Akki estate must eventually own. It is the seed of what a "Function & Promise Registry" surface (candidate for the next Registry tab) would render.
