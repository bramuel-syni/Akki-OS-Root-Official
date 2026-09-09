# MASTER TRACEABILITY AUDIT — UPDATE · 2026-09-08T~06:00Z

**Parent:** `notes/MASTER_TRACEABILITY_AUDIT_20260907.md` (unchanged, remains authoritative for its rows).
**This update:** integrates the 2026-09-09 owner drop (4 artifacts) + closes 7 missing-reference items + adds ~50 new rows + updates rollup + adds DAP charter set.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.

---

## §A · 2026-09-09 drop artifacts (SHA256-banked)

Path: `canon/drops/20260909/raw/*` · sha256 sums at `canon/drops/20260909/sha256sums.txt`.

| Artifact | Bytes | Content · Closure |
|---|--:|---|
| `DAP_Backend_Spec_v1.docx` | 27,146 | DAP-1..DAP-30 requirements + 6 parked rulings · **CLOSES M-17** (`dap_backend_spec_v1` cited 6× by Trojan/Whisper) |
| `files_14.zip` | 87,335 | 11 files (10 .docx + 1 .xlsx). See §B below · closes M-7 + 7 Doc 0 gaps |
| `RMS_Data_Access_Portal_standalone.html` | 233,708 | DAP frontend prototype (pairs with backend spec) · **NEW SOURCE S29** |
| `RMS_AI_Prototype_standalone_v3.html` | 2,032,024 | v3 prototype · +77 KB vs v2 · surface-list byte-diff intact · content-equivalent at top level |

## §B · files_14.zip inventory (11 files)

Path: `canon/drops/20260909/extracted/files_14/` · text at `canon/drops/20260909/extracted/text/*.txt`.

| File | Lines | Anchor | Closes | Classification |
|---|--:|---|---|---|
| `Akki_Governance_Architecture_v1.docx` | 528 | **Doc 0 v2 supersession** of prior 244-line draft | M-8 vicinity (Doc 0 v1 → v2 refresh) | REUSE (supersedes prior doc0_governance_architecture.docx) |
| `Business_Continuity_Annex_v1.docx` | 29 | Business Continuity §3.7 annex | **CLOSES M-7** | REUSE |
| `DAP_Backend_Spec_v1.docx` (also in raw/) | 132 | 30 DAP requirements | **CLOSES M-17** | REUSE (charter W-DAP-BACKEND) |
| `Determinism_Inventory_v1.docx` | ~120 | Per-component deterministic/learned inventory | **CLOSES Doc 0 G-10** | REUSE (feeds W-DETERMINISM-BOUNDARY) |
| `Failure_Posture_Enumeration_v1.docx` | ~100 | Per-component failure-mode + posture enumeration | **CLOSES Doc 0 G-11** | REUSE |
| `Handoff_Generalisation_v1.docx` | ~150 | Mkondo handoff contract generalised to every subsystem | **CLOSES Doc 0 G-13 + CA1-009** | REUSE (feeds W-SUBSYSTEM-DECLARATION-ARCHITECTURE) |
| `Pruning_Unlearning_Amendment_v1.docx` | 172 | NEW amendment · pruning + machine-unlearning mechanism | **NEW canon amendment** (not previously in any register) | NEW rows to classify · charter W-PRUNING-UNLEARNING |
| `Security_Architecture_Description_v1.docx` | ~180 | ADV_ARC.1-shaped architecture description | **CLOSES Doc 0 G-6** | REUSE |
| `Security_Assurance_Promise_Set.xlsx` | 25+ rows | Refreshed Promise Set v2 (post-amendments) | Refresh of S16 (may include ratified S-22..S-25) | REUSE (refresh) |
| `Security_Function_Policies_v1.docx` | ~200 | Named SFPs over principal/asset/operation triad | **CLOSES Doc 0 G-7** | REUSE (feeds W-MANDATORY-BASELINE-CEREMONY) |
| `TCB_Enumeration_v1.docx` | ~90 | Named current TCB list per BA-1.3 | **CLOSES Doc 0 G-1** | REUSE (feeds W-TCB-ENUMERATION) |
| `Trust_Domain_Description_v1.docx` | ~120 | Trust-domain catalog per Att 12 BA-12.1..12.3 | **CLOSES Doc 0 G-12** | REUSE (feeds W-GOVERNANCE-CEREMONY-BR-12) |

**M-item closures from this drop: 7** (M-7, M-8-vicinity, M-17, + 7 Doc 0 gaps that were not on M-list but were G-list).

## §C · DAP Backend Spec — new source S29 · row-by-row

**30 requirements (DAP-1..DAP-30) + 6 parked rulings (R-1..R-6). All PROPOSED as authored, owner-ratification pending.**

Sourced from `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` §1-10.

| Row group | Rows | Purpose | Classification |
|---|--:|---|---|
| DAP-1..DAP-5 | 5 | External-party principal · governed triad extension · slow-play detection · trust-domain boundary | NEW (all 5) — external-party class NEW to Doc 0 Att 3 |
| DAP-6..DAP-11 | 6 | Six crossing profiles: Browse · Connected workspace · Extraction · Fine-tune · Trained weights egress · Raw download | REUSE 2 (DAP-8 Attribute 7 anchor · DAP-9 owner ruling 5-Sep) · NEW 4 |
| DAP-12..DAP-13 | 2 | Admission & API keys | NEW (governed admission workflow) |
| DAP-14..DAP-17 | 4 | Approval workflow · standing approvals | NEW · overlaps with Spend Requests (partial REUSE) |
| DAP-18..DAP-20 | 3 | Extraction commissioning · objective freeze · portal assistance chat | REUSE (Objective Wizard exists; portal-side chat NEW) |
| DAP-21..DAP-24 | 4 | Metering · receipts · terms · spend ceilings · cumulative extraction history | NEW (fresh pricing rails) |
| DAP-25..DAP-27 | 3 | Estate-owner configuration · default-unavailable · suspension | NEW |
| DAP-28..DAP-30 | 3 | Failure posture: fail-closed · unrecorded-extraction refusal · Browse-degrades | REUSE (fail-closed doctrine BR-1.5) · NEW 2 |
| R-1..R-6 | 6 | Parked owner rulings (controlled-unit definition, approving authority, TCB witness role, API-key lifetime, pricing tariff, spend requests overlap) | Rulings-parked · classification-blocked |

**S29 rollup (30 rows · exc. rulings):** DONE 0 · PARTIAL 0 · REUSE 4 · NEW 26 · **86.7% NEW.**

**Interpretation:** DAP is a fully-new subsystem. Every crossing profile (DAP-6..11) needs a wave. Pricing rails (DAP-21..24) are new. The **compute-to-data guarantee** (DAP-9, no exception clause) is the platform's sovereignty guarantee — the most critical row.

## §D · Doc 20 · Model Capability Register · new source S30

**14 rows A20.1..A20.14** extracted from `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.docx`. Owner-ruled: PROPOSED rows adopted as live PROPOSED-class config (not per-model ratification).

| Row group | Rows | Purpose | Classification |
|---|--:|---|---|
| A20.1-A20.2 | 2 | Text dimension — Qwen3/Llama · CANON, models_registry.v0.json | DONE |
| A20.3-A20.6 | 4 | Document/OCR — Qwen-VL, GOT-OCR2, PaddleOCR-VL, ColPali v1.3 | REUSE (license-verified external open models) |
| A20.7-A20.10 | 4 | Vision — Qwen2.5-VL-72B, InternVL3-78B, Llama 4 multimodal, Pixtral 12B | REUSE |
| A20.11 | 1 | Audio — deferred to Doc 17 §A17.10-A17.11 | CANON (reference) |
| A20.12-A20.14 | 3 | Resolution rule — deterministic dimension resolve · calibration-decides · no user-facing choice | NEW (compile-time resolution seam) |

**S30 rollup:** DONE 2 · REUSE 8 · NEW 3 · CANON-ref 1. **CLOSES M-8.**

## §E · Pruning/Unlearning Amendment · new source S31

172 lines · NEW canon amendment (not previously in any register). Introduces pruning + machine-unlearning mechanism. Row extraction deferred to a per-source detail file `s31_pruning_unlearning_amendment.md` (INVENTORY-class this pass).

**S31 rollup:** INVENTORY (row-by-row extraction deferred).

## §F · Refreshed Missing-Reference List

**Closed by this drop (7 items):**

| # | Reference | How closed |
|---|---|---|
| ~~M-7~~ | Business_Continuity_Requirements §3.7 annex | `Business_Continuity_Annex_v1.docx` banked |
| ~~M-8~~ | Doc 20 rows not extracted | Doc 20 extracted at `canon/drops/20260909/extracted/doc20/AKKI_Canon_17_20_v3_full.txt` · S30 above |
| ~~M-17~~ | `dap_backend_spec_v1` | `DAP_Backend_Spec_v1.docx` banked · S29 above |
| ~~G-1~~ | Doc 0 TCB enumeration | `TCB_Enumeration_v1.docx` banked |
| ~~G-6~~ | Doc 0 security architecture description | `Security_Architecture_Description_v1.docx` banked |
| ~~G-7~~ | Doc 0 named SFPs | `Security_Function_Policies_v1.docx` banked |
| ~~G-10~~ | Doc 0 determinism inventory | `Determinism_Inventory_v1.docx` banked |
| ~~G-11~~ | Doc 0 failure posture enumeration | `Failure_Posture_Enumeration_v1.docx` banked |
| ~~G-12~~ | Doc 0 trust domain description | `Trust_Domain_Description_v1.docx` banked |
| ~~G-13~~ | Mkondo handoff generalisation | `Handoff_Generalisation_v1.docx` banked |

**Remaining OPEN (10 items · from M-1..M-16 + M-17):**

| # | Reference | Status | Impact |
|---|---|---|---|
| **M-1** | `rule_criteria_spec_v1 §4` (rule ID naming) | ❌ Not on disk | Blocks Rules Service RBM-1 authoring |
| **M-2** | `rule_criteria_spec_v1 §6` (Registry append-only) | ❌ Not on disk | Blocks Rules Service RBM-12 amendment retention |
| **M-3** | `rule_criteria_spec_v1 §8` (enforcement class axis) | ❌ Not on disk | Blocks RBM-6 conflict check + Enforcement Class column population |
| **M-4** | `ROC-10` (registry field completeness) | ❌ Not on disk | Blocks RBM-18 registry authoritativeness |
| **M-5** | `ROC-11` (amendment retention) | ❌ Not on disk | Same as M-4 |
| **M-6** | `ROC-6` (prefix reservation) | ❌ Not on disk | Blocks RBM-3 |
| M-9 | External standards | ❌ (external) | Not required on disk |
| M-10 | External MITRE Engage / NIST SI-4 | ❌ (external) | Not required on disk |
| M-11 | External DP references | ❌ (external) | Not required on disk |
| **M-12** | Doc 3 Part D (Recovery & Notification) | ⚠ Structural gap | S-10, S-11 sit on Wave E rulings only |
| **M-13** | Rule Book Library FULL for 4 skeleton books | ⚠ Partial | RB-PDP + RB-AIG FULL; 4 others SKELETON |
| **M-14** | Addendum 2+ | ❌ Not on disk | Owner-side authoring not yet started |
| **M-15** | Doc 10 standalone | ⚠ Naming clarified | Not a real file — projection of umbrella 9 + Addendum |
| **M-16** | WPW Tier 3 rulings R1/R2/R3 | ⚠ Owner-parked | Blocks WPW-13..18 |

**M-count trend:** 17 → **10 open** (7 closed · 41% closure rate this drop). The 6 remaining critical items (M-1..M-6) all trace to a single missing document: `rule_criteria_spec_v1`. **One artifact drop closes 6 M-items.**

## §G · Refreshed rollup (denominator 1,192 non-INVENTORY rows)

Adds S29 (30 DAP) + S30 (14 Doc 20) + Doc 0 gap closures (7 Doc 0 gaps flip from NEW to REUSE per closure evidence) = **+44 net rows, +7 NEW→REUSE flips**.

| Bucket | Prior (§C.4) | Δ this drop | New total | % of 1,192 |
|---|--:|--:|--:|---:|
| DONE | 89 | +2 (Doc 20 A20.1-2 CANON already in models_registry.v0.json) | **91** | 7.6% |
| PARTIAL | 104 | 0 | **104** | 8.7% |
| REUSE | 482 | +7 (Doc 0 G-list closures flip) + 12 (Doc 20 A20.3-10, A20.11) + 4 (DAP-6..11 anchors) = +23 | **505** | 42.4% |
| BUILD/NEW | 484 | +26 (DAP-1..DAP-30 net NEW) + 3 (Doc 20 A20.12-14) − 7 (Doc 0 G-flips) = +22 | **506** | 42.4% |
| RETIRED | 0 | 0 | **0** | 0.0% |
| **Total non-INVENTORY** | **1,159** | **+33** | **1,192** | — |

**Interpretation:** 
- **DONE + PARTIAL now = 16.3%** (up from 16.7% — flat because the drop is spec-material, not implemented code).
- **REUSE now = 42.4%** (up from 41.6% — Doc 0 gaps flip from unavailable-to-implement to available-to-implement).
- **NEW still = 42.4%** — DAP adds 26 NEW rows, offset by Doc 0 gap closures flipping to REUSE.

**Net effect of this drop:** the platform's requirement base grew by ~3% (33 rows), but the WAVE-BLOCKING dependency count dropped by 41% (7 of 17 M-items closed). This is progress on the **path to build**, not on **build itself** — the drop is fuel, not building.

## §H · New wave charters (E.8 stack)

Additive to sprint roadmap §E in parent audit.

### E.8 · DAP stack (S29 · 30 rows · all-NEW subsystem)

| Item | REQ-IDs | Outcome | Pass criteria | Effort class |
|---|---|---|---|---|
| **W-DAP-EXTERNAL-PARTY-PRINCIPAL** | DAP-1..DAP-5 | External party admitted as organisation-level principal with slow-play detection + trust-domain boundary | Principal-class enumerable · agent principal distinct · slow-play attack shape wired · trust-domain identifier resolution refused across boundary | L |
| **W-DAP-CROSSING-PROFILES-6** | DAP-6..DAP-11 | Six named crossings implemented per §4 table (Browse · Connected · Extract · Fine-tune · Egress · Raw) | Each crossing wired to its named engine (Mtafiti/Solva/Perception/Targeta/Registry/OuterGate); DAP holds no logic of its own · DAP-9 no-exception compute-to-data enforced structurally | XL |
| **W-DAP-ADMISSION-KEYS** | DAP-12..DAP-13 · R-4 | Party admission ceremony · per-principal API keys with revocability + lifetime | Owner-authority admission gate green · key revocation atomic · key material never in receipts · R-4 lifetime default (DEFAULT-PENDING-OVERRIDE) | M |
| **W-DAP-APPROVAL-WORKFLOW** | DAP-14..DAP-17 · R-2 · R-6 | Approval routing for controlled requests + fine-tune + skill-dev + standing approvals | Approval decisions recorded with identity + reason · silence never inferred as approval · fine-tune always requires approval · standing approvals revocable in one act | L |
| **W-DAP-EXTRACTION-COMMISSION** | DAP-18..DAP-20 | Extraction jobs commissioned with frozen objective; DAP composes engines | Objective freeze at commission · widening = new job · assistance chat proposes but never decides | M (extends Objective Wizard) |
| **W-DAP-METERING-RECEIPTS** | DAP-21..DAP-24 · R-6 | Metered events per operation with terms + cumulative extraction history | AU-3 six elements per event · terms resolution most-specific-first · spend ceiling routing · cumulative history query-able · pricing rails ready (R-6 tariff pending) | L |
| **W-DAP-OWNER-CONFIG** | DAP-25..DAP-27 · R-1 · R-2 | Estate-owner config surface: per-class availability · default-unavailable · suspension | Default-unavailable invariant green · suspension immediate + records in-flight jobs as stopped · R-1 controlled-unit definition pending | M |
| **W-DAP-FAILURE-POSTURE** | DAP-28..DAP-30 | Fail-closed on every gate; unrecorded extraction never permitted; Browse degrades not refuses | All gates fail-closed invariant · metering write refusal = operation refusal · Browse marks stale time · fail-safe-open only on Browse | S |
| **W-DAP-PORTAL-FRONTEND** | S29 UI (RMS Data Access Portal standalone) | External-party facing portal · owner-side config panels · assistance chat integration | Substitution rules against rendered DOM · 6 crossing profile UI paths green · portal-swap chrome · owner-config wired | L |

**E.8 total: 9 wave charters · DAP is XL+L+M×4+S — roughly 2-3 sprints of foundation work.**

### E.9 · Doc 0 gap-closure waves (REUSE-friendly · unblocks E.4)

Every Doc 0 G-item now has a REUSE spec:

| Item | Was BLOCKED on | Now REUSES from | Effort class |
|---|---|---|---|
| W-TCB-ENUMERATION (E.4) | G-1 (missing) | `TCB_Enumeration_v1.docx` | M → **S** (spec drives implementation directly) |
| W-REFERENCE-MONITOR-DISCIPLINE (E.4) | G-6 | `Security_Architecture_Description_v1.docx` | L → **M** |
| W-MANDATORY-BASELINE-CEREMONY (E.4) | G-7 | `Security_Function_Policies_v1.docx` | M → **S** |
| W-DETERMINISM-BOUNDARY (E.4) | G-10 | `Determinism_Inventory_v1.docx` | XL → **L** |
| W-COHERENCE-BR-11 (E.4) | G-11 (via Failure Posture) | `Failure_Posture_Enumeration_v1.docx` | M → **S** |
| W-GOVERNANCE-CEREMONY-BR-12 (E.4) | G-12 | `Trust_Domain_Description_v1.docx` | L → **M** |
| W-SUBSYSTEM-DECLARATION-ARCHITECTURE (E.4) | (adjacent G-13) | `Handoff_Generalisation_v1.docx` | L → **M** |

**Net effect: E.4 stack effort reduces from XL+L×3+M+S+L to L+M×3+S×2 (~40% smaller).**

### E.10 · New standalone (S31 Pruning/Unlearning)

| Item | REQ-IDs | Outcome | Effort |
|---|---|---|---|
| **W-PRUNING-UNLEARNING** | S31 rows (deferred inventory) | Model pruning + machine-unlearning mechanism · per-run · per-tenant | XL (design-heavy · new class of operation) |

## §I · Prototype v3 vs v2 diff

**Byte size:** v2 1,954,907 · v3 2,032,024 (+77,117 = +4%).
**Top-level surface signatures:** identical count for Confidential Information Register (4), Rules Updates (15), Board 360 (3), Exco 360 (3).
**Substitution-rule anchors:** unchanged (37 per_rule entries in banked harness ground truth).
**Byte-diff:** internal to embedded blobs (framework bundles content-equivalent; app-payload delta unknown without deeper diff).

**Ruling required (`DEFAULT-PENDING-OVERRIDE`):** does v3 supersede v2 as the binding design source?
- **Default applied:** **v3 supersedes v2** effective 2026-09-09 (owner's latest drop governs per standing pattern). v2 remains banked as historical reference.
- **Owner may override** to (a) keep v2 as authoritative and treat v3 as "not-yet-adopted" or (b) accept v3 as binding with a mandatory re-run of the substitution-rule authoring against v3's rendered DOM.

## §J · S29 · RMS Data Access Portal · HTML surface inventory (deferred to detail file)

Byte-banked at `canon/drops/20260909/raw/RMS_Data_Access_Portal_standalone.html` (233,708 bytes). Row-shaped surface inventory to be produced in `s29_dap_portal_surfaces.md` follow-on (mirrors SURFACE_AUDIT_v2 method). Rough visible surfaces: external-party portal · owner-config panels · admission ceremony surface · six crossing profile flows · metering/receipts view · cumulative extraction history · spend requests interlink · assistance chat · approval queue. **Estimated: 25-40 surfaces.**

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
