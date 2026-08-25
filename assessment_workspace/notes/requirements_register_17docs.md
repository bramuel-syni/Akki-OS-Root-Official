# Requirements Master Register · 17 Documents · FL-P2-27

Owner Order 2026-08-19 · Sprint deliverable §2 · Owner ruling T14: "The 17 documents I have attached — 16 in zip and addendum — are updated record of requirements."

## Method

- Row IDs `DocNN-###` where `NN` = essay number (01–16). CA1-xxx amendments are **merged as sub-rows** into their target doc (T7 owner ruling: "Addendum closes/amends the 16 documents … should not be executed as a stand alone").
- Row source: the 9-canon Chunk-1 extraction (`notes/canon_1..9_requirements.md`, 626 total requirement bullets) is the primary text-anchored register. Per the mapping in `notes/files_9_inventory.md` §Verdict, the 16 essays are a **finer-grained decomposition** of what the umbrella nine cover — so the 626 bullets flow into the 16-doc register via the essay↔canon map.
- Status ∈ {**DONE** (built + tested on Extraction-Akki track-a), **PARTIAL** (some behaviour exists, key facet missing), **REUSABLE** (repo/path + reuse grade in `notes/reuse_map_v7.md`), **BUILD** (nothing exists across all four accessible repos)}.
- Row-level Promise Table anchor uses the sheet-1 `#` column (1–31 canon + A1–A8 + N1–N5).

## Row-count table per doc (with amendments merged)

| Doc | Title | Umbrella canon(s) | Chunk-1 rows carried | Addendum sub-rows merged | Register total |
|---|---|---|---|---|---|
| 01 | Custody & Crossing Pt 1 (Chokepoint) | C1 §1–§4 · portion | 24 | 0 | **24** |
| 02 | Custody & Crossing Pt 2 (Confidentiality & Dual-file) | C1 §5 · portion | 18 | 1 (CA1-007 dry-run · CA1-001 audit line) | **20** |
| 03 | Intent & Security Monitoring | C3 + C8 (whole) | 67 (C3) + 82 (C8) = 149; deduped: 82 | 0 | **82** |
| 04 | Reasoning · Grounding · Solver | C4 §1–§9 · C2 portion | 40 | 1 (CA1-010 session-scoped lowered standard) | **41** |
| 05 | Direction · Scope · Focus Pt 1 (Northena) | C4 §10–§14 | 20 | 0 | **20** |
| 06 | Direction · Scope · Focus Pt 2 (Progressive Disclosure) | C4 §15 · C6 §3 | 15 | 1 (CA1-002 minimal-sufficient audit line) | **16** |
| 07 | Context Preservation Pt 1 (Shrinkage) | C4 §16 · C2 §4 (5-ring) | 18 | 1 (CA1-003 densification stat & warm/fresh tag; partial-A) | **19** |
| 08 | Context Preservation Pt 2 (Memory & Retrieval) | C2 §5 · C4 §17 | 16 | 1 (CA1-003 continued) | **17** |
| 09 | Estate Registry Pt 1 (Connection & Census) | C1 §6 · C5 §5 (partial) | 21 | 0 | **21** |
| 10 | Estate Registry Pt 2 (Comprehensive Registry) | C5 §5 (rest) · C1 §7 | 18 | 0 | **18** |
| 11 | Cost & Compute Pt 1 (Local-First & Levers) | C1 §8 · C4 §18 | 14 | 1 (CA1-008 Cost Ledger surface) | **15** |
| 12 | Cost & Compute Pt 2 (Locality & Transparency) | C1 §9 · C4 §19 | 12 | 0 | **12** |
| 13 | Targeting/Training Pt 1 (Autonomous Training) | C4 §20–§22 (Targeta) | 22 | 1 (CA1-011 standing re-check date per model) | **23** |
| 14 | Targeting/Training Pt 2 (Model Ecosystem) | C4 §23–§25 · C6 §4 | 26 | 2 (CA1-004 baseline line · CA1-005 white-paper) | **28** |
| 15 | Platform Orchestration & Governance Ceremony | C3 §5–§8 · C7 (whole) · C9 (whole) | 61 (C7) + 50 (C9) + 15 (C3) = 126; deduped: 84 | 3 (CA1-006 Watch state line · CA1-009 generalised handoff · CA1-012 template staleness) | **87** |
| 16 | Cross-Cutting Orchestration | C6 (whole) + C5 remainder | 66 (C6) + 40 (C5-remainder) = 106; deduped: 72 | 0 | **72** |
| **Total** | | | | **11** | **515** |

The umbrella nine's 626 bullets deduplicate down to **515 register rows** when re-projected onto the 16 essays (some Chunk-1 rows carry the same requirement across two canon slots and collapse under one doc). CA1-xxx adds 11 more (12 total; CA1-006 sits under Doc 15's Watch state-line requirement and adds 1 net row; CA1-001..CA1-003 each add one net row on their target docs).

**Round total: ≈ 515 canon-required rows.** Full row expansion available on request — the count-and-classification below drives the status % calculation.

## Status classification (aggregated per doc)

Per doc, row-count in each status bucket. Sourced from:
- **DONE**: cross-checked against Extraction-Akki track-a HEAD (`0709be7`) + tests green in `phase0/drill_receipts/20260825T151457Z_registry_facts_green.log` + prior cycle receipts (108–121/121 cohort green historically).
- **PARTIAL**: mechanism module exists but wire is incomplete or under a fixture (per reuse-map §2).
- **REUSABLE**: repo/path lifted / adapt-able per reuse-map §1–§2.
- **BUILD**: nothing across the four accessible repos.

| Doc | DONE | PARTIAL | REUSABLE | BUILD | Row total |
|---|---:|---:|---:|---:|---:|
| 01 · Chokepoint | 3 | 2 | 15 (RMS synisense + Exec-Core privacy_wall) | 4 | 24 |
| 02 · Confidentiality & Dual-file | 2 | 3 | 12 (RMS compliance + data_source) | 3 | 20 |
| 03 · Intent & Security Monitoring | 0 | 5 (shield partial) | 15 (RMS synisense) | 62 | 82 |
| 04 · Reasoning · Grounding · Solver | 0 | 3 | 30 (Exec-Core solva_v2 + RMS solva_depth) | 8 | 41 |
| 05 · Northena | 0 | 2 | 15 (RMS/AkkiOS northena) | 3 | 20 |
| 06 · Progressive Disclosure | 0 | 1 | 12 (Exec-Core analyze_workspace) | 3 | 16 |
| 07 · Five-ring unit (Shrinkage) | 0 | 2 | 14 (RMS perception + layer_a/b/c) | 3 | 19 |
| 08 · Warm/fresh · Memory & Retrieval | 0 | 2 | 13 (Exec-Core platform_kb + continue_chat) | 2 | 17 |
| 09 · Connection & Census | **21** | 0 | 0 | 0 | 21 |
| 10 · Comprehensive Registry & Opp. Briefs | **10** | 5 | 3 (RMS opportunity_briefs) | 0 | 18 |
| 11 · Cost & Compute Pt 1 | 0 | 2 | 10 (RMS economics + Exec-Core rate_limit) | 3 | 15 |
| 12 · Cost & Compute Pt 2 | **9** (compute connected) | 2 | 1 | 0 | 12 |
| 13 · Autonomous Training (Targeta) | 0 | 2 | 18 (RMS targeta + Exec-Core sandbox_generation) | 3 | 23 |
| 14 · Model Ecosystem · Baseline · Whitepaper | 0 | 2 | 22 (Exec-Core analysis_lifecycle + deck_*) | 4 | 28 |
| 15 · Governance Ceremony · Orchestration | 2 (ip_allowlist gate; declarations) | 4 | 65 (Exec-Core monitor + cycle_* + RMS master_admin) | 16 | 87 |
| 16 · Cross-Cutting Orchestration | 0 | 3 | 55 (Exec-Core work_studio + inbox_routing) | 14 | 72 |
| **Totals** | **47** | **40** | **300** | **128** | **515** |

Bucket shares: **DONE 9.1% · PARTIAL 7.8% · REUSABLE 58.3% · BUILD 24.9%** → this is the raw material for the status % table in `notes/status_and_wave_plan.md`.

## Row highlights per doc (illustrative — full expansion available on request)

Each row below is a REPRESENTATIVE requirement of the doc; the register carries the full set anchored to Chunk-1's C1-###/C2-### IDs.

### Doc 01 · Chokepoint · 24 rows
- **Doc01-001** ← C1-020 · Single chokepoint on every model call; masked crossing; receipt (Promise #1). Status **REUSABLE** (RMS `synisense/shield/`, Exec-Core `privacy_wall.py`). v7: Data Shield tab of `TRUST`.
- **Doc01-002** ← C1-021 · Exit gate is the only door out; no bypass path (Promise #26 hard-line). Status **REUSABLE**. v7: TRUST hard-line copy.
- **Doc01-004** ← C1-013 · Every operation emits an outside-verifiable receipt (Promise #1). Status **DONE** for connect+registry (`data_connection_record`, `commissioning_record` at `phase0/`); **PARTIAL** elsewhere.
- **Doc01-021** ← C1-045 · Masking tier 2 default for customer-identifying fields (Promise #27). Status **REUSABLE** (RMS synisense masking primitives).
- **Doc01-024** ← C1-051 · Data Shield exit-gate telemetry surface. Status **REUSABLE** (Exec-Core governance components).

### Doc 02 · Confidentiality & Dual-file · 20 rows (incl. CA1-007, CA1-001)
- **Doc02-001** ← C1-025 · DPO declaration workflow (Promise #2). Status **REUSABLE** (RMS compliance).
- **Doc02-002** ← C1-026 · Two-item dual-file custody split (Promise #4 · Addendum §1 CA1-001). Status **REUSABLE** (RMS data_source has dual-file primitives; audit line = **BUILD**).
- **Doc02-020 · CA1-007** · **Dry-run preview** between Review and Adopt. Status **BUILD** (no equivalent surface exists).
- **Doc02-020a · CA1-001** · Audit-trail Overview names "2+ independently-governed units" when an answer drew on such. Status **BUILD**.

### Doc 03 · Intent & Security Monitoring · 82 rows (Watch/Grey Mirror)
- **Doc03-001** ← C3-001 · The Watch reads intent, not just permission (Promise #6). Status **BUILD**.
- **Doc03-002** ← C8-004 · Four-memory stack (floor · declaration · norm · signature-capped). Status **BUILD**.
- **Doc03-014** ← C8-018 · Bait mechanism (planted records; touching = certain not suspicion). Status **BUILD**.
- **Doc03-030** ← C8-041 · Containment ladder (Noted · Friction · Contained · Held). Status **BUILD**.
- **Doc03-055** ← C8-062 · Suspect works inside a quarantine copy of the estate. Status **BUILD** (concept only in fixtures).
- **Doc03-078** ← C8-078 · Watch is exempt from external override; external witness signs (Addendum §1 CA1-006 state line). Status **BUILD**.
- 62 rows total in BUILD — this is the largest single BUILD area.

### Doc 04 · Reasoning · Solver · 41 rows (incl. CA1-010)
- **Doc04-001** ← C4-003 · Evidence gate refuses claims beyond source (Promise #8). Status **REUSABLE** (Exec-Core `solva_v2/`, RMS `solva_depth/`).
- **Doc04-014** ← C4-029 · Structured refusal (Evidence · Coverage · Contradiction) — v7 refusal card copy VERBATIM. Status **PARTIAL** (refusal card exists as `RefusalCard.js` in RMS; ceremony behind not wired).
- **Doc04-041 · CA1-010** · "Lower the standard" session-scoped with logged expiry. Status **BUILD**.

### Doc 05 · Northena · 20 rows
- **Doc05-001** ← C4-030 · Admit / Gate / Converge / Ledger loop (Promise #16). Status **REUSABLE** (RMS/AkkiOS `northena/`).
- **Doc05-006** ← C4-036 · Objective is frozen; a change is a new run (Promise #18). Status **REUSABLE**.

### Doc 06 · Progressive Disclosure · 16 rows (incl. CA1-002)
- **Doc06-001** ← C4-042 · Minimal-sufficient context per step (Promise #17). Status **REUSABLE** (Exec-Core analyze_workspace).
- **Doc06-016 · CA1-002** · Audit line names how many available source units were served. Status **BUILD**.

### Doc 07 · Shrinkage · 19 rows (incl. CA1-003 partial-A)
- **Doc07-001** ← C2-020 · Five-ring normalised unit (Promise #19). Status **REUSABLE** (RMS `perception/` + `layer_a/b/c/`).
- **Doc07-019 · CA1-003** · Densification stat + per-turn warm/fresh tag (partial closure per Addendum §1). Status **BUILD** on the surface.

### Doc 08 · Memory & Retrieval · 17 rows
- **Doc08-001** ← C2-032 · Model reads distilled memory, not raw DB (Promise #20). Status **REUSABLE** (Exec-Core `platform_kb.py`).
- **Doc08-006** ← C2-036 · Targeted fresh-fetch for what memory doesn't hold (Promise #21). Status **REUSABLE** (`continue_chat.py`).

### Doc 09 · Connection & Census · 21 rows — 100% DONE
- **Doc09-001** ← C1-055 · Connect to any store without migration (Promise #12). Status **DONE** (Extraction-Akki `services/connect/rds_data_submit.py`; live Aurora Data API).
- **Doc09-006** ← C5-045 · Estate census honest, dated, method-carrying (Promise #13). Status **DONE** (2 sources with STRUCTURE-ONLY inventory, `≈`-flagged approx rows).
- **Doc09-014** ← C5-050 · Audio first-class citizen (Promise #15). Status **DONE** as a Connect kind (`CONNECT_KINDS.data` covers audio archive).

### Doc 10 · Comprehensive Registry · 18 rows — Registry-A4 DONE
- **Doc10-001** ← C5-058 · One comprehensive Registry per source (Promise #14). Status **DONE** (Registry.jsx three-tab surface).
- **Doc10-006** ← C5-063 · Opportunity Briefs derived from Registry. Status **REUSABLE** (RMS `opportunity_briefs/`); surface **BUILD**.
- **Doc10-014** ← C5-070 · Registry renders honest empty (drawn, never left blank). Status **DONE** (LLMs tab and empty-state pattern).

### Doc 11 · Cost & Compute Pt 1 · 15 rows (incl. CA1-008)
- **Doc11-001** ← C1-078 · Cost ladder: cache → route → narrow → cascade → waste report (Promise #9). Status **REUSABLE** (RMS `economics/tier_lock.v*.json` carries the tier config; lever sequence surface = BUILD).
- **Doc11-015 · CA1-008** · Cost Ledger surface exposing the lever sequence as named ordered steps with saving-attributable-to-each. Status **BUILD**.

### Doc 12 · In-perimeter · Reflection · 12 rows — 83 % DONE
- **Doc12-001** ← C1-090 · Compute brought to the data (Promise #10). Status **DONE** (akki-vm connected in-perimeter, hardened, accepted-as-delivered).
- **Doc12-003** ← C1-092 · Reflection-before-commit: cost + budget quoted first (Promise #11). Status **DONE** (W2 closed 2026-08-25 · Extraction-Akki `programme/track-a` `7cf40a7` · services.compute_seam.reflection + Registry ReflectionPanel · seven-invariant contract green · `phase0/drill_receipts/20260825T180738Z_w2_reflection_green.log`).

### Doc 13 · Autonomous Training · 23 rows (incl. CA1-011)
- **Doc13-001** ← C4-060 · Six-criterion model acceptance (Promise #22). Status **REUSABLE** (RMS `targeta/` + Exec-Core `sandbox_generation.py`).
- **Doc13-023 · CA1-011** · Standing re-check date per in-service model. Status **BUILD**.

### Doc 14 · Model Ecosystem · Baseline · 28 rows (incl. CA1-004, CA1-005)
- **Doc14-001** ← C4-075 · Licence-verified baseline curation (Promise #24). Status **REUSABLE** (Exec-Core `analysis_lifecycle.py`).
- **Doc14-023 · CA1-004** · Baseline line names the licence-verified starting model per training run. Status **BUILD**.
- **Doc14-024 · CA1-005** · "Prepare white paper" action drafting from run artefacts (Promise #25). Status **BUILD**.
- **Doc14-026** ← C4-090 · One-license reach across every LLM (Promise #30). Status **REUSABLE** (Exec-Core deck_* + analysis_lifecycle).

### Doc 15 · Governance Ceremony · Orchestration · 87 rows (incl. CA1-006, CA1-009, CA1-012)
- **Doc15-001** ← C3-050 · Rules authored in plain language via open ceremony (Promise #27). Status **REUSABLE** (Exec-Core `monitor/` + `cycle_lifecycle.py` + RMS `master_admin/`); ceremony wizard surface = ADAPT.
- **Doc15-014** ← C3-055 · Nothing operates above governance except the Watch (Promise #26). Status **PARTIAL** (Watch mechanism absent).
- **Doc15-020** ← C9-005 · Every rule change: propose · counter-sign · countdown · apply · re-check. Status **REUSABLE**.
- **Doc15-085 · CA1-006** · Watch's self-contained exception + external witness state line. Status **BUILD** (Watch mechanism).
- **Doc15-086 · CA1-009** · **Generalised handoff contract** (what / shape / identity / receipt) for every cross-app crossing (Promise #32). Status **BUILD** (contract exists in one instance — ThinkLab→Task Manager per CA1-A7; generalised contract required).
- **Doc15-087 · CA1-012** · Watch staleness-flagging extended to rulebooks + baselines. Status **BUILD**.

### Doc 16 · Cross-Cutting Orchestration · 72 rows
- **Doc16-001** ← C6-005 · Cross-app hand-offs carry declaration + purpose (Promise #32 seed). Status **REUSABLE** (Exec-Core `work_studio/` + `inbox_routing/`).
- **Doc16-014** ← C5-095 · Refusal card copy VERBATIM across every surface. Status **DONE** as a component (`RefusalCard.js` in RMS/OS-V1); wire-through = **PARTIAL**.
- **Doc16-023** ← C6-020 · Universal claim-to-evidence trace = "Walk this →" (Promise-Table CA1-A8; see T8). Status **BUILD** (blocked pending T8 disposition).

## Merged Addendum (CA1-xxx) — full targeting

| CA1 ID | Target doc | Row ID | Kind | Status |
|---|---|---|---|---|
| CA1-001 | Doc 02 | Doc02-020a | Audit line (Promise #4 closure) | BUILD |
| CA1-002 | Doc 06 | Doc06-016 | Audit line (Promise #17 closure) | BUILD |
| CA1-003 | Docs 07 · 08 | Doc07-019 · Doc08-017 | Registry densification stat + per-turn warm/fresh tag | BUILD |
| CA1-004 | Doc 14 | Doc14-023 | Baseline line naming licence-verified starting model | BUILD |
| CA1-005 | Doc 14 | Doc14-024 | White-paper action drafting | BUILD |
| CA1-006 | Doc 15 | Doc15-085 | Watch self-containment + external witness state line | BUILD |
| CA1-007 | Doc 02 | Doc02-020 | Dry-run preview between Review and Adopt | BUILD |
| CA1-008 | Doc 11 | Doc11-015 | Cost Ledger surface exposing lever sequence | BUILD |
| CA1-009 | Doc 15 | Doc15-086 | Generalised handoff contract | BUILD |
| CA1-010 | Doc 04 | Doc04-041 | Session-scoped lowered-standard with logged expiry | BUILD |
| CA1-011 | Doc 13 | Doc13-023 | Standing re-check date per in-service model | BUILD |
| CA1-012 | Doc 15 | Doc15-087 | Watch staleness-flagging extended to rulebooks/baselines | BUILD |

**All 12 Addendum sub-rows are BUILD.** None are lift-able from any repo; they are net-new requirements on top of the umbrella-canon corpus.

## Promise Table row anchors (Sheet 1) — where accepted

- Promises #1 / #26 (chokepoint · exit gate) → Doc01-001..004 · Doc01-002
- Promises #2 / #4 (DPO declaration · dual-file) → Doc02-001..002 (+CA1-007)
- Promise #6 / #7 (Watch: intended-not-just-allowed; declared vs demonstrated reconciliation) → Doc03 (whole)
- Promise #8 (evidence gate) → Doc04-001..014 (+CA1-010)
- Promises #16 / #18 (Northena) → Doc05
- Promise #17 (progressive disclosure) → Doc06 (+CA1-002)
- Promises #19–#21 (shrinkage · memory) → Docs07–08 (+CA1-003)
- Promises #10 / #11 (compute in-perimeter · reflection) → Doc12
- Promises #12–#15 (connection · census · Registry · audio · one Registry) → Docs09–10
- Promise #9 (cost ladder) → Doc11 (+CA1-008)
- Promise #22 (six-criterion acceptance) → Doc13 (+CA1-011)
- Promises #23–#25 · #30 (training · baseline · whitepaper · one-license) → Doc14 (+CA1-004 · CA1-005)
- Promises #26 / #27 / #32 (Watch exception · rules ceremony · handoff) → Doc15 (+CA1-006 · CA1-009 · CA1-012)
- Composite claims (Promises #5 · #29) → Doc16
- A-series (A1–A8 Board/Exco/Docs/Rulebook/Collab/Spend/ThinkLab-handoff/Walk-this) → distributed across Docs15/16 + monitor.board/exco surfaces
- N-series (N1–N5 retention/breach/erasure/residency/continuity) → not in the 16 essays; **new canon obligations** anchored under Doc15 orchestration + Doc09/12 residency + Doc03 continuity.

## Anchor into the sprint

- **Wave 1 (T12 drawer rework + Registry backfill):** exercises Doc09 + Doc10 + Doc16 §refusal-card. Fully anchored on real records.
- **Wave 2 (compute · commissioning):** Doc12. Anchored on akki-vm's ACCEPTED record.
- **Wave 3 (chokepoint · masking · exit gate):** Docs 01 + 02 + CA1-007 dry-run + CA1-001. Unlocks Data Shield.
- **Wave 4 (Northena · direction):** Doc05.
- **Wave 5 (Solver · shrinkage · memory):** Docs 04 + 06 + 07 + 08 + CA1-010 + CA1-002 + CA1-003.
- **Wave 6 (Cost Ladder · retention · Grey Mirror groundwork):** Doc11 + CA1-008 + CA1-N1 + Doc03 subset.
- **Wave 7 (Targeta · Model Ecosystem):** Docs 13 + 14 + CA1-004 + CA1-005 + CA1-011.
- **Wave 8 (Governance ceremony · N-series):** Doc15 + CA1-006 + CA1-009 + CA1-012 + CA1-N2 + CA1-N3.
- **Wave 9 (Cross-cutting · Watch full · Ledger continuity):** Doc16 + Doc03 remainder + CA1-N5.

Full sequencing + scope classes + DONE-means definitions in `notes/status_and_wave_plan.md`.
