READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# LEVERAGE_AND_GAP_INVENTORY_20260913.md

**Purpose.** Complete leverage-and-gap inventory from disk truth, answering the owner concern: *"we have been under-leveraging work that is already DONE, and mis-grounding as a result."* Read-only, document-only, evidence-backed. Every claim cites a file, grep, commit, or hash opened this session. `[framing, not canon]` tags mark my interpretation.

**Standing.** ROLE OVERRIDE in force · Phase-1 Canon Assessment · NO production code · do NOT touch the three untracked DAP / Registry-CP10 working-tree files · local commits only, NEVER push · NO egress · HALT rather than guess (SO §3).

**Date.** 2026-09-13.

**Ratchet floor at write time.** 3562 (`repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json` · `counts_at_baseline.passed = 3562` · `passed_floor = 3562`; matched).

---

## A. FULL WAVE LINEAGE — the authoritative "what is already built"

Parsed from `baseline_failures.json.ratchet_history` (73 entries total). Column meanings: **#** = ordinal in `ratchet_history` list · **UTC** = `at_utc` · **commit** = commit-hex first 8 chars from field (`PENDING` = commit field present as literal string in the older rows; `??` = field missing/older schema) · **passed** = `passed` value at close · **Δ** = delta from prior entry · **wave/CP label** = extracted from `cp` field (truncated).

`[framing, not canon]` — I have grouped entries by wave family in the label column to make the lineage legible; the raw `cp` strings are the canonical record.

| # | UTC | commit | passed | Δ | wave / CP |
|--:|---|---|--:|--:|---|
| 1 | 20260827T075209Z | `18748a3` | 1932 | — | CP-D1a (partial close) |
| 2 | 20260827T081200Z | PENDING | 1944 | +12 | CP-D-guard (baseline no-new-breakage guard) |
| 3 | 20260827T085000Z | PENDING | 1961 | +17 | CP-D2 close |
| 4 | 20260827T091500Z | PENDING | 1976 | +15 | CP-D3 |
| 5 | 20260827T094100Z | PENDING | 1982 | +6 | CP-D4 |
| 6 | 20260827T102000Z | PENDING | 2041 | +59 | CP-D5 |
| 7 | 20260827T104500Z | PENDING | 2066 | +25 | CP-D6 |
| 8 | 20260827T113000Z | PENDING | 2084 | +18 | CP-D7 |
| 9 | 20260827T114500Z | PENDING | 2119 | +35 | CP-D8 |
| 10 | 20260827T132858Z | PENDING | 2127 | +8 | CP-E1 |
| 11 | 20260827T134130Z | PENDING | 2138 | +11 | CP-E2 |
| 12 | 20260827T135155Z | PENDING | 2147 | +9 | CP-E3 |
| 13 | 20260827T135837Z | PENDING | 2158 | +11 | CP-E4 |
| 14 | 20260827T140432Z | PENDING | 2160 | +2 | CP-E5 |
| 15 | 20260827T140840Z | PENDING | 2164 | +4 | CP-E6 |
| 16 | 20260827T141354Z | PENDING | 2169 | +5 | CP-E7 |
| 17 | 20260827T205136Z | PENDING | 2333 | +164 | W11 F |
| 18 | 20260827T220103Z | PENDING | 2355 | +22 | Wave F Cleanup |
| 19 | 20260828T012205Z | PENDING | 2363 | +8 | Wave G Step 1 |
| 20 | 20260828T045000Z | PENDING | 2389 | +26 | Wave G Step 2/3 |
| 21 | 20260828T065000Z | PENDING | 2463 | +74 | Wave G2 |
| 22 | 20260828T112138Z | PENDING | 2488 | +25 | Wave G3 |
| 23 | 20260828T122400Z | PENDING | 2566 | +78 | Wave G4 |
| 24 | 20260828T133507Z | ?? | 2589 | +23 | Wave-H |
| 25 | 20260828T142951Z | ?? | 2590 | +1 | Wave-H G5 INTERRUPT 3 |
| 26 | 20260828T144311Z | ?? | 2594 | +4 | Wave-G5b |
| 27 | 20260828T145000Z | ?? | 2611 | +17 | Wave-G5b |
| 28 | 20260828T151542Z | ?? | 2636 | +25 | Wave-G5c-CENSUS |
| 29 | 20260828T152747Z | ?? | 2649 | +13 | Wave-G5c-COMPUTE-BACKEND |
| 30 | 20260828T155222Z | ?? | 2669 | +20 | Wave-G5c-RULINGS-1-2-5 |
| 31 | 20260828T161023Z | ?? | 2680 | +11 | Wave-G5c-COMPUTE-FRONTEND (declared) + REGISTRY-SURFACE-CENSUS-WIRING |
| 32 | 20260831T203335Z | ?? | 2692 | +12 | W-G5c-close |
| 33 | 20260831T213000Z | ?? | 2703 | +11 | W-G5c-COMPUTE-v2-close |
| 34 | 20260831T220000Z | ?? | 2717 | +14 | **W-WPW-v1-c-close** (Tier 1 lab notebook) |
| 35 | 20260906T095000Z | ?? | 2732 | +15 | **W-WPW-v1-d-close** (Tier 2 technical report) |
| 36 | 20260906T102809Z | ?? | 2748 | +16 | W-Orchestrator-Resilience-r1-close |
| 37 | 20260906T104252Z | ?? | 2762 | +14 | W-Orchestrator-Resilience-r1-wire-close |
| 38 | 20260906T111530Z | ?? | 2786 | +24 | W-Orchestrator-Resilience-r2-close |
| 39 | 20260906T113500Z | ?? | 2836 | +50 | **W-Shield-Train-build-close** |
| 40 | 20260906T120800Z | ?? | 2847 | +11 | W-G5c-COMPUTE-RESIDUALS-close |
| 41 | 20260906T122600Z | ?? | 2893 | +46 | W-Campaign-Infra-close |
| 42 | 20260906T124300Z | ?? | 2894 | +1 | W-Shield-Train-Admission-close |
| 43 | 20260906T140000Z | ?? | 2924 | +30 | W-Shield-Train-run-close |
| 44 | 20260906T143700Z | ?? | 2956 | +32 | W-Multi-Table-Extract close |
| 45 | 20260906T162500Z | ?? | 2976 | +20 | W-SMS-Body-Emit close |
| 46 | 20260906T164000Z | ?? | 2978 | +2 | W-SMS-Body-Emit (correction) |
| 47 | 20260906T183500Z | ?? | 2986 | +8 | W-COMPUTE-MAXIMIZE close |
| 48 | 20260906T195250Z | ?? | 2991 | +5 | W-WINDOW-FILL-GUARANTEE close |
| 49 | 20260907T120932Z | ?? | 2997 | +6 | W-WINDOW-FILL-RESTORE close |
| 50 | 20260908T042100Z | PENDING | 3004 | +7 | W-STANDING-ORDERS-COMPACTION-PROOF close |
| 51 | 20260908T050000Z | PENDING | 3006 | +2 | W-WINDOW-FILL-RESTORE-2 close |
| 52 | 20260908T060000Z | PENDING | 3006 | +0 | W-STANDING-ORDERS-MISSION-FRAMED close |
| 53 | 20260909T115200Z | `7f3c8cc` | 3017 | +11 | W-TRACKING-DEFECT-FIX close |
| 54 | 20260909T120400Z | `a5324dd` | 3040 | +23 | W-INGEST-AC-SPEC + W-RULING-LEDGER-STEP3 close |
| 55 | 20260909T121500Z | `318e7cd` | 3064 | +24 | **W-REGISTRY-FULL-BUILD CP1 close** |
| 56 | 20260909T122300Z | `41bec22` | 3078 | +14 | W-REGISTRY-FULL-BUILD CP2+CP3+CP4 close |
| 57 | 20260909T123500Z | `10fcc06` | 3086 | +8 | W-REGISTRY-FULL-BUILD CP5+CP6+CP7 close |
| 58 | 20260909T124300Z | `5b7a490` | 3093 | +7 | W-REGISTRY-FULL-BUILD CP8 close |
| 59 | 20260909T125100Z | `3a5584c` | 3098 | +5 | **W-REGISTRY-FULL-BUILD CP9 close** (CP10 SHELVED on HOLD) |
| 60 | 20260912T060604Z | PENDING | 3164 | +66 | **W-MTAFITI-GPU-DISCOVERY CP1** (governance blind + guards) |
| 61 | 20260912T063200Z | PENDING | 3198 | +34 | W-MTAFITI-GPU-DISCOVERY CP2 (PII detector + redaction) |
| 62 | 20260912T065000Z | PENDING | 3212 | +14 | W-MTAFITI-GPU-DISCOVERY CP3 (**first live read** Weego/USSD) |
| 63 | 20260912T070500Z | PENDING | 3223 | +11 | W-MTAFITI-GPU-DISCOVERY CP4 (deep composition census) |
| 64 | 20260912T071500Z | PENDING | 3232 | +9 | W-MTAFITI-GPU-DISCOVERY CP5 |
| 65 | 20260912T072500Z | PENDING | 3241 | +9 | W-MTAFITI-GPU-DISCOVERY CP6 |
| 66 | 20260912T073500Z | PENDING | 3251 | +10 | **W-MTAFITI-GPU-DISCOVERY CP7 WAVE CLOSE** |
| 67 | 20260913T054400Z | `04d4ae9` | 3251 | +0 | CP0.a (silent-success ban surface enumeration) |
| 68 | 20260913T063000Z | `04d4ae9` | 3282 | +31 | **W0** (output-verified seal — silent-success ban) |
| 69 | 20260913T071000Z | `fe01e5e` | 3392 | +110 | **W1** (work-supervisor generic kernel · job_manifest · governance · runtime supervisor) |
| 70 | 20260913T081000Z | `5364593` | 3492 | +100 | **W1b** (platform primitives · kind_registry · attribute_stream_bundle · retention · capability_registry) |
| 71 | 20260913T083500Z | `e1712a1` | 3503 | +11 | **W1c** (platform integration proof · end-to-end spine walk) |
| 72 | 20260913T103202Z | `33edf56b` | 3531 | +28 | **W-REGISTRY-EXTENSION-G3 wave close** (Doc-0 G-3 half · 6 CPs) |
| 73 | 20260913T104829Z | `7f6d235a` | 3562 | +31 | **W-SOLVA-V2-LIFT wave close** (8 CPs · DPO-S2 HALT declared) |

### A.1 Gaps / anomalies flagged

1. **Commit field is `"PENDING"` (literal string) in entries 2–23 and 50–52, 60–66.** Older ratchet-history schema pre-dated commit backfill. Entries 24–49 have `??` (missing entirely). Entries 53–59, 67–73 carry real SHAs. The two most recent Registry-Extension-G3 and Solva-V2-Lift entries were **backfilled** in the follow-on commits `c5d5d6c` and `e2ae44b` (per git log). Older SHAs are recoverable via `git log --grep='CP-D1a'`-style if needed.
2. **Entry 52 has Δ=0** — W-STANDING-ORDERS-MISSION-FRAMED added invariants without moving the passed count. This is atypical; needs confirmation the invariants were correctly gated. `[framing, not canon]`.
3. **Ratchet climb is 3562 − 1932 = 1,630 invariants across 73 wave/CP closes** — the platform is materially built; this is the leverage the owner is asking us to see.
4. **NEXT.md top-marker (`## Current step marker`) still reads W-MTAFITI-GPU-DISCOVERY 3251** — 3 waves stale relative to `ratchet_history` (W1c → W-REGISTRY-EXTENSION-G3 → W-SOLVA-V2-LIFT closed after that marker was written). Book-keeping drift, not code drift.

---

## B. DELIVERABLE & STATE CATALOG (what already exists on disk)

### B.1 Root workspace deliverables

| Path | Bytes | Date | What it is |
|---|--:|---|---|
| `/app/assessment_workspace/REUSE_ASSESSMENT.md` | 53,479 | 2026-08-14 | Chunk-3 REUSE/MODIFY/RE-POINT/BUILD/RETIRE assessment; PINS says ACCEPTED. |
| `/app/assessment_workspace/BUILD_STRATEGY.md` | 250,939 | 2026-08-14 | Full build-strategy plan against Extraction-Akki as spine. |

### B.2 `STATE/` — permanent standing law + master state

| Path | Bytes | Date | Purpose |
|---|--:|---|---|
| `STATE/STANDING_ORDERS.md` | 14,103 | 2026-09-13 | Permanent standing law (SO §1..§3.2). |
| `STATE/PINS.md` | 29,939 | 2026-09-13 | Repo/canon/deliverable/tool pins. Canon block last touched 2026-08-14. |
| `STATE/NEXT.md` | 183,401 | 2026-09-12 | Anti-compaction ledger; top-marker now 3 waves stale. |
| `STATE/DECISIONS.md` | 825,102 | 2026-09-13 | Append-only owner-ruling log (verbatim). |
| `STATE/HOLISTIC_PLAN.md` | 42,752 | 2026-09-12 | Holistic programme plan. |
| `STATE/SPRINT_PLAN.md` | 27,856 | 2026-09-06 | Sprint plan (superseded by wave discipline). |
| `STATE/CONTEXT.md` | 58,843 | 2026-08-26 | Wave-A/B/C context reference. |
| `STATE/WPW_CHARTER.md` | 14,747 | 2026-08-31 | Whitepaper-Wizard charter. |
| `STATE/ORCHESTRATOR.md` | 11,192 | 2026-08-15 | Orchestrator reference. |

### B.3 `notes/` — assessments, roadmaps, audits, wave briefs, canon extractions

Grouped by category; every path exists on disk.

**Assessment & rollup:**
- `MASTER_TRACEABILITY_AUDIT_20260907.md` (49,873 B · 2026-09-08) — 1,159-row master traceability across 24 spec IDs.
- `MASTER_TRACEABILITY_AUDIT_20260908_UPDATE.md` (16,961 B · 2026-09-09) — Doc-15 O15 +12 AC rows update; 1,159 → 1,171.
- `MASTER_TRACEABILITY_AUDIT_20260909_UPDATE.md` (9,220 B · 2026-09-09) — DPO-1..7 named + defaults.
- `MASTER_TRACEABILITY_AUDIT_20260907/` (subdir · 8 shard files) — per-donor detail.
- `BUILD_STATUS_PERCENT_20260909.md` (24,513 B · 2026-09-10) — **component-by-component completion % table** (15 rows). Referenced heavily in §E below.
- `TRUE_STATE_OF_CODE.md` + `TRUE_STATE_matrix.json` (38K + 27K · 2026-09-06) — code-vs-canon reconciliation.
- `SILENT_FAILURE_ROOTCAUSE_AND_LAYER_MAP.md` (41,681 B · 2026-09-13) — silent-failure taxonomy and layer map (paired with W0 close).
- `akki_holistic_inventory.md` (18,922 B · 2026-09-01) — holistic inventory of components.

**Charters & framing:**
- `SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md` (62,547 B · 2026-09-13) — mission charter.
- `GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md` (51,814 B · 2026-09-13) — roadmap.
- `PHASE_C_SYSTEMATIC_BUILD_PLAN.md` (36,635 B · 2026-09-13) — W-REGISTRY-EXTENSION-G3 · W-DAP-STACK · W-SOLVA-V2-LIFT plan.
- `JOURNEY_AND_ASSISTANT_AUDIT_20260913.md` (14,216 B · 2026-09-13) — journey/assistant canon audit.

**Rulings / claims / registers:**
- `RULING_LEDGER.md` (4,479 B · 2026-09-09) — 5 RATIFIED / 9 DEFAULT / 1 COUPLED / 4 OPEN.
- `NON_CLAIMS_REGISTER.md` (4,617 B · 2026-09-09) — 5 LIM-* non-claims.
- `claims_verification.md` (20,102 B · 2026-08-14) — 7 §6 claims verified.
- `fidelity_ledger.md` (27,734 B · 2026-08-14) — open questions.
- `spec_id_index.md` + `spec_id_index.json` (5K + 22K · 2026-09-09) — 24 spec IDs (18 BANKED / 1 BANKED-DERIVED / 5 MISSING).
- `models_roster.json` (27,220 B · 2026-09-09) — 78 unique run_ids.
- `function_promise_registry.jsonl` (2,407 B · 2026-09-13) — F&P Registry seed.

**Canon requirements extractions (already banked):**
- `canon_1..9_requirements.md` (2026-08-14) — 559 rows.
- `canon_addendum_1_requirements.md` (17,310 B · 2026-08-27) — Addendum 1 rows.
- `canon_agent_containment_spec_v1_requirements.md` (8,302 B · 2026-09-09) — Agent-Swarm-Containment rows (12 AC-* + 5 LIM-* non-claims).
- `requirements_register_17docs.md` (30,788 B · 2026-08-27) — 17-doc requirements register.
- `requirements_register_20docs.md` (23,123 B · 2026-08-27) — 20-doc register.
- `row_to_item_index.md` (30,571 B · 2026-08-14) — row-to-work-item mapping.

**Domain tables + inventories:**
- `domain_5_1..10.md` (2026-08-14) — 10 Doc-5 domain tables.
- `build_inventory.md` (8,538 B · 2026-08-14) — 148 BUILD rows + 9 HARVEST clusters.
- `retire_inventory.md` (6,862 B · 2026-08-14) — 37 retires + 7 renames.
- `strategy_items_part1.md` + `part2.md` (101,813 + 70,870 B · 2026-08-14) — full strategy items.
- `reuse_map_v7.md` (16,018 B · 2026-08-25) — REUSE mapping v7.

**Prototype inventories (3 versions):**
- `prototype_inventory.md` (15,346 B · 2026-08-14) — v6 standalone.
- `prototype_inventory_v7.md` (18,870 B · 2026-08-28) — v7 refresh.
- `prototype_inventory_v8.md` (57,275 B · 2026-08-28) — v8 (broader, current widest).
- `SURFACE_AUDIT_v2_prototype_20260907.md` (41,898 B · 2026-09-07) — surface audit of v2 standalone.

**Wave briefs & close reports (30+ files):**
- Wave close/grounding docs at `w3..w11_*.md`, `waveA..waveG_*.md`.
- W1 / W1b / W1c grounding + close docs (2026-09-13).
- `W_MTAFITI_GPU_DISCOVERY_grounding_brief.md` + `_wave_close.md`.
- `W_REGISTRY_FULL_BUILD_grounding_brief.md` + `_close.md` (2026-09-09).
- `W_REGISTRY_EXTENSION_G3_grounding_brief.md` + `_close.md` (2026-09-13).
- `W_SOLVA_V2_LIFT_grounding_brief.md` + `_close.md` (2026-09-13).
- `DPO_S2_REFLECTION_CANDIDATES_20260913.md` (9,630 B) — reflection contract HALT candidates.

**Audio-specific extracts (drop 2026-09-09):**
- `AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md` (102,393 B · 2026-09-13).
- `AUDIO_AUTONOMOUS_JOURNEY_CAPABILITY_ASSESSMENT.md` (74,550 B · 2026-09-13).
- `W_AUDIO_POC_SCOPING_20260912.md` (40,584 B).

**Chunk-1 outputs (2026-08-14):**
- `chunk1_summary.md` · `cross_repo_overlap.md` · `repo_summaries.md` · `prototype_inventory.md` · `_raw_repo_trees.txt` · `_raw_services.txt` · `_raw_service_diff.md`.

### B.4 `phase0/` — receipts, seals, proofs, drills

- **`drill_receipts/`** — 449 RED/GREEN receipts across all closes; every mechanical-RED + double-green banked here.
- **`output_verified_seals/`** — 2 seals present: `registry_extension_g3.seal.txt` (2026-09-13 10:32) + `solva_v2_lift.seal.txt` (2026-09-13 10:58).
- **`commissioning_records/`** — 2.1 MB of commissioning receipts (latest 2026-09-13T10:55).
- **`crossing_receipts/`** — 39 MB of governed crossing receipts.
- **`northena_ledger/`** — 88 MB of ledger records.
- **`mtafiti_gpu_discovery/`** — 17 MB of GPU-discovery deep-census + live-probe receipts (Weego 21 schemas / 1,637 tables / 18,316 columns / 181,708,249 rows).
- **`shield_train_receipts/`** — 70 MB of Shield-Train pipeline receipts.
- **`gpu_receipts/`** + **`gpu_burn/`** — 3.5 MB + 804 KB training-run receipts.
- **`storage_survey/`** — 43 MB storage-survey receipts.
- **`campaign_drafts/`**, **`training/`**, **`training_runner/`**, **`text_train_pipeline/`** — campaign + trainer receipts.
- **`wpw_notebook/`** + **`wpw_tier2_demo/`** — WPW receipts (Tier 1 notebook + Tier 2 demo).
- **`whitepapers/`** — 36 KB whitepaper receipts.
- **`harness_ground_truth/`** — 416 KB harness ground-truth (latest 2026-09-12T06:01:36Z).
- **`integration_proofs/`** — empty on disk (the W1c trace at `phase0/integration_proofs/w1c_integration_proof_trace.md` per DECISIONS §W1c close item 8, but the dir itself lists empty — investigate at Phase-2 open · not blocking here).
- Watch-family dirs (`watch_actions/`, `watch_marks/`, `watch_verdicts/`, `watch_mirage_artifacts/`, `watch_sever_signals/`, `mirages/`, `mirage_touches/`, `severances/`, `witness_attestations/`, `witness_identities/`) — thin (4–12 KB); Watch mechanism largely NOT yet exercised.
- **`live_census_receipts/`**, **`census/`** — Northena census receipts.

---

## C. CAPABILITY INVENTORY — what's already implemented

**Method.** Every service dir under `backend/services/` on `programme/track-a` HEAD `e2ae44b0`, with `.py` file count + LOC + invariant-test-hit count (invariant tests referencing `services.<name>` or `services/<name>`). Full table computed in-session. `[framing, not canon]` — I have grouped by function; individual LOC-vs-substantive judgement is measured by LOC threshold + invariant coverage.

**Loose files at services/ root:** `__init__.py`, `capability_registry.py` (referenced by W1b), `system_state.py`.

### C.1 Platform substrate (W0 · W1 · W1b · W1c primitives) — **material**

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `output_verified_seal` | 1 | 183 | 8 | W0 · silent-success ban seal primitive (SO §3.1). |
| `work_supervisor` | 6 | 1,048 | 14 | W1 · generic job_manifest, kind_registry, governance, runtime_supervisor, supervisor. |
| `attribute_stream_bundle` | 1 | 127 | 6 | W1b · generic 5-ring unit contract (Canon-4 §30). |
| `capability_registry.py` (root file) | 1 | — | — | W1b · generic capability register. |
| `orchestrator_resilience` | 6 | 679 | 11 | Pod-side orchestrator resilience primitives. |
| `chokepoint` | 8 | 1,403 | 35 | Chokepoint discipline primitives. |
| `governance_plane` | 2 | 159 | 6 | Governance plane primitives. |
| `governance` | 2 | 129 | 8 | Governance primitives. |
| `ip_allowlist` | 2 | 168 | 4 | Source-IP allowlist middleware. |
| `estate_keys` | 2 | 86 | 2 | Estate keypair custody. |

### C.2 Registry family — **material for base register + partial for CP10**

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `registry` | 5 | 2,153 | 4 | Core register (Canon-1 §4.6, Canon-7 §35-40). |
| `registry_facts` | 3 | 354 | 4 | R-registry facts surface. |
| `w_registry_full_build` | 2 | 455 | 1 | 2026-09-09 CP1..CP9 wave (22 routes, payload contracts, real-data wires); **CP10 wave-close test SHELVED-UNTRACKED**. |
| `wizard` | 10 | 1,258 | 14 | Setup guided sequence (Canon-6 §3) + Connect Wizard chrome. |
| `credentials_paste` | 3 | 294 | 6 | Credentials-paste parser (data-source connect flow). |
| `connect` | 11 | 2,022 | 19 | Data-source connect (Aurora RDS Data API + estate connectors). |
| `connect_estate` | 2 | 131 | 4 | Estate-connect surface. |
| `data_source` | 5 | 739 | 1 | Data-source model. |
| `source_plane` | 3 | 229 | 5 | Source-plane primitives. |

### C.3 Reasoning stack — **Solva partial, Solva-v2 lifted this session (with HALT)**

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `solva` | 2 | 700 | 37 | Original reasoning surface (`reasoning.py`, 21,674 B) — 2026-08-25 · pre-lift. |
| `solva_v2` | 10 (nested engines dir) | 297 | 14 | **W-SOLVA-V2-LIFT close (2026-09-13)**: `assertion_boundary.py` (parameterless compute_class · Canon-4 §23.1), `critic_seam.py` (Tier-2 · Canon-7 §44/§44.1), `intent_audit.py` (§21.1), `reasoning_faculty.py`, `trace.py` (au_3b_defensible=False R-C2 marker), `engines/` (candidate_generation · tension_detector · reflection — **reflection.run() raises NotImplementedError · DPO-S2 HALT**). |
| `solva_depth` | 15 | 692 | 17 | Solva-depth companion (older). |
| `critic_pass` | 8 | 1,035 | 4 | Critic-pass mechanism (Canon-7 §44/§44.1 Tier-2). |

### C.4 DAP — **~5% (only rulings wired · scaffolding untracked)**

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `dap` | 2 | 107 | 1 | **UNBANKED scaffolding in working tree** (`contracts/dap.py` 288 lines + `services/dap/admission.py` 101 lines + test file 174 lines). Untracked. Not to be touched in Phase-1. |
| `rulings` | 2 | 137 | 3 | Where the 3 RATIFIED + 9 DEFAULT ruling constants live (`default_class_constants.py`). |

### C.5 Watch (Doc-03) — **thin scaffolding present, mechanism NOT built**

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `watch` | 15 | 2,787 | 54 | `containment.py`, `continuity.py`, `continuity_policy.v0.json`, `fitness.py`, `macho.py`, `mark.py`, `mirage.py`, `mirage_artifacts.py`, `mkono.py`, `persistence.py`, `route_recheck_failure.py`, `route_staleness_flag.py`, `router.py`, `sever_signals.py`, `witness.py`. **Watch primitives exist as file-level scaffolding but Doc-03 62-row BUILD list not exercised** per BUILD_STATUS_PERCENT-20260909 (~6%). |
| `grey_mirror` | 2 | 91 | 2 | Grey-Mirror thin. |
| `rights_quarantine` | 3 | 262 | 3 | Rights-quarantine mechanism. |
| `shield_train` | 6 | 1,120 | 17 | Shield-Train build (governed masking pipeline). |

### C.6 Whitepaper Wizard (WPW) — **Tier 1 + Tier 2 DONE at close-grade**

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `wpw` | 3 | 923 | 5 | `tier1_notebook.py` + `tier2_report.py` — closed at W-WPW-v1-c/d (ratchet 2717 → 2732). |
| `whitepapers` | 3 | 150 | 12 | `draft.py` + `router.py` — whitepaper routing. |

### C.7 Extraction + training pipeline — **material**

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `training` | 8 | 1,568 | 33 | Training kernel. |
| `training_runner` | 5 | 1,382 | 23 | Runner + campaign infra binding. |
| `campaign_infra` | 7 | 1,040 | 9 | Campaign lifecycle. |
| `model_admission` | 3 | 342 | 9 | Model admission chokepoint. |
| `model_registry` | 3 | 281 | 17 | Model registry. |
| `model_recheck` | 3 | 126 | 6 | Model recheck. |
| `synisense` | 18 | 2,826 | 12 | Executive-donor synisense subset (case-agnostic-only). |
| `perception` | 29 | 2,158 | 13 | Perception pipeline (a1_a5_eab_1). |
| `mtafiti` | 28 | 2,752 | 41 | **W-MTAFITI-GPU-DISCOVERY CP1..CP7 closed** — read-only guard, PII detector, redaction guard, live-probe, composition census, adaptive sampler. |
| `n_series` | 4 | 524 | 11 | N-series primitives. |

### C.8 Governed values + audit + ceremony

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `audit_trail` | 3 | 298 | 6 | Audit trail primitive. |
| `evidence_register` | 5 | 521 | 8 | Evidence register. |
| `approvals` | 4 | 407 | 8 | Approvals ceremony. |
| `declaration` | 2 | 86 | 6 | Actor-declaration seam (Assessment C3-008/9/10). |
| `outer_gate` | 4 | 285 | 8 | Outer-gate discipline. |
| `retention` | 5 | 619 | 8 | Retention policy. |
| `cost_ledger` | 4 | 497 | 6 | Cost ledger + metering. |
| `lowered_standard` | 3 | 305 | 2 | Lowered-standard ceremony. |
| `trace` | 3 | 211 | 2 | Trace primitive. |
| `handoff` | 2 | 75 | 2 | Handoff primitive. |
| `canonical_projection` | 2 | 88 | 22 | Canonical projection (heavy tests). |
| `contract_shells` | 1 | 122 | 3 | Contract shells. |
| `response_sanitizer` | 1 | 64 | 7 | Response sanitizer. |
| `baseline_line` | 3 | 102 | 4 | Baseline-line (Attr 7 partial). |

### C.9 Frontier / harness / integration

| Service | py | LOC | inv-tests | Purpose |
|---|--:|--:|--:|---|
| `service_1` | 19 | 3,857 | 57 | Service-1 (largest). |
| `northena` | 8 | 1,223 | 36 | Northena ledger writer. |
| `checker` | 6 | 751 | 8 | Checker. |
| `compliance` | 15 | 1,594 | 15 | Compliance. |
| `auth` | 15 | 1,714 | 45 | Auth kernel. |
| `master_admin` | 2 | 115 | 2 | Master admin. |
| `chat` | 2 | 99 | 4 | Chat surface. |
| `use_data` | 4 | 757 | 2 | Use-data path. |
| `census_engine` | 3 | 810 | 9 | Census engine. |
| `census_dimensions` | 3 | 371 | 6 | Census dimensions. |
| `opportunity_briefs` | 9 | 696 | 7 | Opportunity briefs. |
| `targeta` | 6 | 425 | 6 | Targeta. |
| `economics` | 8 | 827 | 13 | Economics. |
| `memory` | 11 | 1,429 | 11 | Memory. |
| `compute_seam` | 7 | 1,292 | 14 | Compute seam. |
| `compute_estate` | 3 | 227 | 3 | Compute estate. |
| `transform_forms` | 5 | 417 | 2 | Transform forms. |
| `layer_a` | 9 | 457 | 0 | Layer A (frontier, no invariant tests). |
| `layer_b` | 10 | 505 | 2 | Layer B. |
| `layer_c` | 3 | 227 | 2 | Layer C. |
| `g1_defensibility` | 9 | 599 | 0 | G-1 defensibility (frontier). |
| `v1_harness` | 3 | 223 | 0 | v1 harness. |
| `v2_gate` | 3 | 141 | 2 | v2 gate. |
| `v3_harness` | 2 | 138 | 0 | v3 harness. |
| `artifact_store` | 4 | 577 | 2 | Artifact store. |
| `team` | 2 | 202 | 0 | Team. |
| `multi_instance` | 3 | 190 | 0 | Multi-instance. |
| `health` | 2 | 91 | 11 | Health surface. |
| `skill_files` | 4 | 265 | 5 | Callable Skill Files. |

### C.10 Summary

- **84 service dirs on `programme/track-a`.** RMS-IQ-Core-2 has 34, Akki-OS-V1 has 36, Executive-Core has 17. Extraction-Akki carries roughly 2.4× the surface of the older `main`-branch cores.
- **~52 services (~62%) have ≥1 invariant-test hit** — substantive gated behaviour.
- **~14 services (~17%) have zero invariant-test hits** — frontier/thin/stub territory.

**`[framing, not canon]` verdict:** The platform substrate (W0+W1+W1b+W1c primitives · Registry · Solva/Solva-v2 · WPW Tier 1+2 · Watch scaffolding · Extraction+Training pipeline · Mtafiti · Northena · Shield-Train · Compute · Chokepoint · Governance-plane · IP-allowlist · Credentials-paste) is materially in place with real invariant coverage. **The DAP stack is the largest single unfilled area on the substrate.**

---

## D. DECISIONS / RULINGS STATE — what's ratified vs open

### D.1 From `RULING_LEDGER.md` (2026-09-09 · owner banked)

**RATIFIED (5) — binding immediately:**
1. Rules-Service **R-4** taxonomy — ratified as proposed.
2. **DAP R-1 controlled-unit definition — RATIFIED as proposed** (already used as settled throughout everything built since — see PHASE_C `[framing, not canon]` for the plan-linkage).
3. Agent-Containment **R-1** capability-ceiling list (four ceilings: no self-replication, no unauthorised resource acquisition, no unauthorised credential escalation, no self-access to oversight).
4. Rules-Service **R-3** witness — same witness the Watch already uses (C3).
5. Agent-Containment **R-2** scope-ratifying authority — Syni.ai for early deployments.

**DEFAULT-class, revisable (9) — wired tests-first at `backend/services/rulings/default_class_constants.py`:**
1. Rules-Service R-1 countdown — 48h system-ordinary / 7d system-TCB.
2. DAP R-4 API-key lifetime — 90-day rotation.
3. DAP R-5 AI-labs taxonomy — separate entry.
4. Security R-10 recommendation window — 24h.
5. Security R-8 — baseline-period approach.
6. Security R-9 — baseline-period approach.
7. Security R-11 — baseline-period approach.
8. Agent-Containment R-3 — baseline-period approach.
9. Pruning R-12 — re-derivation is default (recall requires owner sign-off).

**COUPLED (1) — must be ruled with companion:**
1. DAP **R-3 per-party ceilings** — MUST be ruled with Security **R-7** estate release budget.

**OPEN (4) — genuine owner decisions:**
1. **Security R-7 estate release budget number** — highest priority (gates DAP R-3, DAP-6, DAP §5).
2. **DAP R-6 pricing model** — commercial.
3. **WPW R-2** external-release signatory.
4. **DAP named approving authority** (person/role).

### D.2 From `Ratification_Record_v1.docx` (drop 2026-09-10 · 26 items across 6 sections)

Ratification-Record verbatim table structure verified (`docx` opened this session, 9 tables, 13 paragraphs):
- Section 1 · Document 0 — R-1 Resolved-by-use (TCB test), R-3 Resolved (Mkono in, Grey Mirror out), R-5 Resolved (dedicated per tenant).
- Section 2 · Rules Service — R-1 Recommended default (48h/7d), R-2 **Owner input** (second-signatory named role), R-3 Recommended default (reuse Watch witness), R-4 Recommended default (ratify v1 business-type taxonomy).
- Section 3 · DAP — R-1 Recommended default (already used as settled), **R-2 Owner input (approving authority named person)**, R-3 **Dependent** (allocation against R-7), R-4 Recommended default (90-day), R-5 Recommended default (AI-labs entry), **R-6 Owner input (pricing model)**.
- Section 4 · Security Amendments — **R-7 Owner input · highest priority**, R-8 Recommended default (baseline-period), R-9 Recommended default (baseline-period), R-10 Recommended default (24h), R-11 Recommended default (baseline-period).
- Section 5 · Pruning & Unlearning — R-12 Recommended default (re-derivation).
- Section 6 · Agent Containment — R-1 Recommended default (ratify AC-1 list), R-2 Recommended default (Syni.ai), R-3 Recommended default (baseline-period).

**Dependency order** (Ratification-Record Table 7): (a) Security R-7 gates DAP R-3; (b) Doc-0 R-1/R-3/R-5 already resolved by later documents (sign-off only, listed for completeness).

**Sign-off (Table 8) — none of the 6 sections has been dated/signed.** Owner has neither confirmed the recommended defaults en masse via section sign-off, nor filled in the 6 owner-input rows.

**Reconciliation with RULING_LEDGER:** the 2026-09-08 DECISIONS entry ratified 5 items and defaulted 9 items, but the Ratification-Record (dated 2026-09-09) lists **6 owner-input rows** (2 in RULING_LEDGER's 4-OPEN vs 4 in the Ledger's OPEN). Discrepancy:
- Ratification-Record owner-input rows: RS-R-2 (rules second signatory), DAP-R-2 (approving authority named person), DAP-R-6 (pricing), Sec-R-7 (release budget), plus Ledger-tracked WPW-R-2 signatory + DAP named approving authority = 4 in Ledger.
- **RS-R-2 (rules-second-signatory named role) is present in Ratification-Record but not tracked in RULING_LEDGER's 4-OPEN.** `[framing, not canon]` — this is a book-keeping gap; owner sign-off may implicitly cover it since RULING_LEDGER was created 2026-09-09 same day as the Ratification-Record but only tracks 4 OPEN items.

### D.3 From `NON_CLAIMS_REGISTER.md` (2026-09-09)

**5 explicit non-claims** (`LIM-1..5`) from `agent_containment_spec_v1` §5 — deliberately NOT counted in requirement rollups. Downstream code MUST NOT read these as met requirements.

### D.4 In-progress owner rulings (from DECISIONS.md tail)

- **ROC-1 (rule_criteria_spec_v1 framework)** — RATIFIED 2026-09-09T~11:40Z as `BANKED-DERIVED` from `System_Rules_Registry` + `Master_Requirements_Registry` rows 322-332 + eight-way citation trail. Rules Service unblocked to that extent.
- **BUILD GO · CP0.a → W0** — RATIFIED 2026-09-13T~05:15Z.
- **W1 CP-breakdown** — RATIFIED 2026-09-13T~06:07Z (kind_registry OPEN registry-backed; runtime-supervisor HALT verdict; zero-influence).
- **W1b charter** — RATIFIED 2026-09-13T~07:15Z.
- **W1c integration-proof charter** — RATIFIED 2026-09-13T~08:15Z (hand-banked trace, zero-domain, zero-NAS, zero real dispatch).
- **W-REGISTRY-EXTENSION-G3 label** — ruled 2026-09-13 (name distinct from prior W-REGISTRY-FULL-BUILD 2026-09-09 wave).
- **W-SOLVA-V2-LIFT standalone** — ruled 2026-09-13 (NOT a sub-component of Registry or DAP).
- **DPO-S2 HALT (reflection contract)** — open owner ruling; `engines/reflection.py` remains raising `NotImplementedError` until ratified. 3-5 candidates drafted at `notes/DPO_S2_REFLECTION_CANDIDATES_20260913.md`.

### D.5 Summary

| Bucket | Count | Notes |
|---|--:|---|
| RATIFIED (bindings live in code + tests) | 5 (Ledger) / 5 (Ratif-Rec Resolved) | Plus ROC-1, W0/W1/W1b/W1c/G-3/Solva-V2 charter rulings |
| DEFAULT wired (revisable) | 9 (Ledger) / 12 (Ratif-Rec recommended) | Owner en-masse-ratify by section sign-off would flip these to RATIFIED |
| Section sign-offs pending | 6 | All six sections of Ratification-Record un-signed |
| COUPLED (blocks companion) | 1 | DAP R-3 vs Security R-7 |
| **GENUINELY OPEN (owner-reserved)** | **4 in Ledger · 6 in Ratif-Rec** | **These are the actual next-turn owner decisions** |
| DPO-S2 (reflection HALT) | 1 | Semantic engine gap · candidates ready |

**Owner-critical gates for the DAP stack:** Security R-7 → DAP R-3 → DAP-6 (per-party ceilings + cumulative disclosure budget). Without R-7, DAP-STACK sub-waves that touch R-3 / R-6 / DAP-6 cannot close as production-grade; they can, however, land as tests-first mechanism with the R-7 value read from a `DEFAULT-PENDING-OVERRIDE` constant.

---

## E. INTENDED-WORK LEVERAGE MAP — the heart of the concern

For each intended item: **status** (DONE / PARTIAL / SCAFFOLDED-UNBANKED / NOT-STARTED) · **evidence on disk** · **what remains** · **leverage risk** (what could be redundantly rebuilt · what can be leveraged now).

### E.1 W-REGISTRY-FULL-BUILD CP10 · DOM Chromium proof

- **Status: SCAFFOLDED-UNBANKED (long-standing).**
- **Evidence:** `backend/tests/invariants/test_w_registry_full_build_cp10_wave_close.py` present in `git status --porcelain` output as `??` (untracked). PINS.md §"CP10 wave-close test file … remains shelved-untracked in working tree pending owner lift of the Registry-CP10 HOLD" (long-standing). W-REGISTRY-FULL-BUILD closed CP1..CP9 at ratchet 3098 (entries 55-59). W-REGISTRY-EXTENSION-G3 (later, at 3531) explicitly did NOT touch CP10.
- **What remains:** real-Chromium DOM proof invariant + wave-close manifest.
- **Leverage risk:** LOW — the wave-close test is already drafted; only owner-HOLD lift is required to open. Do NOT scaffold anew.

### E.2 W-DAP-STACK 2A..2H · DAP-1..30

- **Status: SCAFFOLDED-UNBANKED (partial · 2A only).**
- **Evidence:**
  - `backend/contracts/dap.py` (288 lines) — untracked.
  - `backend/services/dap/admission.py` (101 lines) — untracked.
  - `backend/tests/invariants/test_wdap_2a_external_party_principal_and_admission.py` (174 lines) — untracked.
  - No mechanical-RED receipt banked (checked `phase0/drill_receipts/` most recent — the last DAP-related receipt is a Solva/Registry receipt · latest wdap RED absent).
  - Rulings wired: R-1 controlled-unit (RATIFIED), R-4 90-day rotation (DEFAULT), R-5 AI-labs entry (DEFAULT) at `services/rulings/default_class_constants.py`.
  - Spec on disk: `canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx` (21,346 B) + `.../extracted/text/DAP_Backend_Spec_v1.txt`.
  - Plan on disk: `notes/PHASE_C_SYSTEMATIC_BUILD_PLAN.md` §W-DAP-STACK carries the DAP-1..30 sub-wave lineup with R-C1 (Rules-Service fallback) and R-C2 (reliable time source) markers explicitly enumerated.
- **What remains:** all 8 sub-waves (2A..2H). 2A scaffolding present but not RED-tested + not committed.
- **Leverage risk: HIGH.** If the scaffolding is re-scaffolded from scratch it wastes prior work. The correct move is: at Phase-2 open, mechanically-RED the existing files, iterate as needed per SO §3, close 2A with double-green, then continue 2B..2H per PHASE_C plan.
- **Owner gates required for full-grade close:** R-7 (blocks DAP-6 · sub-wave 2E-ish per PHASE_C), R-2 (approving authority · blocks DAP-11 approval routing), R-6 (pricing · blocks DAP-22 pricing/billing).

### E.3 W-SOLVA-V2-LIFT · reasoning component

- **Status: DONE at wave-grade (with declared DPO-S2 HALT).**
- **Evidence:**
  - Track-a commit `7f6d235a` (2026-09-13T10:48Z) · ratchet 3562 (+31).
  - `backend/services/solva_v2/` on disk: assertion_boundary.py · critic_seam.py · intent_audit.py · reasoning_faculty.py · trace.py · engines/{candidate_generation,tension_detector,reflection}.
  - Seal: `phase0/output_verified_seals/solva_v2_lift.seal.txt`.
  - Close doc: `notes/W_SOLVA_V2_LIFT_close.md`.
  - DPO-S2 HALT: `engines/reflection.py::run()` raises `NotImplementedError` until owner ratifies reflection contract; 3-5 candidates in `notes/DPO_S2_REFLECTION_CANDIDATES_20260913.md`.
- **What remains:** owner ratification of one of the DPO-S2 candidates, then land the reflection mechanism as a follow-on close (single CP, expected small delta).
- **Leverage risk: MEDIUM.** The `solva/reasoning.py` (700 LOC, 2026-08-25) is the pre-lift original; **BUILD_STATUS_PERCENT-20260909 §2 row 2 estimated Solva at ~7% and called for a 24,595-LOC XL lift of the donor pool from Executive-Core**. The Solva-V2-Lift wave at 3562 is a **case-agnostic reasoning-faculty seam-and-boundary lift**, not the full 24,595-LOC donor lift. `[framing, not canon]` — the two are compatible but distinct scopes; owner should confirm whether "Solva-V2-Lift" as closed IS the full Solva scope, or whether a further "W-SOLVA-DONOR-FULL-LIFT" wave remains.

### E.4 W-JOURNEY-ASSISTANT

- **Status: NOT-STARTED as a build wave; AUDITED at read-only grade.**
- **Evidence:**
  - `notes/JOURNEY_AND_ASSISTANT_AUDIT_20260913.md` (14,216 B · 2026-09-13) — interim canon-grounded audit answering the owner's guided-collaboration question. Verdict: guided-collaboration is canon-intended for Setup / Commission / DAP-assistance, but NOT for Whitepaper Wizard (invariant: not-influence) and NOT for Agent-Deploy Wizard (underspecified).
  - The wave is a **candidate**, not chartered — no grounding brief exists, no ratchet-history entry references it.
  - PHASE_C plan does NOT include W-JOURNEY-ASSISTANT in its named waves (§W-REGISTRY-EXTENSION-G3 / §W-DAP-STACK / §W-SOLVA-V2-LIFT).
- **What remains:** owner ruling on scope + charter + grounding brief. Not a build in itself; probably touches the wizard family + DAP-20 assistance-chat surface.
- **Leverage risk: LOW.** Do not build until chartered. If the owner wants to open this as a wave, `wizard/` (10 py / 1,258 LOC / 14 tests), `chat/` (2 py / 99 LOC / 4 tests), and the DAP-20-relevant surface would be the natural substrate.

### E.5 WPW Tier 1 + Tier 2

- **Status: DONE at wave-grade (both tiers).**
- **Evidence:**
  - Ratchet entries 34 (W-WPW-v1-c-close · Tier 1 lab notebook) and 35 (W-WPW-v1-d-close · Tier 2 technical report) — closed at 2717 and 2732.
  - Services on disk: `backend/services/wpw/{tier1_notebook.py, tier2_report.py}` + `backend/services/whitepapers/{draft.py, router.py}`.
  - Receipts: `phase0/wpw_notebook/` + `phase0/wpw_tier2_demo/` + `phase0/whitepapers/`.
- **What remains:** Tier 3 (external-release whitepaper) — BLOCKED on ruling #3 (R-2 external-release signatory) + ruling #6 (R1/R3 — see Doc-0/Watch cluster).
- **Leverage risk: LOW.** Tier 1+2 already in place. Do not rebuild.

### E.6 Rules Service stack

- **Status: PARTIAL — 3 of 4 rulings landed as ruling-constants; core mechanism NOT built.**
- **Evidence:**
  - `backend/services/rulings/default_class_constants.py` carries the ruling values (per RULING_LEDGER wired-at column).
  - `spec_id_index.json` shows `rule_criteria_spec_v1` is **BANKED-DERIVED** (ROC-1 ratification 2026-09-09T~11:40Z).
  - `System_Rules_Registry` has 286 rules INVENTORY but only 14 rules have Enforcement Class populated (BUILD_STATUS_PERCENT §2 row 4d — audit §D M-3 · G-4 gap 272 rules).
  - No dedicated Rules-Service wave has fired (no ratchet-history entry names it).
- **What remains:** four waves — W-RULE-REGISTRY-BOOTSTRAP · W-RULES-SERVICE-CEREMONY · W-RULE-BOOK-LIBRARY · W-286-RULE-ENUMERATION-CLASSIFY. Estimated XL total (BUILD_STATUS row 5).
- **Leverage risk: MEDIUM.** The RATIFIED (R-4 taxonomy) and DEFAULT (R-1 countdown) values are already binding. The Rules Service mechanism gates several Doc-0 attributes (Attr-4 controls · Attr-9 change-control ceremony) — see BUILD_STATUS §2 rows 4d, 4i.

### E.7 DOC-0 twelve-attribute gap-closure

- **Status: PARTIAL — ~20% average across 12 attributes (BUILD_STATUS_PERCENT §2 row 4).**
- **Attribute-by-attribute % (per BUILD_STATUS §2 rows 4a..4l):** Attr 1 TCB ~15% · Attr 2 Subsystem Decl ~10% · Attr 3 Governed Triad ~15% · Attr 4 Controls ~10% · Attr 5 Checkpoint ~30% · Attr 6 Reference Monitor ~5% · Attr 7 Baseline Ceremony ~40% · Attr 8 AU-3 ~25% · Attr 9 Change-Control ~15% · Attr 10 Determinism ~5% · Attr 11 Coherence ~5% · Attr 12 Governance Ceremony ~0%.
- **G-3 mechanical half CLOSED** via W-REGISTRY-EXTENSION-G3 (ratchet 3531, entry 72) — this covered asset-class schema, typed queryable custody class, class enumeration surface, four-class governance-value taxonomy, F&P Registry 11-field row, ledger-scoped visibility (WriteReceipt R-C2 marker).
- **Leverage risk: HIGH for Attr 4/9 (blocked on Rules Service — do not rebuild if Rules Service is where they land) · MEDIUM for Attr 10 (`determinism_inventory_v1` BANKED as spec, but no code path yet).**

### E.8 Watch (Doc-03 · 62 BUILD rows)

- **Status: SCAFFOLDING PRESENT · MECHANISM ~6% (BUILD_STATUS §2 row 8).**
- **Evidence:**
  - `backend/services/watch/` — 15 files, 2,787 LOC, 54 invariant-tests. Scaffolding present.
  - `phase0/watch_actions/`, `phase0/watch_marks/`, `phase0/mirages/`, `phase0/severances/`, `phase0/witness_attestations/` all thin (4-12 KB dirs) — Watch mechanism not yet exercised at scale.
- **What remains:** Wave C — bait mechanism · containment ladder · quarantine copies · external witness signing + tamper alarms · mirage planting / touch detection / severance · Doc03-078 Watch exemption.
- **Leverage risk: MEDIUM.** Watch primitives exist. Do not re-scaffold; iterate on the existing `services/watch/` files at Wave-C open.

### E.9 Agent Swarm Containment (12 AC rows)

- **Status: PARTIAL — 3 rulings wired (25% ceremony coverage · BUILD_STATUS §2 row 9). Zero code path yet against AC-1..AC-12 mechanisms.**
- **Evidence:** `RULING_LEDGER` RATIFIED entries 3 + 5, DEFAULT entry 8. `NON_CLAIMS_REGISTER.md` explicitly holds `LIM-1..5` as non-requirements.
- **Leverage risk: LOW.** Not likely to be redundantly rebuilt; simply not-yet-started.

### E.10 Audio / Media census

- **Status: SCOPED, NOT-STARTED.**
- **Evidence:**
  - `notes/W_AUDIO_POC_SCOPING_20260912.md` (40,584 B).
  - `notes/AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md` (102,393 B).
  - `notes/AUDIO_AUTONOMOUS_JOURNEY_CAPABILITY_ASSESSMENT.md` (74,550 B).
  - Source: `canon/w11_new_docs/audio_intel_plane_spec.docx` (26,623 B).
  - **BUILD_STATUS_PERCENT-20260909 does NOT include Audio as a component row** — Audio was scoped afterward. Audio-Census Addendum ruling banked 2026-09-12T~12:00Z (DECISIONS.md).
- **Leverage risk: LOW.** Fresh scope; scoping docs are the leverage. Not to be opened this phase.

### E.11 Mtafiti GPU Discovery — **DONE**

- **Status: DONE at wave-grade (CP1..CP7).**
- **Evidence:** entries 60-66 · ratchet 3251. `backend/services/mtafiti/` 28 files / 2,752 LOC / 41 invariant-tests. `phase0/mtafiti_gpu_discovery/` 17 MB of receipts.
- **Leverage risk: NONE.** Follow-on candidates (`W-MTAFITI-GPU-EMBEDDINGS`, `W-MTAFITI-DEEP-SWEEP`) are enumerated in NEXT.md but not chartered.

### E.12 Shield-Train pipeline — **DONE at build + admission + run grade**

- **Status: DONE across three linked waves (build + admission + run).**
- **Evidence:** entries 39, 42, 43 · ratchet 2836 → 2924. `services/shield_train/` 6 files / 1,120 LOC / 17 tests. `phase0/shield_train_receipts/` 70 MB.
- **Leverage risk: NONE.**

### E.13 Orchestrator resilience + window-fill guarantee — **DONE**

- **Status: DONE across r1/r1-wire/r2 + WINDOW-FILL-GUARANTEE + WINDOW-FILL-RESTORE-1/2.**
- **Evidence:** entries 36-38, 48, 49, 51 · ratchet reach 2748 → 3006. `services/orchestrator_resilience/` 6 files / 679 LOC / 11 tests.
- **Leverage risk: NONE.**

### E.14 Summary of leverage risks

| Item | Redundant-rebuild risk | Leverage lever |
|---|---|---|
| CP10 Registry-Full-Build proof | LOW | Test drafted · owner-HOLD lift required |
| DAP 2A scaffolding | **HIGH** | Existing untracked files; correct move = mechanical-RED at Phase-2 open |
| DAP 2B..2H sub-waves | HIGH | PHASE_C plan already sequences them; open in order; do not re-plan |
| Rules Service mechanism | MEDIUM | ROC-1 BANKED-DERIVED; 3 rulings wired; core waves not started |
| Watch Doc-03 62 BUILD rows | MEDIUM | Watch scaffolding exists; iterate, do not re-scaffold |
| DOC-0 Attr 4/9 gap-closure | HIGH | Rolled into Rules Service; do NOT open as independent waves |
| DOC-0 Attr 10 determinism | MEDIUM | `determinism_inventory_v1` BANKED as spec |
| Journey-Assistant candidate wave | LOW | Audit exists; not yet chartered |
| Audio POC | LOW | Fresh; scoping docs are the leverage |

**What has been at risk of being skipped or redundantly rebuilt (the owner's real question):**
1. **DAP 2A untracked scaffolding** — highest risk. If a next agent redoes 2A from scratch, ~5 hours of prior scaffolding is thrown away.
2. **CP10 Registry proof** — lower risk but the shelved test is a real asset.
3. **Rules Service scope creep** — Attr-4 / Attr-9 / rule-book-library gaps that belong in Rules Service could be opened as separate waves and duplicate effort.
4. **BUILD_STATUS_PERCENT-20260909 itself** — this doc *is* the master leverage map, dated 4 days before this session; if we don't cite it we redo the analysis.
5. **DPO-S2 reflection candidates** — already drafted; do not re-draft.

**What can be leveraged right now instead of built:**
1. **Solva-V2 · WPW Tier 1+2 · Registry-Full-Build CP1..CP9 · Registry-Extension-G3 · Mtafiti CP1..CP7 · Shield-Train build+admission+run · W0/W1/W1b/W1c platform substrate · Orchestrator-Resilience · Window-Fill · Multi-Table-Extract · SMS-Body-Emit · Campaign-Infra** — all DONE at wave grade; these are the fixed points the DAP + Rules-Service + Watch waves compose against.
2. **BUILD_STATUS_PERCENT_20260909.md** as the master % table (cite, don't redo).
3. **PHASE_C_SYSTEMATIC_BUILD_PLAN.md** as the DAP-stack + Registry-extension + Solva-v2 sequencing (already accounts for R-C1 / R-C2 markers).
4. **HOLISTIC_PLAN.md** (STATE) as the programme-wide plan.
5. **All 449 drill_receipts** as the mechanical-RED / double-green audit trail.

---

## F. CANON DELTA — un-extracted / stale requirements notes

### F.1 Un-extracted canon-family docs (from §3 of the STEP-0 report)

| Category | File | On-disk | Requirements-note? |
|---|---|---|---|
| w11 batch v3 | `AKKI_Canon_Documents_17_20_v3.docx` | ✅ | ❌ not extracted |
| w11 new | `canon_17_19.docx` | ✅ | ❌ not extracted |
| w11 new | `audio_intel_plane_spec.docx` | ✅ | Partial: `notes/AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md` (deep-extract, not a `canon_*_requirements.md`-schema file) |
| w11 new | `training_capacity.docx` | ✅ | ❌ not extracted |
| w11 new | `training_techniques.docx` | ✅ | ❌ not extracted |
| drop 09-09 | `DAP_Backend_Spec_v1.docx` | ✅ | ❌ not extracted (has extracted text at `.../extracted/text/DAP_Backend_Spec_v1.txt` but no `canon_*_requirements.md`) |
| drop 09-09 · files_14 | `TCB_Enumeration_v1.docx` | ✅ | ❌ spec_id_index shows `tcb_enumeration_v1` BANKED but no `canon_*_requirements.md` at row-level |
| drop 09-09 · files_14 | `Security_Architecture_Description_v1.docx` | ✅ | ❌ not extracted |
| drop 09-09 · files_14 | `Determinism_Inventory_v1.docx` | ✅ | ❌ spec BANKED per spec_id_index; no `canon_*_requirements.md` |
| drop 09-09 · files_14 | `Security_Function_Policies_v1.docx` | ✅ | ❌ not extracted |
| drop 09-09 · files_14 | `Failure_Posture_Enumeration_v1.docx` | ✅ | ❌ not extracted |
| drop 09-09 · files_14 | `Trust_Domain_Description_v1.docx` | ✅ | ❌ not extracted |
| drop 09-09 · files_14 | `Handoff_Generalisation_v1.docx` | ✅ | ❌ not extracted |
| drop 09-09 · files_14 | `Business_Continuity_Annex_v1.docx` | ✅ | ❌ not extracted |
| drop 09-09 · files_14 | `Pruning_Unlearning_Amendment_v1.docx` | ✅ | ❌ not extracted (though ruling R-12 landed; not the same as row extraction) |
| drop 09-09 · files_14 | `Akki_Governance_Architecture_v1.docx` (sha `b8af25f486` · 51,456 B) | ✅ | ❌ not extracted |
| drop 09-09 · files_14 | `Security_Assurance_Promise_Set.xlsx` | ✅ | ❌ not extracted |
| drop 09-10 | `Ratification_Record_v1.docx` | ✅ | Contents parsed into §D of this note; formal `_requirements.md` not written (this doc is a ratification-tracker, not requirements per se) |
| drop 09-10 · files_15 | `Master_Requirements_Registry.xlsx` | ✅ | Sheets: **Build Status** (56 rows), **System Rules Registry** (445 rows: Rule ID · Statement · Objective · Promise/Source Doc · Doc · Status …), **Objectives** (17 rows), **Legend** (15 rows). `notes/requirements_register_17docs.md` + `_20docs.md` may partially cover; needs reconciliation. |
| drop 09-10 · files_15 | `Akki_Governance_Architecture_v1.docx` **REVISED** (sha `b03932000c` · 51,587 B · 131-byte diff from files_14) | ✅ | ❌ not extracted, AND the earlier files_14 version wasn't extracted either |

### F.2 Stale-checks against revised source docs

- **`Akki_Governance_Architecture_v1.docx` was revised.** files_14 (sha `b8af25f486`, 51,456 B) → files_15 (sha `b03932000c`, 51,587 B, +131 bytes). Neither is extracted as `canon_*_requirements.md`. `spec_id_index.json` marks `akki_governance_architecture_v1` as BANKED, but the underlying doc was revised on 2026-09-09 between drops — any prior extraction against the files_14 version is potentially STALE with respect to the files_15 version.
- **`Master_Requirements_Registry.xlsx`** is the closest to a source-of-truth requirements corpus (445 rules · 17 objectives · 56 build-status rows). It has NOT been fully cross-walked into a `canon_*_requirements.md`. `notes/requirements_register_17docs.md` and `_20docs.md` (both 2026-08-27, pre-drop-09-10) MAY be stale against this xlsx.
- **`Pruning_Unlearning_Amendment_v1.docx`** — ruling R-12 landed; the doc itself has not been row-extracted. If the Pruning wave (BUILD_STATUS §2 row 7) opens, it will need the row extraction as its grounding brief.
- **`DAP_Backend_Spec_v1.docx`** — the definitive source for DAP-1..30 rows. Not extracted as `canon_*_requirements.md`. The `PHASE_C_SYSTEMATIC_BUILD_PLAN.md §W-DAP-STACK` names R-C1/R-C2 fallback markers but does not enumerate all 30 rows.

### F.3 Existing extractions likely still valid

- `canon_1..9_requirements.md` — sources byte-identical to Aug-14 zip contents · **valid**.
- `canon_addendum_1_requirements.md` — source unchanged since Aug-27 · **valid**.
- `canon_agent_containment_spec_v1_requirements.md` — source is `Agent_Swarm_Containment_Governance_Model_v1.docx` (sha `2824796d06` · 18,435 B), which has not been revised since drop 2026-09-10 · **valid**.

---

## G. UPDATED PLAN — sequenced true remaining scope, leveraging banked assets

### G.1 True in-flight next work order (post-3-waves-stale-marker reconciliation)

**`STATE/NEXT.md` top-marker reads W-MTAFITI-GPU-DISCOVERY / floor 3251.** The actual in-flight state per `baseline_failures.json` + track-a git log:

- **Floor**: 3562.
- **Last closed wave**: W-SOLVA-V2-LIFT (commit `7f6d235a` · 2026-09-13T10:48Z).
- **Backfill commit at HEAD**: `e2ae44b` (backfilled SHA into ratchet_history for both G-3 and Solva-V2-Lift).
- **Uncommitted / shelved**:
  - `backend/contracts/dap.py` · `backend/services/dap/` · `backend/tests/invariants/test_wdap_2a_external_party_principal_and_admission.py` — DAP 2A scaffolding (Phase-2 build artefact · untracked · **prior agent halted mid-flight before mechanical-RED**).
  - `backend/tests/invariants/test_w_registry_full_build_cp10_wave_close.py` — CP10 wave-close test on owner HOLD (long-standing).
- **Open owner-input rulings gating downstream work**: Security R-7, DAP R-2 (approving authority), DAP R-6 (pricing), WPW R-2 (external-release signatory), Rules-Service R-2 (second signatory named role · Ratif-Rec Section 2), DPO-S2 (reflection contract).

**True in-flight next work order:** DPO-S2 reflection ratification (small, unblocks Solva reflection landing) OR W-DAP-STACK 2A open (large, per PHASE_C plan) — dependent on owner's next sequencing ruling.

### G.2 Proposed sequence (leveraging, not rebuilding)

Applying the standing DEFAULT-PENDING-OVERRIDE answers from the prior STEP-0/STEP-1 message (Q1 delta-only extraction, Q2 supersession-form, Q3 exclude 5th repo, Q4 v6 prototype stays reference, Q5 defer NEXT.md/PINS.md refresh):

**Stage P1 — Canon delta extraction (Phase-1 · document-only · this session's remit if owner ratifies).**

Priority order (each row = one `notes/canon_<slug>_requirements.md` file at extraction grade, verbatim quotes, cited to §):

1. **`DAP_Backend_Spec_v1`** — DAP-1..DAP-30 rows. Directly gates W-DAP-STACK 2B..2H grounding briefs.
2. **`Akki_Governance_Architecture_v1` (files_15 REVISED, sha `b03932000c`)** — Doc-0 rows; delta-mark against files_14 (`b8af25f486`) if any content differs beyond the 131-byte tail. Gates every remaining DOC-0 attribute wave.
3. **`Pruning_Unlearning_Amendment_v1`** — rows for the Pruning wave (BUILD_STATUS row 7).
4. **`TCB_Enumeration_v1`** — Doc-0 Attr-1 rows (spec BANKED but no row-level `canon_*_requirements.md`).
5. **`Determinism_Inventory_v1`** — Doc-0 Attr-10 rows (spec BANKED · row-level absent).
6. **`Security_Architecture_Description_v1` + `Security_Function_Policies_v1` + `Failure_Posture_Enumeration_v1` + `Trust_Domain_Description_v1` + `Business_Continuity_Annex_v1` + `Handoff_Generalisation_v1`** — Watch/Doc-03 shared substrate; these gate Wave-C.
7. **`Master_Requirements_Registry.xlsx`** — cross-walk into `notes/master_requirements_registry_reconciled.md` (rules / objectives / build-status); sub-check stale-ness of `requirements_register_17docs.md` + `_20docs.md`.
8. **`AKKI_Canon_Documents_17_20_v3.docx`** + **`canon_17_19.docx`** — deltas over the core-9 (may be renumberings vs additions).
9. **`audio_intel_plane_spec` · `training_capacity` · `training_techniques`** — Audio POC substrate (deferred per NEXT.md's post-Audio-Census Addendum sequencing).
10. **`Ratification_Record_v1.docx`** — already parsed into §D of this note; formal write-out only if owner wants a durable ratification-tracker note.

**Stage P2 — Phase-2 wave-open discipline (post-Phase-1 · post-ratification).**

Sequenced (all use tests-first · BASELINE_GUARD=1 · mechanical-RED then double-green · two-commit local · never push):

1. **DPO-S2 reflection ratification (small, singleton close-CP)** — owner picks one of the drafted 3-5 candidates at `notes/DPO_S2_REFLECTION_CANDIDATES_20260913.md`; land the reflection mechanism; bump ratchet 3562 → +N.
2. **W-DAP-STACK 2A close** — mechanical-RED the existing three untracked files; iterate as needed; double-green; seal; ratchet-bump. **Do NOT rescaffold; leverage the working-tree scaffolding.**
3. **W-DAP-STACK 2B..2H sequential** — per PHASE_C §W-DAP-STACK plan (R-C1 fallback markers, R-C2 metering markers explicit; owner-open R-7/R-6/R-2 default-pending-override where required).
4. **W-REGISTRY-FULL-BUILD CP10 close** — if owner lifts HOLD; leverage the shelved close test (Registry has been extended via G-3 in the meantime · reconcile).
5. **W-RULES-SERVICE-STACK (four waves)** — W-RULE-REGISTRY-BOOTSTRAP · W-RULES-SERVICE-CEREMONY · W-RULE-BOOK-LIBRARY · W-286-RULE-ENUMERATION-CLASSIFY. Attr-4 and Attr-9 rolled into this; do NOT open them as independent waves.
6. **W-DOC0-ATTR1-TCB · W-DOC0-ATTR5 (rolled) · W-DOC0-ATTR6-REFERENCE-MONITOR · W-DOC0-ATTR7-BASELINE · W-DOC0-ATTR8-AUDIT-AU3 · W-DOC0-ATTR10-DETERMINISM · W-COHERENCE-BR-11** — Doc-0 attributes 1, 6, 7, 8, 10, 11 (in dependency order per BUILD_STATUS row 4). Attr-2, 3, 4, 9, 12 either rolled into Rules Service or downstream.
7. **W-WATCH-STACK (Wave C, 62 BUILD rows)** — bait · containment ladder · quarantine · witness · mirage · severance · Doc03-078 Watch exemption. Leverages existing `services/watch/` scaffolding.
8. **W-PRUNING-UNLEARNING** — retirement ceremony end-to-end (rulings landed; row extraction from step P1.3 needed first).
9. **W-AGENT-CONTAINMENT (AC-1..AC-12)** — mechanism build (3 rulings landed; row extraction from `canon_agent_containment_spec_v1_requirements.md` already valid).
10. **W-JOURNEY-ASSISTANT (candidate)** — awaits owner charter. Not-started.
11. **W-AUDIO-POC** — awaits owner Path A/B/C ruling on storage + NAS network path + 3-station confirm (W2 remains BLOCKED per DECISIONS 2026-09-13 W1c-close item 12).
12. **W-DATA-SUITE-v2-LIFT · W-TRUST-SURFACE-v2 · W-EXECUTIVE-SUITE-v2-LIFT** — surface migrations (BUILD_STATUS row 10).

### G.3 Explicit gates for Stage P2

Every P2 wave carries at least the following gates from §D:

- **DEFAULT-PENDING-OVERRIDE** for rows touching Security R-7 · DAP R-2 · DAP R-6 · WPW R-2 · Rules-Service R-2 — proceed with a stated default constant per SO §2, mark row `DEFAULT-PENDING-OVERRIDE`, revise on owner ruling in a single-commit flip.
- **R-C1 marker** (Rules Service not built): `custody_class_fallback = True` for controlled_determination_basis; flip-forbidden invariant per PHASE_C §W-DAP-STACK.
- **R-C2 marker** (reliable time source not built): `au_3b_defensible = False` for metered/timestamped rows; flip-forbidden invariant.
- **DPO-1 linkage** (per PHASE_C §W-DAP-STACK): controlled custody-class value maps to DAP R-1, not Document 4.
- **NON_CLAIMS_REGISTER `LIM-1..5`** rows never counted as met requirements.

### G.4 What this plan explicitly does NOT do

- Does not re-run Chunk-1 (SO §1 forbids it).
- Does not touch the three untracked DAP / Registry-CP10 working-tree files.
- Does not push (SO §3 · local commits only).
- Does not open W2 (audio · blocked).
- Does not open W-JOURNEY-ASSISTANT (needs owner charter).
- Does not refactor beyond thin-kernel discipline.
- Does not use `testing_agent` (SO §3 · terminal pytest only).
- Does not attempt egress (Radio T4 held).

### G.5 Book-keeping recommendation (deferred per Q5 DEFAULT-PENDING-OVERRIDE)

At the earliest Phase-2 wave open, refresh:
- `STATE/NEXT.md` `## Current step marker` block — write W-SOLVA-V2-LIFT close 3562 · then the wave being opened.
- `STATE/PINS.md` canon-pin block — expand from "Nine .docx documents" to acknowledge Addendum 1 · w11 batch · drop 09-09 · drop 09-10; hash-manifest per §3 of the STEP-0 report.

---

## HALT

Stopping here per owner instruction. No extraction, no build, no scaffolding.

**Deliverable:** `notes/LEVERAGE_AND_GAP_INVENTORY_20260913.md` (this file).

**Local commit:** to be recorded in the reply after this file lands.

**Awaiting:** owner ratification of the updated plan G — specifically the Stage-P1 canon-delta extraction order (§G.2 Stage P1) and Stage-P2 wave sequence (§G.2 Stage P2).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
