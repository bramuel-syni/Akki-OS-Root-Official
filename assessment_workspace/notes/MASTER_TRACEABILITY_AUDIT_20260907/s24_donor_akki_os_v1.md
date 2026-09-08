# S24 · Donor · Akki-OS-V1 spec material · Detail Classification

**Repo:** `/app/assessment_workspace/repos/Akki-OS-V1/` · HEAD `8c361903` (main, 2026-08-14) · 167 total commits.
**Coverage:** Owner directive "scan what wasn't". Prior 17-doc + 20-doc registers listed some paths but did NOT mine per-file requirements.

## §A · Requirements catalog (11 files · 1,465 total lines)

| Row ID | File | Lines | Anchor | Classification | Notes |
|---|---|--:|---|---|---|
| A24-1 | `docs/requirements/cif_spec_v1.md` | 184 | CIF · Conditioned Ideation Faculty v1.0 (owner-ratified 2026-07-23) | REUSE (LIFT-ADAPT into Extraction-Akki) | Full CIF mechanic spec; covers §1..§14 (promise · principle · systems · vocabulary · mechanics · quality · enforce · execute). This is the CIF donor for Doc 0 §Attribute 10 BR-9.x. |
| A24-2 | `docs/requirements/critic_seam_spec_v1.md` | 174 | Critic Seam v1.0 | REUSE | Underpins Doc 19A rows (Doc19A-001..006 in 20-doc register) |
| A24-3 | `docs/requirements/critic_seam_spec_v1_1.md` | 29 | Critic Seam v1.1 (delta only) | REUSE | Amendment; layer on top of A24-2 |
| A24-4 | `docs/requirements/eab_tier1_adoption_spec_v1.md` | 202 | EAB Tier-1 Adoption (v1) | REUSE | Pre-perception restructuring · Occurrence index · Coverage-gap refusal · Per-batch quarantine · Precomputed evidence · Gate folds (F1/F2 into Operating Values v1.1) |
| A24-5 | `docs/requirements/eab_tier1_adoption_spec_v1.1.md` | 216 | EAB Tier-1 v1.1 (amendment · adopted 2026-07-14) | REUSE | 5 mechanics + 2 gate folds explicitly named; explicit non-adoptions ("shard-as-atomic-unit REJECTED"; "budget-capped priority scheduling NOT a new scheduler") |
| A24-6 | `docs/requirements/extraction_derisking_spec_v1.md` | 34 | Extraction De-risking v1 | REUSE (small · easy LIFT-CLEAN) | Feeds Doc 03 · Intent & Security Monitoring |
| A24-7 | `docs/requirements/operating_values_v1.md` | 132 | Operating Values v1 | REUSE | FACT/NORM/DEFAULT evidence classes; drives WPW's evidence_class grammar |
| A24-8 | `docs/requirements/operating_values_v1_1.md` | 93 | Operating Values v1.1 (amendment) | REUSE | Gate folds F1/F2 from A24-5 |
| A24-9 | `docs/requirements/s1_memory_model_spec_v1.md` | 121 | S1 Memory Model v1 | REUSE | Doc 08 · Warm/fresh · Memory & Retrieval donor |
| A24-10 | `docs/requirements/training_techniques_spec_v1.md` | 103 | Training Techniques v1.0 (owner-ratified 2026-07-17) | REUSE | Anchors Doc 17-004..010 in 20-doc register (T-1..T-4 including Muon adoption) |
| A24-11 | `docs/requirements/transformation_quality_spec_v1.md` | 177 | Transformation Quality v1 | REUSE | Anchors Doc 19A-004..005 (Part A rows tied to §7 in this spec) |

## §B · Mandates catalog (10 files)

| Row ID | File | Lines | Anchor | Classification |
|---|---|--:|---|---|
| A24-M1 | `docs/mandates/MANIFEST.md` | 96 | Catalog of mandates | REUSE (index) |
| A24-M2 | `docs/mandates/RMS_Build_Completion_Requirements_v1_4.md` | 341 | Build completion v1.4 | REUSE |
| A24-M3 | `docs/mandates/RMS_Build_Completion_Requirements_v1_5.md` | 359 | Build completion v1.5 (amendment) | REUSE |
| A24-M4 | `docs/mandates/RMS_Mtafiti_Specification.md` | 501 | Mtafiti (Registry) full spec | REUSE (LIFT-ADAPT into Doc 10) |
| A24-M5 | `docs/mandates/RMS_Product_Engineering_Spec_v3.md` | 197 | Product engineering v3 | REUSE |
| A24-M6 | `docs/mandates/RMS_Solva_Specification.md` | 455 | Solva full spec | REUSE (feeds W-SOLVA-V2-LIFT) |
| A24-M7 | `docs/mandates/RMS_SyniSense_Specification.md` | 171 | SyniSense (Shield) full spec | REUSE (feeds Doc 01/02) |
| A24-M8 | `docs/mandates/RMS_Targeta_Specification.md` | 479 | Targeta full spec | REUSE (Doc 13 Autonomous Training) |
| A24-M9 | `docs/mandates/RMS_UI_Specification_v1.md` | 116 | UI spec v1 | REUSE (superseded by prototype v2) |
| A24-M10 | `docs/mandates/RMS_UI_Specification_v2_1.md` | 207 | UI spec v2.1 | REUSE (aligned with v2 prototype surfaces) |

## §C · g4_prep + build_briefs + production_housing (10 files)

| Row ID | File | Anchor | Classification |
|---|---|---|---|
| A24-G1 | `docs/g4_prep/service_1_v1_scope_from_source.md` | Service 1 v1 scope | REUSE |
| A24-G2 | `docs/g4_prep/mtafiti_scope_from_source.md` | Mtafiti scope | REUSE (cross-ref A24-M4) |
| A24-G3 | `docs/g4_prep/targeta_scope_from_source.md` | Targeta scope | REUSE (cross-ref A24-M8) |
| A24-G4 | `docs/g4_prep/OPEN_GOVERNANCE.md` | Open governance items | REUSE |
| A24-G5 | `docs/g4_prep/targeta_prep.md` | Targeta prep | REUSE |
| A24-G6 | `docs/g4_prep/mtafiti_prep.md` | Mtafiti prep | REUSE |
| A24-G7 | `docs/build_briefs/phase_8_seam_3_sub_stage_1.md` | Phase 8 seam 3 · sub-stage 1 | INVENTORY (build-brief, claim-to-verify) |
| A24-P1 | `docs/production_housing/env_findings_v0.md` | Env findings | INVENTORY |
| A24-P2 | `docs/production_housing/llm_swap_seam.md` | LLM swap seam | REUSE |
| A24-P3 | `docs/production_housing/promotion_audit_v0.md` | Promotion audit v0 | INVENTORY |
| A24-P4 | `docs/production_housing/frontend_backend_split.md` | Frontend-backend split | INVENTORY |

## §D · S24 rollup

**Total rows this file: 32** (11 requirements + 10 mandates + 11 g4/build/production).

| Bucket | Rows | % of 32 |
|---|--:|---:|
| REUSE | 27 | 84.4% |
| INVENTORY (build-brief / production-housing) | 5 | 15.6% |
| DONE / PARTIAL / NEW | 0 | 0.0% |

**Interpretation:** Akki-OS-V1 is a **content-donor repo** — no rows are DONE/PARTIAL/NEW at S24 level; every requirement file is a REUSE candidate feeding another audit source (Doc 17-19B, Doc 04 Reasoning/Solver, Doc 08 Memory, Doc 10 Registry, Doc 13 Training). Total donor lines: **1,465 requirements + 2,922 mandates + ~700 g4/build = ~5,100 lines** of spec material to lift.

**Full per-row extraction (of the ~5,100 lines) is deferred as INVENTORY.** Wave charter: **W-DONOR-MINE-AKKI-OS-V1** (L effort) — extract every REQ-tagged bullet into a projectable row-shaped register, cross-link to 17/20-doc register rows.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
