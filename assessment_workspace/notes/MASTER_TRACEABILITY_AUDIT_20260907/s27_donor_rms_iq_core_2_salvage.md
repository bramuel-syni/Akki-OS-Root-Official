# S27 · Donor · RMS-IQ-Core-2 salvage briefs · Detail Classification

**Repo:** `/app/assessment_workspace/repos/RMS-IQ-Core-2/` · HEAD `ea5aa019` (main, 2026-08-01) · 198 total commits.
**Coverage:** salvage briefs from mid-2026 retirement waves. Owner directive "scan what wasn't" — these were previously listed as file paths in `notes/repo_summaries.md` but NEVER mined for requirement content.

## §A · Salvage catalog (11 files · 3 salvage waves)

### A.1 · dispatch_v2 retirement (2026-07-31 · 8 files)

| Row ID | File | Anchor | Classification |
|---|---|---|---|
| A27-1 | `salvage/dispatch_v2_retirement_2026-07-31/RETIREMENT_NOTE.md` | Retirement rationale for dispatch v2 | INVENTORY (retirement claim) |
| A27-2 | `salvage/dispatch_v2_retirement_2026-07-31/AKKI_OS_FRONTEND_BRIEF_v2.md` | Frontend brief v2 · full spec | REUSE (feeds v2 prototype surface work) |
| A27-3 | `salvage/dispatch_v2_retirement_2026-07-31/AKKI_OS_SURFACES_v2_AMENDMENT.md` | Surfaces v2 amendment | REUSE |
| A27-4 | `salvage/dispatch_v2_retirement_2026-07-31/frontend_brief_v2_missing_2026-07-30.md` | Frontend brief · missing bits list | REUSE |
| A27-5 | `salvage/dispatch_v2_retirement_2026-07-31/frontend_brief_v2_intake_summary_2026-07-31.md` | Intake summary | INVENTORY |
| A27-6 | `salvage/dispatch_v2_retirement_2026-07-31/phase3_subcycle1_owner_rulings_2026-08-01.md` | Owner rulings phase3 subcycle 1 | INVENTORY (rulings must be re-verified against DECISIONS.md) |
| A27-7 | `salvage/dispatch_v2_retirement_2026-07-31/phase3_subcycle2_memory_and_registry_2026-08-02.md` | Owner rulings phase3 subcycle 2 · memory + registry | INVENTORY |
| A27-8 | (implied — dispatch_v2 code retirement) | Retired code | RETIRED |

### A.2 · askconsole retirement (2026-07-31 · 1 file)

| Row ID | File | Anchor | Classification |
|---|---|---|---|
| A27-9 | `salvage/askconsole_retirement_2026-07-31/RETIREMENT_NOTE.md` | Retirement of askconsole surface | RETIRED (source superseded by v2 chat surface C.1 in S23) |

### A.3 · ui1a retirement (2026-07-31 · 1 file)

| Row ID | File | Anchor | Classification |
|---|---|---|---|
| A27-10 | `salvage/ui1a_retirement_2026-07-31/RETIREMENT_NOTE.md` | Retirement of ui1a surface | RETIRED |

### A.4 · commercial cut (2026-07-06 · 2 files)

| Row ID | File | Anchor | Classification |
|---|---|---|---|
| A27-11 | `salvage/commercial_cut_2026_07_06/MANIFEST.md` | Commercial-cut manifest (retired code paths) | INVENTORY (retirement) |
| A27-12 | `salvage/commercial_cut_2026_07_06/README.md` | Commercial-cut README | INVENTORY |

## §B · Repo-level requirement material outside `salvage/`

| Row ID | Path | Anchor | Classification |
|---|---|---|---|
| A27-B1 | `BUILD_JOURNAL.md` | Repo build journal | Claim-to-verify (per binding rule; see S28) |

## §C · S27 rollup

**Total salvage rows: 12** (11 salvage docs + 1 build journal · Q4 above).

| Bucket | Rows | % of 12 |
|---|--:|---:|
| REUSE | 3 (A27-2, A27-3, A27-4) | 25.0% |
| INVENTORY | 6 | 50.0% |
| RETIRED | 3 (A27-8, A27-9, A27-10) | 25.0% |
| DONE / PARTIAL / NEW | 0 | 0.0% |

**Interpretation:** RMS-IQ-Core-2 salvage is retirement-heavy. The 3 REUSE items (`AKKI_OS_FRONTEND_BRIEF_v2.md`, `SURFACES_v2_AMENDMENT.md`, `frontend_brief_v2_missing_2026-07-30.md`) are the pre-v2-prototype design intent documents; they anchor the surface list superseded by SURFACE_AUDIT_v2 (S23).

**Rulings sub-cycle 1 + 2** (A27-6, A27-7) contain owner rulings from 2026-08-01 and 2026-08-02 that were never explicitly re-verified in `STATE/DECISIONS.md`. **This is a coverage-ledger finding:** these rulings should be cross-checked against DECISIONS.md; any missing = a supersession finding.

**Wave:** **W-VERIFY-RMS-SALVAGE-RULINGS** (S effort) — cross-reference A27-6, A27-7 owner rulings against `STATE/DECISIONS.md` to confirm all rulings are banked verbatim; any unbanked ruling is a supersession record to add.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
