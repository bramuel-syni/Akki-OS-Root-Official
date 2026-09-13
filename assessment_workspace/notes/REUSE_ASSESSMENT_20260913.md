READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# REUSE_ASSESSMENT_20260913.md

**Standing.** Supersession-form delta over `/app/assessment_workspace/REUSE_ASSESSMENT.md` (Aug-14, 53,479 B, ACCEPTED per PINS.md). Aug-14 original preserved unchanged. This file records what the M0 canon-delta extraction changed about the classification matrix, WITHOUT rewriting the 585-row Chunk-3 table.

**Precedence.** Where this delta conflicts with Aug-14, this delta governs (rows added post-Aug-14). Where silent, Aug-14 governs.

**Scope of delta.** M0 (2026-09-13) extractions covered 12 canon-family docs beyond the original 9 pack + Addendum 1 + Agent-Containment. This file lists rows that MUST be added or modified in the eventual `REUSE_ASSESSMENT_v2.md` full-refresh, but does NOT execute that refresh (deferred per Q2 supersession-form disposition).

---

## §A · NEW REUSE rows implied by M0 extractions

For each newly-extracted requirement row from `notes/canon_*_requirements.md`, the eventual REUSE_ASSESSMENT_v2 must classify as one of {REUSE / MODIFY / RE-POINT / BUILD / RETIRE}. Below is a **triage-only** verdict list — evidence-backed but not the final Chunk-3 row. `[framing, not canon]` on each recommended class.

### A.1 · DAP-Spec (DAP-1..DAP-38, +DAP-31+/32+/A5.7+)

All 40 rows are **BUILD** — no existing implementation in the 4 named repos or in Extraction-Akki `programme/track-a` beyond the untracked 2A scaffolding (`contracts/dap.py`, `services/dap/admission.py`, test file). REUSE candidates:
- **DAP-6** (browse aggregates): REUSE from `services/mtafiti/census_engine` — census surface already lands.
- **DAP-7** (chokepoint pull seam): REUSE from `services/chokepoint`.
- **DAP-8** (Solva assertion floor): REUSE from `services/solva_v2/assertion_boundary.py` (W-SOLVA-V2-LIFT close · commit `7f6d235a`).
- **DAP-18** (objective freeze): REUSE from `services/work_supervisor/job_manifest` (W1 close · commit `fe01e5e`).
- **DAP-21** (metering to Ledger): REUSE from `services/northena/ledger_writer.py` (W-Northena close).
- **DAP-27** (suspension): REUSE from `services/watch/persistence.py` A5.3 pattern.
- Rest (DAP-1..DAP-5, DAP-9..DAP-17, DAP-19..DAP-20, DAP-22..DAP-26, DAP-28..DAP-30) — **BUILD**.

### A.2 · Serving Integrity Amendment (V-1..V-4, S-27, AC-13/14, R-13, R-14)

All **BUILD**. NO existing implementation of load-time hash verification or reference validation cadence.
- Composition: SFP-8 sits inside Rules-Service (M2 scope); TCB gate row lands with Attr-1.
- Gate-runner assertion (V-2) will REUSE M1 chokepoint refuse-if-unset pattern (FP-2 platform-wide) — no new gate primitive needed.

### A.3 · TCB Enumeration (27 rows + 1 UNDETERMINED)

Every IN row exists as service scaffolding or full implementation:
- **REUSE**: SyniSense chokepoint, Solva assertion seam, Northena objective-freeze, Mtafiti registry, Targeta/MOAC, Ledger writer, Rules Service ceremony engine, Whitepaper Wizard Tier-3 eligibility, Connect Wizard rights-recording, DAP release/distance/output-content gates.
- **BUILD (still)**: Mkondo hand-off registry ("IN pending build") — awaits `handoff_registry_v1` implementation.
- **MODIFY**: DAP-32 admission-integrity probe (trigger-scan SPLIT half) — technique choice needed.
- **RETIRE**: none.

### A.4 · Determinism Inventory (24 rows + Article-14 mapping)

REUSE from `services/*` for all classified rows; **BUILD** for DET-1 (CIF halt-independent-of-Targeta), **BUILD** for DET-2 (Mtafiti classification deterministic confirmation step) — both `DEFAULT-PENDING-OVERRIDE` markers.

### A.5 · Security Architecture Description (SEC-1..SEC-7 + 7 Reference-Monitor property rows)

**BUILD**: SEC-1 (SyniSense integrity-verified-at-load), SEC-2..SEC-5 (MOAC Reference-Monitor properties), SEC-6/SEC-7 (DAP-31/32 secure-initialisation).
**REUSE**: Watch-Mkono ADV_ARC.1 already Met; SyniSense non-bypassability + domain-sep + init already Met.

### A.6 · Security Function Policies (SFP-1..SFP-7, +SFP-8 via SIA)

**REUSE**: SFP-1 (assertion floor via `services/solva_v2`), SFP-4 (custody floor via `services/chokepoint`).
**BUILD**: SFP-2/SFP-3/SFP-5/SFP-6/SFP-7 as named Rules-Service catalog entries. SFP-8 BUILD.

### A.7 · Failure Posture Enumeration (FP-1..FP-4 + 13 per-component rows)

**REUSE**: SyniSense/Solva/Mtafiti/MOAC/Mkondo/Watch/Ledger fail-closed postures are all already documented and behaviourally consistent.
**BUILD**: FP-3 (Mtafiti explicit fail-safe-open declaration), FP-4 (Watch already-active-containments persistence).

### A.8 · Trust Domain Description (TD-1..TD-3 + 4 boundary rows)

**REUSE**: TD-2 already inherent in appliance model; TD-3 already covered by DAP-5.
**BUILD**: TD-1 platform-domain enumeration; explicit invariant on "no Tenant↔External-Party direct path".

### A.9 · Business Continuity Annex (S-10 · S-11 · BC-1..BC-4)

**BUILD** (fresh): S-10 recovery mechanism (RTO 3600s), S-11 notification (72h), BC-1 independent countersigner, BC-2 quarterly cadence.
**DEFAULT-PENDING-OVERRIDE**: BC-3 RPO, BC-4 disaster-scenario disposition.

### A.10 · Hand-Off Generalisation (HR-1..HR-7)

**REUSE**: ThinkLab→Task-Manager crossing already meets HR-1..HR-6 by construction.
**BUILD**: HR-1 registry (owned by Mkondo), HR-7 fail-closed posture.

### A.11 · Pruning/Unlearning Amendment (DAP-37 · DAP-38 · S-26 · R-12)

**BUILD (all)**: DAP-37 pruning path, DAP-38 unlearning path, RBM-20 registry query.
- SISA mechanism dependency — `services/training_runner` currently lacks per-shard training isolation → potential MODIFY row.

### A.12 · Governance Architecture v1 (files_15 delta)

Delta only. R-1/R-3/R-5 flipped RESOLVED in canon; no REUSE/BUILD implications.

## §B · REUSE-classification summary (delta triage)

| Category | Count | Rows |
|---|--:|---|
| **REUSE** (from existing service dirs on `programme/track-a`) | ~28 | Chokepoint, Solva-V2 seam, Northena freeze, Mtafiti registry, MOAC, Ledger writer, Rules-Service ceremony engine, Watch-Mkono, DAP release/distance/output-content gates, WPW eligibility, Connect Wizard rights-recording, ThinkLab handoff, appliance-domain model, most FP rows |
| **MODIFY** (existing service, requires targeted change) | ~5 | DAP-32 trigger-scan SPLIT · SISA per-shard isolation in training_runner · TD-3 vs DAP-5 supersession · A5.7+ receipt extension · A5.16 recommendation-window wiring |
| **RE-POINT** (existing code, wrong location) | 0 | none identified in this delta |
| **BUILD** (fresh) | ~60 | Full DAP-1..DAP-38 + SIA V-1..V-4 + SFP-2/3/5/6/7/8 + SEC-1..SEC-7 + FP-3/FP-4 + BCA S-10/S-11/BC-1..BC-4 + HR-1..HR-7 + DET-1/DET-2 |
| **RETIRE** (retire an existing row) | 0 | none |

## §C · Deferred to full refresh

- Row-level Chunk-3 classification (585-row spine) is NOT re-run in M0 — that is a Phase-2-block operation once M1..M5 opens.
- BUILD_STRATEGY delta lives at `notes/BUILD_STRATEGY_20260913.md` (siblings this file).
- Master requirements registry cross-walk (Q1 delta-only scope) — deferred.

## §D · Standing

Aug-14 `REUSE_ASSESSMENT.md` remains the canonical reference until the eventual `REUSE_ASSESSMENT_v2.md` full-refresh replaces both. This delta is the audit trail of what changed in the corpus between Aug-14 and 2026-09-13.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
