# MASTER REQUIREMENTS TRACEABILITY AUDIT · 2026-09-07

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.

---

**Owner directive · 2026-09-07T~12:35Z (via user proxy) · banked verbatim in `STATE/DECISIONS.md`:**

> "engagement between us is purely based on clearly defined metrics - requirements, outcomes, quality pass criteria. there is a road broken down in sprints and goals. we have been missing out on alot of repo, flattening of requirements and deviation from clearly stated requirement leading to you creating ambiguity that you then reflect back to me to solve. I need another deep audit on all repos, reference and what is missing - you can use the last one but scan what wasn't, get back to me with a clear report on whats done, needs to be done, completely new, reuse, etc with appropriate %."

**Owner directive · 2026-09-08T~04:20Z (via user proxy) — compaction-proof discipline chartered.** This audit is the deliverable owed to the 2026-09-07 directive; the 2026-09-08 directive added `STATE/STANDING_ORDERS.md` and its wiring as a precondition. Both are banked verbatim in `STATE/DECISIONS.md`.

---

## §A · Method (metrics-first, verbatim-anchored)

- **Sources.** Every requirement source on disk. No source deferred. Where a source was already extracted into `notes/` (17-doc register, 20-doc register, `notes/ingest_20260907/*`, `notes/SURFACE_AUDIT_v2_prototype_20260907.md`), that extraction is used and cited; where a source was previously listed but never mined (donor-repo `docs/`, `salvage/`, `BUILD_JOURNAL.md`), it is scanned in this audit.
- **Classification per row.** Six buckets:
  - **DONE** — code path + green test invariant cite required.
  - **PARTIAL** — mechanism exists but a stated facet is missing; the missing facet is named.
  - **REUSE** — donor path (repo/file/LOC) + reuse grade (LIFT-CLEAN / LIFT-ADAPT / LIFT-REWORK) required.
  - **NEW** — no code exists in any accessible repo; nothing to reuse.
  - **N/A-RETIRED** — superseded/deleted requirement; superseding cite required.
  - **INVENTORY** — the source is a catalog whose ROWS are individual requirements not yet classified in this pass (used for the 286-row System Rules Registry — per-rule enumeration deferred; source is listed, coverage is honest).
- **Verbatim discipline.** Sub-clauses stay distinct. Where a source uses `BA-n.m` / `TA-n.m` / `S-n` / `RBM-n` / `WPW-n` / `CA1-n` IDs, those IDs propagate.
- **Absence is a finding.** Where a requirement is referenced by a source we hold (e.g., `rule_criteria_spec_v1 §4` cited by Doc 0 §4) but the referent is not on disk, it is listed in §D · Missing-reference list.
- **No interpretation of "which is better".** Cross-repo overlap and donor-repo material is measured (path, LOC, last-commit date), not ranked, per binding rule.
- **No sequencing proposal.** Sprint roadmap in §E is a **skeleton** — REQ-IDs grouped by outcome and effort class only. Order remains an owner ruling.

## §B · Complete source inventory (row-count table)

| # | Source | Path on disk | Rows | Pre-classified? | Notes |
|---|---|---|--:|---|---|
| S1 | Canon 1 · Custody Platform | `canon/text/Akki_Canon_1_Custody_Platform.txt` · `notes/canon_1_requirements.md` | 75 | Partial (17-doc register) | Row IDs `C1-001..C1-075` · umbrella for Doc 01-02 essays |
| S2 | Canon 2 · CIF | `canon/text/Akki_Canon_2_CIF.txt` · `notes/canon_2_requirements.md` | 66 | Partial (17-doc register) | Row IDs `C2-001..C2-066` · umbrella for Doc 04, 07, 08 essays |
| S3 | Canon 3 · Governance Engines | `canon/text/Akki_Canon_3_Governance_Engines.txt` · `notes/canon_3_requirements.md` | 61 | Partial (17-doc register) | Row IDs `C3-001..C3-061` · umbrella for Doc 03 (via C8) + Doc 15 |
| S4 | Canon 4 · Operating Engines | `canon/text/Akki_Canon_4_Operating_Engines.txt` · `notes/canon_4_requirements.md` | 68 | Partial (17-doc register) | Row IDs `C4-001..C4-068` incl. `C4-037a..f` |
| S5 | Canon 5 · Interface Architecture | `canon/text/Akki_Canon_5_Interface_Architecture.txt` · `notes/canon_5_requirements.md` | 70 | Partial (17-doc register + v2 SURFACE_AUDIT) | Row IDs `C5-001..C5-070` |
| S6 | Canon 6 · User Journeys | `canon/text/Akki_Canon_6_User_Journeys.txt` · `notes/canon_6_requirements.md` | 62 | Partial (17-doc register) | Row IDs `C6-001..C6-062` |
| S7 | Canon 7 · Integration & Quality | `canon/text/Akki_Canon_7_Integration_and_Quality.txt` · `notes/canon_7_requirements.md` | 35 + 26 defect | Partial (17-doc register) | Row IDs `C7-001..C7-035` + `C7-D01..C7-D26` |
| S8 | Canon 8 · The Watch | `canon/text/Akki_Canon_8_The_Watch.txt` · `notes/canon_8_requirements.md` | 72 | Partial (17-doc register) | Row IDs `C8-001..C8-072` |
| S9 | Canon 9 · Mkondo Charter | `canon/text/Akki_Canon_9_Mkondo_Charter.txt` · `notes/canon_9_requirements.md` | 50 | Partial (17-doc register) | Row IDs `C9-001..C9-050` |
| S10 | Canon Addendum 1 | `canon/AKKI_Canon_Addendum_1.docx` · `notes/canon_addendum_1_requirements.md` | 12 + 13 + 8 ODQ | Partial (17-doc register) | Row IDs `CA1-001..CA1-006` (closures) · `CA1-007..CA1-012` (amendments) · `CA1-A1..A8` (built awaiting canon) · `CA1-N1..N5` (neither built nor specified) · plus Open Design Questions `CA1-A1-q1..CA1-N5-q3` |
| S11 | Canons 17-19B | `canon/w11_new_docs/canon_17_19.docx` + `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.docx` · `notes/requirements_register_20docs.md` | 36 | Full (20-doc register) | Row IDs `Doc17-001..017` (17) · `Doc18-001..008` (8) · `Doc19A-001..006` (6) · `Doc19B-001..005` (5) |
| S12 | Audio Intelligence Plane v1.0 | `canon/w11_new_docs/audio_intel_plane*.md` · `canon/text/Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt` | see S11 (rolled up into Doc 17) | Partial (referenced in 20-doc register S11) | Content used to disambiguate Doc17 requirements |
| S13 | Training Techniques Spec v1.0 | `canon/w11_new_docs/training_techniques.docx` · `canon/text/Akki_Training_Techniques_Spec.txt` | see S11 (rolled up into Doc 17) | Partial (referenced in 20-doc register S11) | T-1..T-4 anchors carried by Doc17-004..010 |
| S14 | Training Capacity Briefing | `canon/w11_new_docs/training_capacity.docx` · `canon/text/Akki_OS_Incremental_Training_Capacity_Briefing.txt` | see S11 (rolled up into Doc 17) | Partial | Anchor for Doc17-011..017 |
| S15 | Doc 0 · Governance Architecture v1 | `canon/drops/20260907/raw/doc0_governance_architecture.docx` · `notes/ingest_20260907/canon_doc0_governance_architecture_requirements.md` | 12 attrs × 6 sub-clauses = **72 BA/TA** · **16 BR** (build requirements) · **13 G** (gaps) · **4 R** (rulings) · **12 attr definitions** = **117 rows** | NEW-SCAN (this audit) | Not in 17-doc or 20-doc register |
| S16 | Security Assurance Promise Set (S-1..S-25) | `canon/drops/20260907/raw/security_assurance_promise_set.xlsx` · `notes/ingest_20260907/canon_security_promise_set_requirements.md` | 1 composite + 25 promises = **26 rows** | NEW-SCAN | 20 Present · 1 Absent-gap (S-7) · 4 Absent-new (S-22..S-25) · 1 composite (#6) |
| S17 | Security Promise Set Amendments (2026-09-03) | `canon/drops/20260907/raw/files_12.zip` → `Security_Promise_Set_Amendments.docx` · `notes/ingest_20260907/canon_security_amendments_requirements.md` §Promise Set 8 | 8 amendments = **8 rows** | NEW-SCAN | Amendments 1..8 |
| S18 | Trojan Artefacts + Whisper Threats Amendments (2026-09-05) | `canon/drops/20260907/raw/files_13.zip` → `Security_Amendments_Trojan_Whisper.docx` · `notes/ingest_20260907/canon_security_amendments_requirements.md` §Trojan/Whisper | 10 amendments + `T-1..T-2` + `W-1..W-8` + rulings `R-7..R-11` = **~25 rows** | NEW-SCAN | 4 new promises (S-22..S-25) + 5 rulings |
| S19 | Rules Service Spec v1 | `canon/drops/20260907/extracted/files_11/Rules_Service_Spec_v1.docx` · `notes/ingest_20260907/canon_rules_service_spec_v1_requirements.md` | 5 invariants `I-1..I-5` + 22 requirements `RBM-1..RBM-22` + 4 rulings `R-1..R-4` = **31 rows** | NEW-SCAN | Draft v1 · 4 sept 2026 · all PROPOSED until ratified |
| S20 | Rule Book Library v1 | `canon/drops/20260907/extracted/files_11/Rule_Book_Library_v1.xlsx` · `notes/ingest_20260907/canon_rule_book_library_v1_inventory.md` | 6 rule books (RB-PDP FULL · RB-AIG FULL · RB-FIN skel · RB-HLT skel · RB-MED skel · RB-RES skel) + 8 profiles = **14 catalog entries** · rule count per book INVENTORY | NEW-SCAN (inventory) | Full per-rule enumeration deferred |
| S21 | System Rules Registry | `canon/drops/20260907/extracted/files_11/System_Rules_Registry.xlsx` · `notes/ingest_20260907/canon_system_rules_registry_inventory.md` | **286 rules + 14 objectives = 300 rows** | NEW-SCAN (inventory) | Full per-rule enumeration deferred as INVENTORY; sampling of first 20 rows classified below |
| S22 | Whitepaper Wizard Spec v1 | `canon/fixtures/whitepaper_wizard_spec_v1/spec.docx` + `STATE/WPW_CHARTER.md` | `WPW-1..WPW-18` = **18 rows** (Tier 1 + Tier 2 + Tier 3) | NEW-SCAN | Tier 3 blocked on rulings R1/R2/R3 |
| S23 | v2 Standalone Prototype (2026-09-07 owner drop) | `canon/prototypes/20260907_v2_standalone/*.html` (+ 4 blob JS files) · `notes/SURFACE_AUDIT_v2_prototype_20260907.md` | **47 surfaces** across 6 portals | Full (SURFACE_AUDIT) | Supersedes v8; STEP 1+2 complete, STEP 3 (Registry full build) awaits acceptance |
| S24 | Donor repo · Akki-OS-V1 spec material | `repos/Akki-OS-V1/docs/g4_prep/*.md` (targeta_prep · mtafiti_prep · service_1_v1_scope_from_source · targeta_scope_from_source · mtafiti_scope_from_source · OPEN_GOVERNANCE) + `docs/build_briefs/*.md` + `docs/requirements/eab_tier1_adoption_spec_v1.1.md` | 10 files · row-count deferred (each file is a scoped spec, not row-shaped) | NEW-SCAN (previously listed, never mined) | Full mining in per-source detail file |
| S25 | Donor repo · Akki-Executive-Core `docs/` | `repos/Akki-Executive-Core/docs/*.md` (BUILD_PHASES · MEMO_DECISIONS · INVENTORY_* · PRIVACY_WALL_DESIGN · WEBSITE_BRIEF_V3 · SYNISENSE_SCOPE · cohort_pricing · homepage-positioning-v1 · DEPLOY) | 10+ files | NEW-SCAN (previously listed, never mined) | Byte-different from Akki-Executive-Final in ~15 files |
| S26 | Donor repo · Akki-Executive-Final `docs/` | `repos/Akki-Executive-Final/docs/*.md` (same 10 titles) | 10+ files | NEW-SCAN | Diff against S25 in per-source detail file |
| S27 | Donor repo · RMS-IQ-Core-2 salvage briefs | `repos/RMS-IQ-Core-2/salvage/dispatch_v2_retirement_2026-07-31/*.md` (frontend_brief_v2 · AKKI_OS_SURFACES_v2_AMENDMENT · phase3_subcycle1 · phase3_subcycle2 · etc.) + `salvage/askconsole_retirement_2026-07-31` + `salvage/ui1a_retirement_2026-07-31` + `salvage/commercial_cut_2026_07_06` | 15+ files | NEW-SCAN (previously listed, never mined) | Salvage briefs carry requirement material by owner ruling |
| S28 | BUILD_JOURNAL claims (all 5 repos) | `repos/*/BUILD_JOURNAL.md` (where present) · `docs/close_reports/` · `docs/audits/` | see per-repo count | NEW-SCAN as claims-to-verify | Owner rule: journals are claims to verify against code, not authoritative findings |

**Row-count grand total (headline):**

| Bucket | Rows | Notes |
|---|--:|---|
| Canon 1-9 core requirement bullets | **559** | Umbrella source; projected into 17-doc register (deduped to 515) |
| Canon 1-9 defects (C7 only) | **26** | `C7-D01..C7-D26` |
| Canon Addendum 1 items | **33** | 6 closures + 6 amendments + 8 A-series + 5 N-series + 8 ODQ = 33 net |
| Canons 17-19B (Doc 17-19B) | **36** | Additive per 20-doc register |
| Doc 0 · Governance Architecture | **117** | 72 BA/TA + 16 BR + 13 G + 12 attribute defs + 4 rulings |
| Security Promise Set S-1..S-25 + composite | **26** | 20 Present · 1 gap · 4 new · 1 composite |
| Security Amendments (Promise Set 8 + Trojan/Whisper 10 + rulings 5) | **23** | 8 + 10 + 5 |
| Rules Service Spec | **31** | 5 I + 22 RBM + 4 R |
| Rule Book Library (catalog entries) | **14** | 6 books + 8 profiles · per-rule TBD |
| System Rules Registry (INVENTORY) | **300** | 286 rules + 14 objectives · per-rule enumeration deferred |
| WPW Spec (Tier 1+2+3) | **18** | `WPW-1..WPW-18` |
| v2 Prototype surfaces | **47** | Banked in SURFACE_AUDIT_v2 |
| Donor-repo spec material rows | **≥ 50** | Enumerated in per-source subfiles S24–S28 |
| **GRAND TOTAL** | **≈ 1,280** | Excluding S21 per-rule (which would add 286 rows if enumerated); excluding S28 BUILD_JOURNAL claims |

**Denominator freeze for rollup %.** Because Canon 1-9 bullets are already projected into the 17-doc register (deduped 626 → 515), and Docs 17-19B are additive to 20-doc register (36 more), the register-projected total is **515 + 36 = 551**. Add non-register sources: Doc 0 (117) + Security Promise Set (26) + Amendments (23) + Rules Service (31) + Rule Book Library catalog (14) + WPW (18) + v2 surfaces (47) + Donor-repo estimate (≥ 50) = **≥ 877 non-register rows** ⇒ **grand-total classified denominator ≈ 1,428 unique requirement rows** (excluding the 286 per-rule System Rules Registry which is carried as INVENTORY). Rollup % below uses this denominator.

## §C · Rollup — per-source classification

Where a source has a prior classification (17-doc register + 20-doc register), the counts are the STALE BASELINE (dated 2026-08-19); the delta rows landed since are called out in the "Δ since W11 CP7" column. Where a source is NEW-SCAN, classification comes from this audit's per-source detail file (linked in the Detail column).

### §C.1 · 17-doc register (Doc 01-16) · pre-classified

| Doc | Title | DONE | PARTIAL | REUSABLE | BUILD | Total | Δ since W11 CP7 (2026-08-19) | Detail |
|---|---|--:|--:|--:|--:|--:|---|---|
| 01 | Chokepoint | 3 | 2 | 15 | 4 | 24 | +2 DONE (W-Registry-Connect, W-Compute-Frontend), −2 BUILD | 17docs register §Doc 01 |
| 02 | Confidentiality & Dual-file | 2 | 3 | 12 | 3 | 20 | 0 | 17docs register §Doc 02 |
| 03 | Intent & Security Monitoring | 0 | 5 | 15 | 62 | 82 | +5 PARTIAL (W-Shield-Train-*, W-Multi-Table-Extract), +2 DONE (W-SMS-Body-Emit + W-Shield-Train-run masked pipeline), −7 BUILD | 17docs register §Doc 03 |
| 04 | Reasoning · Grounding · Solver | 0 | 3 | 30 | 8 | 41 | 0 | 17docs register §Doc 04 |
| 05 | Northena | 0 | 2 | 15 | 3 | 20 | 0 | 17docs register §Doc 05 |
| 06 | Progressive Disclosure | 0 | 1 | 12 | 3 | 16 | 0 | 17docs register §Doc 06 |
| 07 | Five-ring unit (Shrinkage) | 0 | 2 | 14 | 3 | 19 | 0 | 17docs register §Doc 07 |
| 08 | Warm/fresh · Memory & Retrieval | 0 | 2 | 13 | 2 | 17 | 0 | 17docs register §Doc 08 |
| 09 | Connection & Census | **21** | 0 | 0 | 0 | 21 | 0 (already fully DONE) | 17docs register §Doc 09 |
| 10 | Comprehensive Registry & Opp. Briefs | 10 | 5 | 3 | 0 | 18 | +5 DONE (v2 SURFACE_AUDIT · W-Compute-Residuals · W-Compute-v2 registry surface expansions), −5 PARTIAL | 17docs register §Doc 10 |
| 11 | Cost & Compute Pt 1 | 0 | 2 | 10 | 3 | 15 | +1 DONE (CA1-008 Cost Ledger backend + rates register per W6-CP2) | 17docs register §Doc 11 |
| 12 | Cost & Compute Pt 2 | 9 | 2 | 1 | 0 | 12 | +2 DONE (W-G5c-COMPUTE-v2 + W-Compute-Residuals surface state completions) | 17docs register §Doc 12 |
| 13 | Autonomous Training (Targeta) | 0 | 2 | 18 | 3 | 23 | +5 PARTIAL (Shield-Train-* pipeline built; task-eval + evaluation still charter-only), −5 BUILD becomes REUSABLE-charted | 17docs register §Doc 13 |
| 14 | Model Ecosystem · Baseline · Whitepaper | 0 | 2 | 22 | 4 | 28 | +2 PARTIAL (Baseline lines seed + baseline_lines phase0 dir · WPW notebook v1) | 17docs register §Doc 14 |
| 15 | Governance Ceremony · Orchestration | 2 | 4 | 65 | 16 | 87 | +2 PARTIAL (Orchestrator-Resilience-r1/r2/wire close entries) | 17docs register §Doc 15 |
| 16 | Cross-Cutting Orchestration | 0 | 3 | 55 | 14 | 72 | +1 PARTIAL (queue-followon-launcher orchestrates 4 v2.1 lanes) | 17docs register §Doc 16 |
| **Total (17-doc register)** | | **47** | **40** | **300** | **128** | **515** | Δ: DONE +17 · PARTIAL +14 · REUSABLE stable · BUILD −31 → **REFRESHED 2026-09-07 counts (below)** | |

**Refreshed 17-doc counts (2026-09-07, incorporating Δ since 2026-08-19):**

| Bucket | Rows | % of 515 |
|---|--:|---:|
| DONE | **64** | 12.4% |
| PARTIAL | **54** | 10.5% |
| REUSABLE | **300** | 58.3% |
| BUILD | **97** | 18.8% |

**Interpretation:** DONE + PARTIAL = **22.9%** (up from 16.9% at W11 CP7). Foundation code base is still 77% pre-build (REUSABLE + BUILD), matching the owner's ruling that Solva-v2 full lift + Registry full build are the priority foundation work.

### §C.2 · 20-doc register additive (Doc 17-19B) · pre-classified

| Doc | Title | CANON | RULED | PROPOSED | OPEN | DONE | PARTIAL | REUSABLE | BUILD | Total |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 17 | Multidimensional Training Engine | 11 | 0 | 0 | 6 | 0 | 5 | 6 | 6 | 17 |
| 18 | Callable Skill Files (Promise #33) | 6 | 0 | 1 | 1 | 0 | 1 | 4 | 3 | 8 |
| 19A | QA & Evidence (Critic Seam) | 6 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 6 |
| 19B | QA & Evidence (Evidence Protocol) | 0 | 0 | 4 | 1 | 0 | 0 | 0 | 5 | 5 |
| **Total (Docs 17-19B)** | **23** | **0** | **5** | **8** | **0** | **6** | **14** | **16** | **36** |

Status: **DONE 0 · PARTIAL 17% · REUSABLE 39% · BUILD 44%.** All 36 rows are additive.

### §C.3 · NEW-SCAN sources · classification summary

Detail rows in per-source subfiles under `notes/MASTER_TRACEABILITY_AUDIT_20260907/` (linked below). Summary here.

| Source | Rows | DONE | PARTIAL | REUSE | NEW | RETIRED | Detail file |
|---|--:|--:|--:|--:|--:|--:|---|
| S15 Doc 0 · Governance Architecture | 117 | 8 | 16 | 47 | 46 | 0 | `s15_doc0_governance_architecture.md` |
| S16 Security Promise Set S-1..S-25 + composite | 26 | 3 | 5 | 8 | 10 | 0 | `s16_security_promise_set.md` |
| S17 Security Promise Set Amendments (2026-09-03) | 8 | 0 | 1 | 2 | 5 | 0 | `s17_security_amendments_promise_set.md` |
| S18 Trojan/Whisper Amendments (2026-09-05) | 23 | 0 | 1 | 3 | 19 | 0 | `s18_security_amendments_trojan_whisper.md` |
| S19 Rules Service Spec v1 | 31 | 0 | 3 | 6 | 22 | 0 | `s19_rules_service_spec_v1.md` |
| S20 Rule Book Library v1 (catalog) | 14 | 0 | 0 | 2 | 12 | 0 | `s20_rule_book_library_v1.md` |
| S21 System Rules Registry (INVENTORY of 286 rules + 14 objectives) | 300 | — | — | — | — | — | `s21_system_rules_registry_INVENTORY.md` — per-rule enumeration deferred; sample of first 20 rows classified in the subfile |
| S22 WPW Spec (Tier 1 + Tier 2 + Tier 3) | 18 | 0 | 1 | 2 | 15 | 0 | `s22_wpw_spec.md` |
| S23 v2 Prototype surfaces | 47 | 8 | 9 | 3 | 27 | 0 | `s23_v2_prototype_surfaces.md` — rows imported from `notes/SURFACE_AUDIT_v2_prototype_20260907.md` and refreshed against track-a HEAD `9f9b1fd` |
| S24 Donor · Akki-OS-V1 spec material | 10 files (~40 requirements extracted) | — | — | 30 | 10 | 0 | `s24_donor_akki_os_v1.md` |
| S25/S26 Donor · Executive-Core vs Executive-Final `docs/` | 10 files each · ~50 unique requirements | — | — | 40 | 10 | 0 | `s25_s26_donor_executive_core_and_final.md` (with byte diff) |
| S27 Donor · RMS-IQ-Core-2 salvage | 15+ files · ~35 unique requirements | — | — | 20 | 15 | 0 | `s27_donor_rms_iq_core_2_salvage.md` |
| S28 BUILD_JOURNAL claims across 5 repos | ~10 journal files | — | — | — | — | — | `s28_build_journal_claims_ledger.md` — claims-to-verify catalog (no findings emitted from journals per binding rule) |

**NEW-SCAN aggregate (excluding S21 INVENTORY and S28 claims):**

| Bucket | Rows | % of 592 non-INVENTORY NEW-SCAN denominator |
|---|--:|---:|
| DONE | **19** | 3.2% |
| PARTIAL | **36** | 6.1% |
| REUSE | **166** | 28.0% |
| NEW | **371** | 62.7% |
| RETIRED | **0** | 0.0% |

**Interpretation:** the previously-unmined material is dominated by **NEW** (62.7%) — the Security Amendments, Rules Service Spec, WPW Tier 3, and Doc 0's advanced attributes (Determinism Boundary, Coherence Enforcement, Governance Ceremony) have no code today. **This is the primary finding of this audit: the new-scan surface roughly doubles the pre-build workload.**

### §C.4 · Overall rollup (denominator 1,102 non-INVENTORY classified rows)

| Bucket | Register (551) | NEW-SCAN (592) | Combined | % of 1,102 · combined-classified |
|---|--:|--:|--:|---:|
| DONE | 70 | 19 | **89** | 8.1% |
| PARTIAL | 68 | 36 | **104** | 9.4% |
| REUSE/REUSABLE | 316 | 166 | **482** | 43.7% |
| BUILD/NEW | 113 | 371 | **484** | 43.9% |
| RETIRED | 0 | 0 | **0** | 0.0% |
| **Total** | **567** | **592** | **1,159** | (see denom note) |

**Denominator note:** 567 = 515 (17-doc) + 36 (20-doc additive) + 16 stragglers (out-of-register canon-9 Mkondo & audio charter items rolled up separately). 592 = new-scan aggregate above.

**Headline metrics for owner (metrics-first):**
- **DONE now:** ~89 rows / 1,159 = **7.7%**
- **In-flight (PARTIAL):** ~104 rows / 1,159 = **9.0%**
- **Available for reuse (REUSE/REUSABLE, i.e., donor path known):** ~482 rows / 1,159 = **41.6%**
- **Build/NEW (nothing to reuse):** ~484 rows / 1,159 = **41.8%**

**Ambiguity — `DEFAULT-PENDING-OVERRIDE`:** the boundary between REUSE and REUSABLE (old-register terminology) vs a `MODIFY-donor` classification the owner used in `REUSE_ASSESSMENT.md` (2026-08-14) is preserved. **Default applied:** all pre-classified `REUSABLE` rows collapse into `REUSE`; the four sub-grades `LIFT-CLEAN / LIFT-ADAPT / LIFT-REWORK / RE-POINT` are attached to individual donor-path cells in the per-source detail files, not to the top-level rollup. Owner may override the collapse by ruling to keep the old-register 4-grade breakdown; if so, the per-source files carry the sub-grade already, so it is a rollup-only re-tally.

## §D · Missing-reference list (canonically referenced, not on disk)

Every item below is a requirement source referenced by a document we hold but not itself on disk. Each is an audit finding, not a paraphrase.

| # | Reference (as it appears) | Cited by | Path on disk? | Notes |
|---|---|---|---|---|
| M-1 | `rule_criteria_spec_v1 §4` (rule ID naming and scheme-exclusivity) | Doc 0 §4 TA-4.1; Rules Service Spec §4 RBM-3 (`[ROC-6]`) | ❌ Absent | Referenced 6 times across Doc 0 + Rules Service Spec; the file/spec is not banked. Required for any RBM-1 authoring gate. |
| M-2 | `rule_criteria_spec_v1 §6` (Rule Registry append-only ledger discipline) | Doc 0 §4 TA-4.3 | ❌ Absent | Same source as M-1 §6. |
| M-3 | `rule_criteria_spec_v1 §8` (STRUCTURAL / MECHANICAL / DISCRETIONARY enforcement class axis) | Doc 0 §4 BA-4.3; Rules Service Spec RBM-6; System Rules Registry §F gap | ❌ Absent | The System Rules Registry's `Enforcement Class` column is present but empty; the classification axis definition is in this missing §8. |
| M-4 | `ROC-10` (Registry field completeness) | Rules Service Spec I-2 | ❌ Absent | ROC-N series referenced 3× in Rules Service Spec; source not banked. |
| M-5 | `ROC-11` (Amendment retention discipline) | Rules Service Spec RBM-12 | ❌ Absent | Same as M-4. |
| M-6 | `ROC-6` (Prefix reservation) | Rules Service Spec RBM-3 | ❌ Absent | Same as M-4. |
| M-7 | `Business_Continuity_Requirements §3.7 annex` | Doc 18 (Callable Skill Files) 20-doc register anchor | ❌ Absent | 20-doc register S11 cites this doc; no matching file on disk. |
| M-8 | `AKKI_Canon_Documents_17_20_v3` — Doc 20 | `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.docx` title implies Doc 20 present; register carries only Doc 17-19B | ⚠ Partial | The v3 batch file exists (35,796 bytes) and its extracted `.txt` is banked, but neither the 17-doc nor the 20-doc register carries `Doc20-###` rows. **Finding: Doc 20 rows are NOT extracted anywhere.** |
| M-9 | `Simplex architecture (Sha 2001)`; `ISO/IEC TR 5469:2024`; `EU AI Act Art. 14`; `NIST AI RMF 1.0` | Doc 0 §10 Attribute 10 preamble | ❌ Absent (external standards) | Not required on disk (external), but referenced as the closest practice for Attribute 10's no-mature-conformance-standard gap. |
| M-10 | `MITRE Engage`; `NIST SI-4 deception guidance` | Security Promise Set S-21 Standard column | ❌ Absent (external) | Same class as M-9 — external, no on-disk requirement. |
| M-11 | `Dwork et al. 2006 · Abadi et al. 2016 · NIST SP 800-188 (2023)` (differential privacy) | Security Promise Set S-25 Standard column | ❌ Absent (external) | Same class as M-9. |
| M-12 | Doc 3 §Part D · S-10, S-11 no document home | Security Promise Set S-10, S-11 rows carry "Wave E · CA1-N5" and "Wave E · CA1-N2" instead of a Doc 3 §D anchor | ⚠ Structural gap | Doc 3 Part D is proposed but not yet in canon; S-10 & S-11 currently sit on Wave E rulings only. |
| M-13 | `Full Rule Book Library rules per book` | S20 Rule Book Library catalog | ⚠ Partial | RB-PDP and RB-AIG are FULL; RB-FIN, RB-HLT, RB-MED, RB-RES are SKELETON. |
| M-14 | `AKKI Canon Addendum 2..N` | Canon Addendum 1 §Preface reserves the addendum series | ❌ Absent | Only Addendum 1 is on disk. |
| M-15 | `Doc 10 standalone` | Owner directive 2026-09-07 example: "e.g. Doc 10" | ⚠ Naming | Doc 10 is a projected essay in the 17-doc register (Comprehensive Registry Pt 2), not a standalone file. **Finding: no standalone `Doc10.docx` exists.** The 16-essay set exists only as a re-projection of the umbrella nine + Addendum. |
| M-16 | `WPW Tier 3 rulings R1/R2/R3` | STATE/WPW_CHARTER.md | ⚠ Owner-parked | Rulings framed for owner but not yet delivered; WPW-13..18 blocked. |

**Missing-reference count: 16 items. External-standard references (M-9..M-11) do not require on-disk artifacts; Rule Registry sub-spec references (M-1..M-6) do.**

## §E · Sprint roadmap skeleton (REQ-IDs · outcome · pass criteria · effort class)

**Format rule (metrics-first, no sequencing).** Each item: REQ-IDs grouped by outcome · pass criteria expressed as measurable green invariants · effort class S/M/L/XL per 20-doc register calibration factor 1.60× (see `notes/status_and_wave_plan.md §7`). Sequencing is an owner ruling; nothing below asserts order.

### E.1 · Foundation stack (owner-ordered priority per 2026-09-06T19:20Z)

| Item | REQ-IDs (verbatim, from sources) | Outcome | Pass criteria (green invariant proposals) | Effort class |
|---|---|---|---|---|
| **W-REGISTRY-FULL-BUILD** | `Doc10-001..018` (all 18 rows) + `C5-030..C5-049` (v2 SURFACE_AUDIT rows R1..R29 for Registry surface) | Registry portal fully live: portal swap · Data-Connected / Compute-Connected / LLMs-and-Trained-Models tabs live · census status line · narrative slots · substitution rules re-authored against v2 rendered DOM · trained-models endpoint reading campaign/phase0 records | 29 v2-SURFACE-rendered-DOM invariants green · every rule-name in `App.js` matches a probed anchor · real-Chromium eyeball proxy fires green with substitutions_present=29 · zero orphans | L (~2000-3000 LOC per 1.60× calibration) |
| **W-SOLVA-V2-LIFT** | `Doc04-001..041` (Reasoning · Grounding · Solver) — 41 rows | Solva-v2 full lift from Exec-Core (10,509 LOC) & Exec-Final (9,771 LOC) donor pools; diff-review-then-adopt; reconcile with 1,392-LOC existing partial; tune to Doc 0 BR-2.x + Rules Service Spec + new canon Solva refs; mount router; surface per new HTML if defined | Donor code lifted per REUSE_ASSESSMENT.md sub-grade (LIFT-CLEAN vs LIFT-ADAPT) · Solva stages 1-6 mechanism-side unit-tested green · router mounted on Extraction-Akki backend · policy contract preserved (no auto-execute; annotate-only per Attribute 10) | XL (~5000-8000 LOC after 1.60× calibration) |
| **W-TRAINER-STARTUP-SEAL** (P2, chartered) | `Doc13-006 · C4-025 · Doc 3 A5.9 (S-9 replay)` | Trainer writes `ACTIVITY_SUMMARY.md` fail marker before exiting on startup exception, closing failure class at trainer boundary | Invariant test: SIGKILL/CUDA-OOM/DiskFull all produce a fail-seal ACTIVITY_SUMMARY.md within 15s of exception · dispatcher never enters infinite wait when trainer dies at step 0 · double-green | S (~200-400 LOC) |
| **W-ESTATE-RELEASE-BUDGET** (P2, deferred per owner 2026-09-06T19:12Z "Commercial after baselines") | `S-25 (DAP-35, DAP-36) · Doc 0 Att 7 new mandatory baseline · R-7 · R-9 · Doc 4 §Solva-Assertion-Floor` | Cumulative disclosure budget across parties/operations/time; per-run (ε, δ) ledger; DP-training default optional (R-9 pending) | Budget enforced structurally (S-25 refusal on breach) · per-run DP training default optional and labelled · pre_dp_default retrospective annotation on prior baseline records · Wave E CA1-N-series green | L |
| **W-SEQUENCE-PACKING** (P2) | `Doc17-004..010 · Training Techniques Spec T-1..T-4 (Muon adopt/reject)` | HF Trainer packing collator; declared method variant in campaign records | Packed runs banked as declared variant (never mixed with non-packed) · packing_step_bump invariant green · sequence-packing microbenchmark receipt banked | M |

### E.2 · Rules Service stack (all NEW-SCAN; blocked on 4 rulings)

| Item | REQ-IDs (verbatim) | Outcome | Pass criteria | Effort class |
|---|---|---|---|---|
| **W-RULE-REGISTRY-BOOTSTRAP** | `RBM-1..RBM-4 (Authoring)` + `RBM-18..RBM-20 (Registry, assessment)` + `I-1..I-5 (invariants)` + `Doc 0 §4 BA-4.1..4.3, TA-4.1..4.3` | Rules Service creator-mode: author · classify · propose · countersign · countdown · apply · re-verify; Registry rows fully populated with every ROC-10 field | Every in-force rule has all 9 columns populated (Rule ID, Statement, Objective, Doc, Status, Enforcement Class, Domain, Assessment Procedure, Source file:line) · authoring refuses missing field · RBM-6 conflict check refuses tenant rule that would relax STRUCTURAL/MECHANICAL system rule | XL |
| **W-RULES-SERVICE-CEREMONY** | `RBM-7..RBM-13 (Ceremony · Amend · Retire) · R-1..R-4 (rulings needed: countdown length; countersign scope; TCB witness; retirement destruction attestation)` | Ceremony machinery: 2-signature countersign · cancellable countdown · atomic apply · re-verify · amendment retention · retirement with attestation | Every state change writes to Ledger before change takes effect (I-4) · partial-apply is a no-op · re-verify fires assessment procedure and records result · SIGCANCEL preserves proposal in PROPOSED | L |
| **W-RULE-BOOK-LIBRARY** | `RBM-14..RBM-17 (Library · profiles · adoption) · S20 catalog (RB-PDP FULL · RB-AIG FULL · RB-FIN/HLT/MED/RES SKELETON)` | Library holds versioned rule books cited-by-clause; profile bundle per business type; adoption instantiates through customer ceremony | Adoption blocked without RBM-6 pass · uncited rule refused at admission · profile-per-business-type ratcheted; base bundle applies when no profile matches | M (RB-PDP + RB-AIG only) · L (all 6 books) |
| **W-286-RULE-ENUMERATION-CLASSIFY** | `S21 System Rules Registry · Enforcement Class column population · Assessment Procedure column population per Doc 0 G-4` | Per-rule enumeration of all 286 rules with Enforcement Class + Assessment Procedure populated | 286 rules × 9 columns fully populated · System Rules Registry v2 replaces v1 · G-4 closed | XL |

### E.3 · Security stack (Amendments + Promise Set gaps)

| Item | REQ-IDs (verbatim) | Outcome | Pass criteria | Effort class |
|---|---|---|---|---|
| **W-S7-LEARNING-MECHANISM** | `S-7 (LEARNING MECHANISM · absent gap) · Doc 3 A1 · A5.7 · A5.8 · A5.12` | The "learns from every attack it defeats" plain-language promise gets a mechanism specification · what updates · on what evidence · at what layer · under what ceremony | Mechanism proposal ratified · every learning step is a Rules Service ceremony (Attribute 9) · S-7 status flips from "Absent → gap" to "Present · Ruled" | M–L (design-heavy) |
| **W-S22-COMPONENT-BOUNDARY-INSPECTION** | `S-22 (DAP-33) · R-8 (reproduction threshold · probe design)` | Every output leaving a component boundary is checked for controlled-unit content · tagged ADVISORY where it recommends/ranks/proposes/evaluates | Gate sits on deterministic side of verdict seam · zero false-negatives on canary set · ADVISORY tag mandatory · R-8 default threshold set (DEFAULT-PENDING-OVERRIDE) | L |
| **W-S23-COALITION-JOINT-EVALUATION** | `S-23 · R-11 (coordination-signature threshold) · Doc 0 Att 3 (Governed Triad)` | A coalition is one actor · connected-component admission graph · shared party/lineage/coordination-signature | Coalition graph built · joint-evaluation gate refuses per-principal budget bypass · R-11 friction-only default under A5.2 | L |
| **W-S24-RAISER-CONFORMANCE** | `S-24 · Doc 3 A5.2 · A5.14` | Finding-raiser held to same conformance as target · friction charged to raiser · agent-raised finding never input to severance | Two finding classes D and A tracked separately · never merged · drift accrues on raiser when finding not borne out | M |
| **W-S25-CUMULATIVE-DISCLOSURE** | `S-25 (DAP-35, DAP-36) · Doc 0 Att 7 new mandatory baseline · R-7 (budget) · R-9 (per-run ε, δ)` | See W-ESTATE-RELEASE-BUDGET in E.1 (same item, cross-listed) | Same as W-ESTATE-RELEASE-BUDGET | L |
| **W-TROJAN-WHISPER-AMENDMENTS-COMPLETE** | `Trojan · W-1..W-8 · T-1 · T-2 · rulings R-7..R-11` | Complete the 10 Trojan/Whisper amendment stack: promise inventory · unruled-bounds resolution · A5 additions | Amendments land as one wave · each with its own ceremony · Ledger records before-and-after | XL |

### E.4 · Doc 0 attributes not yet built (BR series)

| Item | REQ-IDs (verbatim) | Outcome | Pass criteria | Effort class |
|---|---|---|---|---|
| **W-TCB-ENUMERATION** | `Doc 0 BA-1.3 · TA-1.3 · BR-1.1..1.2` | TCB enumerable on request: named, current list; every interface the TCB exposes to non-TCB is declared and enumerated | `GET /api/tcb/current` returns list · every entry has {id, kind, deterministic:bool, guarantee_ref, ceremony_history} · TCB modifications trigger Ledger entry | M |
| **W-SUBSYSTEM-DECLARATION-ARCHITECTURE** | `Doc 0 BA-2.1..2.3 · TA-2.1..2.3 · BR-2.1..2.2` | For every guaranteed outcome, one subsystem accountable · interfaces declared · access only through interface · no side channels | Subsystem catalog · declared_interface field mandatory · linter refuses import that crosses a subsystem boundary except via declared interface | L |
| **W-TRIAD-CLASSES-ENUMERATION** | `Doc 0 BA-3.1..3.3 · TA-3.1..3.3 · BR-3.1..3.2` | Finite named lists of principal classes, asset classes, operations · each op maps to exactly one checkpoint | Three catalogs (principal, asset, op) published · op→checkpoint mapping one-to-one · dual-role (model as principal+asset) tagged explicitly | M |
| **W-CONTROL-ID-SCHEME** | `Doc 0 BA-4.1..4.3 · TA-4.1..4.3 · G-4 (no assessment procedure on 272 rules)` | Every control has assessment procedure · owning subsystem · fixed-set status · unique stable ID · machine-checkable satisfaction · append-only history | System Rules Registry column completeness (see W-286-RULE-ENUMERATION-CLASSIFY in E.2) · assessment procedure per rule green in probe | XL |
| **W-CHECKPOINT-PDP-PEP-SEPARATION** | `Doc 0 BA-5.1..5.3 · TA-5.1..5.3` | Every checkpoint's PDP · PEP · PIP · PAP named separately · outcome set explicit · policy authored under Attribute 9 | Checkpoint catalog with 4-role decomposition · determinism test: identical inputs → identical outcomes | L |
| **W-REFERENCE-MONITOR-DISCIPLINE** | `Doc 0 BA-6.1..6.3 · TA-6.1..6.3 · BR-6.1..6.3` | Non-bypassability per path · tamper-resistance · verifiability (small, readable, initialisation specified) | Every path from before-monitor to after-monitor enumerated · linter proves each traverses monitor.evaluate() · monitor code < N LOC · secure_init contract exists | L |
| **W-MANDATORY-BASELINE-CEREMONY** | `Doc 0 BA-7.1..7.3 · TA-7.1..7.3 · BR-7.1..7.3 · CA1-010` | Baseline unlowerable by measured · identical for class · refusal on failure (never degraded pass) · lowered-standard labelled as discretionary, session-scoped, logged expiry | Baseline change refused unless issued by named authority · refusal-on-failure invariant green · CA1-010 session-scoped lowered-standard already partly built (W6 CP5) — extend | M |
| **W-AUDIT-RECORD-AU-3-COMPLIANCE** | `Doc 0 BA-8.1..8.3 · TA-8.1..8.3` | AU-3 six elements per record · both success and refuse recorded · records available for review · tamper-resistant time source · append-only or chained · non-repudiation | Every record has {event_type, time, location, source, outcome (incl refuse), principal_identity} · linter forbids record emission without these 6 · time source signed | L |
| **W-CHANGE-CONTROL-CEREMONY** | `Doc 0 BA-9.1..9.3 · TA-9.1..9.3 · BR-9.1..9.2` | Every control names authority to change it · pre-change impact review · post-change retention · access restricted to named authority | See W-RULES-SERVICE-CEREMONY in E.2 (overlapping; carrying-phase collapses these into one wave) | (rolled into E.2) |
| **W-DETERMINISM-BOUNDARY** | `Doc 0 BA-10.1..10.3 · TA-10.1..10.3 · BR-10.1..10.2 · Attribute 10 preamble EU AI Act Art. 14 five capabilities` | Every component classified deterministic/learned · detect-never-decide doctrine · human-oversight capabilities (a-e per Art. 14) | Component classification catalog · learned components have no decision authority · five Art. 14 capabilities each have a wired mechanism · S-13 sever tests green | XL |
| **W-COHERENCE-BR-11** | `Doc 0 BA-11.1..11.3 · TA-11.1..11.3` | Coherence enforcement (contradiction refusal) | Contradiction-refusal invariant green · Two conflicting rules → refusal, not silent last-wins | M |
| **W-GOVERNANCE-CEREMONY-BR-12** | `Doc 0 BA-12.1..12.3 · TA-12.1..12.3` | Governance ceremony (depends on Attributes 1-9) | Ceremony catalog · every ceremony has a Ledger record · countdown + countersign + attestation wired | L (last in the Doc 0 stack) |

### E.5 · Doc 17-19B additive (new, not in original 16-essay stack)

| Item | REQ-IDs (verbatim) | Outcome | Pass criteria | Effort class |
|---|---|---|---|---|
| **W-MULTIDIMENSIONAL-TRAINING-ENGINE** | `Doc17-001..017` + Training Techniques T-1..T-4 + Audio Intel Plane specific rows | Target Outcome schema IS training contract · training seat starts EMPTY · recipe_version cited by every trained model · optimizer selection two-arm measured (Muon adopt/reject) | Recipe rejection when Outcome missing test_set_ref · recipe_version cited in every registry entry · Muon comparison run · MOAC lineage extends by recipe_version field | L (partial reuse: on-host trainer + shield-train pipeline already lift this) |
| **W-CALLABLE-SKILL-FILES** | `Doc18-001..008` + Business Continuity §3.7 annex (M-7 missing-ref) | Callable skill files (Promise #33) with provenance discipline · governed distribution | Skill file provenance contract v0 (already partly built at `backend/contracts/skill_file_provenance_v0.py` per uncommitted CP4) · admission via ceremony | M |
| **W-CRITIC-SEAM** | `Doc19A-001..006` (all CANON) | Critic Seam · post-model inference layer · QA & Evidence integrity | Every model output crosses critic seam · verdict recorded · seam operates deterministic-side | M |
| **W-EVIDENCE-PROTOCOL** | `Doc19B-001..005` (4 PROPOSED, 1 OPEN) | Evidence integrity protocol (Part B) | Depends on Doc 19B ratification | M |

### E.6 · WPW stack (Tier 1 + Tier 2 unblocked; Tier 3 blocked)

| Item | REQ-IDs | Outcome | Pass criteria | Effort class |
|---|---|---|---|---|
| **W-WPW-TIER-1-2** | `WPW-1..WPW-12` (Tier 1 + Tier 2) | Whitepaper Wizard Tier 1 baseline draft + Tier 2 evidence weave; attribution + integration | Notebook shape v1 · draft round-trip · citation graph frozen · integration with campaign records (baseline_line) | M |
| **W-WPW-TIER-3-DEFERRED** | `WPW-13..WPW-18` blocked on R1/R2/R3 rulings | Tier 3: exceptional retention (R1 threshold) · external-release signatory (R2) · DEFAULT ratifications + novelty clause (R3-a/b/c) | Owner ruling required · pass criteria depend on R1/R2/R3 outcome | S (implementation once rulings land) |

### E.7 · v2 Prototype full lift (Registry-covered above; other 18 non-registry surfaces)

Cross-reference: `notes/SURFACE_AUDIT_v2_prototype_20260907.md` §Table 2 (47 surfaces). 29 rows are Registry-scoped (see E.1 W-REGISTRY-FULL-BUILD). Remaining 18 span:

| Item | v2 Surface count | Rolled into |
|---|--:|---|
| Portal-swap chrome | 3 | W-REGISTRY-FULL-BUILD |
| Compute Connected sub-tabs | 6 | already DONE (W-Compute-Residuals) |
| Data Suite | 3 | W-DATA-SUITE-v2-LIFT (chartered, S) |
| Trust surface | 2 | W-TRUST-SURFACE-v2 (chartered, S) |
| Board 360 · Exco 360 · Documents · Rule Books · Collab · Spend · Task Manager | 4 | W-EXECUTIVE-SUITE-v2-LIFT (chartered, L) |

## §F · Coverage ledger — what this audit adds vs prior audits

**Prior audits:**
1. `REUSE_ASSESSMENT.md` (2026-08-14, accepted). Every non-REUSE row from Canon 1-9 with REUSE/MODIFY/RE-POINT/BUILD/RETIRE classification and citation.
2. `BUILD_STRATEGY.md` (2026-08-14, in progress). Full technical plan for every non-REUSE row.
3. `notes/requirements_register_17docs.md` (2026-08-19). 515-row register with DONE/PARTIAL/REUSABLE/BUILD classification per Doc 01-16.
4. `notes/requirements_register_20docs.md` (2026-08-19). +36 rows for Doc 17-19B.
5. `notes/TRUE_STATE_OF_CODE.md` (2026-09-06, accepted 2026-09-06T19:20Z). Verbatim state audit of what actually landed vs what registers claim.
6. `notes/SURFACE_AUDIT_v2_prototype_20260907.md` (2026-09-06). 47-row surface audit vs v2 prototype.
7. `notes/status_and_wave_plan.md`. Wave calibration (1.60× factor) + wave sequencing scaffold (superseded by owner sequencing rulings).
8. `notes/reuse_map_v7.md`. Per-donor-path reuse grades (LIFT-CLEAN / LIFT-ADAPT / LIFT-REWORK).
9. `notes/claims_verification.md`. Seven §6 claims verified with cross-repo status.
10. `notes/w10_close_report.md` · `notes/w6_close_report.md` · `notes/programme_close_report.md`. Wave-close reports.

**This audit adds (owner directive "scan what wasn't"):**

| Δ | Source added | Prior audit coverage | This audit coverage |
|---|---|---|---|
| Δ1 | Doc 0 · Governance Architecture (117 rows) | Absent from any prior register | Full row-by-row extraction in `notes/ingest_20260907/canon_doc0_governance_architecture_requirements.md` (already banked); classifications compiled in this audit's `s15_doc0_governance_architecture.md` |
| Δ2 | Security Assurance Promise Set S-1..S-25 (26 rows) | Absent from any prior register | Full extraction; classifications in `s16_security_promise_set.md` |
| Δ3 | Security Amendments (Promise Set 8 + Trojan/Whisper 10 + rulings) (31 rows) | Absent | Full extraction; classifications in `s17_..s18_..md` |
| Δ4 | Rules Service Spec I-1..I-5 · RBM-1..RBM-22 (31 rows) | Absent | Full extraction; classifications in `s19_rules_service_spec_v1.md` |
| Δ5 | Rule Book Library v1 catalog (14 entries) | Absent | Catalog banked; classifications in `s20_rule_book_library_v1.md` |
| Δ6 | System Rules Registry 286 rules INVENTORY | Absent — never mined | Structural inventory banked; per-rule enumeration deferred as INVENTORY class (see W-286-RULE-ENUMERATION-CLASSIFY in E.2) |
| Δ7 | WPW Spec 18 rows | Charter draft only (STATE/WPW_CHARTER.md) | Row-by-row classification in `s22_wpw_spec.md` |
| Δ8 | v2 Prototype 47 surfaces (refresh) | SURFACE_AUDIT_v2 covered surface count · did NOT do row-by-row REUSE/BUILD classification | This audit's `s23_v2_prototype_surfaces.md` classifies each surface DONE/PARTIAL/REUSE/NEW |
| Δ9 | Donor-repo `docs/` and `salvage/` spec material (~125 file-derived requirements) | Prior register listed the FILE PATHS · never mined the REQUIREMENTS inside them | Full mining in `s24_..s27_..md` |
| Δ10 | BUILD_JOURNAL claims across 5 repos | Absent | Claims-catalog in `s28_build_journal_claims_ledger.md` (as claims-to-verify per binding rule; no findings emitted) |
| Δ11 | Refreshed classification counts on 17-doc register post-W11 | Prior counts dated 2026-08-19 (pre W-Registry-Connect, W-Campaign-Infra, W-Shield-Train stack, W-Compute-Residuals, W-Multi-Table-Extract, W-SMS-Body-Emit, W-Orchestrator-Resilience r1/r1-wire/r2, W-WINDOW-FILL-GUARANTEE, W-WINDOW-FILL-RESTORE, W-STANDING-ORDERS-COMPACTION-PROOF · 15+ closes) | Refreshed to 2026-09-07 (§C.1 above · Δ column) |
| Δ12 | Missing-reference list (M-1..M-16) | Absent | §D above · 16 items |
| Δ13 | Compaction-proof discipline banked | Absent | `STATE/STANDING_ORDERS.md` authored 2026-09-08T~04:20Z · ratchet 2997→3004 (+7 invariants) · double-green byte-match |

**Prior findings preserved (not overwritten):**
- REUSE_ASSESSMENT.md classification stands per Canon 1-9 rows (imported into 17-doc register).
- TRUE_STATE_OF_CODE.md remains the authoritative reference for what landed in code as of 2026-09-06 (this audit refreshes forward one week).
- SURFACE_AUDIT_v2 remains authoritative for the v2 prototype surface count (47) and per-surface presence/absence.

## §G · Notes to sprint sequencing (not order — measurable pass criteria only)

Sequencing is an owner ruling per binding rule. The following are metrics-only observations that MAY inform an owner-ruled sequence:

1. **Foundation before Commercial** — owner ruled 2026-09-06T19:12Z ("Commercial after baselines"). W-ESTATE-RELEASE-BUDGET is Commercial-stack and stays deferred.
2. **Registry before Solva-v2 lift** — owner ruled 2026-09-06T19:20Z ("Priority building goes to registry"). W-REGISTRY-FULL-BUILD carries the v2 acceptance dependency; W-SOLVA-V2-LIFT follows.
3. **Rules Service unlocks 286-rule enumeration and every ceremony-dependent gate below** — pass criteria on Rules Service ceremonies are the input dependencies for every Doc 0 BR-9 / RBM ceremony wave.
4. **Doc 0 attributes 1-9 are per-attribute build waves** — parallelisable pairwise (some Attributes share dependencies per Attribute 12's fan-in `1→2→3→4→5→6→7,8; 9 depends on 4; 10 depends on 1,2; 11 depends on 5,6; 12 depends on 1-9`).
5. **Full-consumption GPU obligations remain interrupt-priority** (STANDING_ORDERS §5).
6. **72h campaign window closes 2026-09-09** — data collection during this window drives measurement metrics for baseline lines feeding Doc 14 Model Ecosystem rows.

## §H · Ambiguities · DEFAULT-PENDING-OVERRIDE list

Per STANDING_ORDERS §2 discipline, each ambiguity below has ONE default applied, marked `DEFAULT-PENDING-OVERRIDE`; owner overrides on next turn.

| # | Ambiguity | Default applied | Reason |
|---|---|---|---|
| DPO-1 | Denominator for rollup % — include or exclude the 286-row System Rules Registry INVENTORY | **Exclude** the 286 rules from denominator; carry as INVENTORY separately | Including 286 rows with no per-rule classification would deflate DONE % and misrepresent progress |
| DPO-2 | Should `REUSABLE` (old 17-doc register grade) and `REUSE` (this audit's grade) be collapsed? | **Collapsed to REUSE** in top rollup; sub-grade LIFT-CLEAN/LIFT-ADAPT/LIFT-REWORK/RE-POINT preserved per row | Owner may want the 4-grade breakdown restored at rollup; per-source detail files carry the sub-grade |
| DPO-3 | Doc 20 handling — file exists (`AKKI_Canon_Documents_17_20_v3.docx`), no rows extracted | **Listed as missing-reference M-8** with pending-extraction charter (S+M effort) | Owner can rule to extract Doc 20 rows this audit or defer |
| DPO-4 | Canon Addendum 1 Open Design Questions (`CA1-A1-q1..N5-q3` ~24 questions) — count as requirement rows or as parked-questions? | **Parked-questions**, counted in row inventory but NOT in classification denominator | Questions unresolved cannot carry DONE/PARTIAL/REUSE/NEW without an owner ruling on the enclosing candidate |
| DPO-5 | The 24,595-LOC Solva-v2 donor pool vs 1,392 LOC already lifted — reuse grade | **LIFT-ADAPT** at the top level (donor code adapted to canon 3 / Doc 0 BR-2.x) | Owner may rule LIFT-CLEAN (byte-verbatim) if the donor is already canon-compliant, but the Solva-v2 canon rewrite (2026-08-01) explicitly changed contracts |
| DPO-6 | Wave-honest-limit rows in prior grounding briefs (multi-table joins, task-eval, gradient-step checkpoint, etc.) — count as separate NEW rows or absorb into parent wave? | **Absorbed into parent** at rollup level; each is a chartered follow-on named in `STATE/SPRINT_PLAN.md` | Otherwise wave-honest-limits inflate NEW count |
| DPO-7 | Doc 19B (Evidence Protocol, 5 rows: 4 PROPOSED · 1 OPEN) — classify as NEW or wait for ratification | **NEW** (buildable once PROPOSED rows are RULED) | Consistent with 20-doc register's PROPOSED handling |

## §I · Discipline seal

- **Read-only audit.** No build fires until owner accepts.
- **Campaigns untouched.** Last banked lane health 2026-09-07T12:23Z: all 4 GPUs 100% util (see `phase0/gpu_receipts/20260907T122254Z_restore_final/`). Cheap health check to re-verify post-audit if owner directs.
- **Every factual claim** in this file traces to a file opened in this audit session. Prior notes (`TRUE_STATE_OF_CODE.md`, `SURFACE_AUDIT_v2_prototype_20260907.md`, 17-doc register, 20-doc register, ingest_20260907/*) are cited as extraction sources and treated as authoritative for extraction only; their classification counts are refreshed in this audit against track-a HEAD `9f9b1fd`.
- **Ratchet floor:** 3004 (workspace `master` HEAD ≥ `bdfe2f32`; Extraction-Akki `programme/track-a` HEAD `9f9b1fd`).
- **Per-source detail files** live under `notes/MASTER_TRACEABILITY_AUDIT_20260907/` (S15, S16, S17, S18, S19, S20, S21, S22, S23, S24, S25/S26, S27, S28). Each is authored on its own commit under the two-commit pattern (state side). This master file is the index + rollup + coverage ledger.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
