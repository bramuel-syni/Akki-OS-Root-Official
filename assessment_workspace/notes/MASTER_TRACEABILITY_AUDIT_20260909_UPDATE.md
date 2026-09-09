# MASTER_TRACEABILITY_AUDIT_20260909_UPDATE.md — STEP 4 rebuild

**Wave:** W-AUDIT-REBUILD-STEP4 (owner directive 2026-09-08T~06:15Z STEP 4, executed straight-through under 2026-09-09T~11:40Z)
**Landed:** 2026-09-09
**Predecessor:** `notes/MASTER_TRACEABILITY_AUDIT_20260907.md` (2026-09-08T~04:40Z) + `notes/MASTER_TRACEABILITY_AUDIT_20260908_UPDATE.md`
**Ratchet floor at landing:** 3040
**Owner rulings governing this rebuild:** DECISIONS.md 2026-09-08T~06:15Z + 2026-09-09T~11:40Z
**Superseding index authority:** `notes/spec_id_index.json` (24 spec-IDs · 11 design-IDs · sha256-locked · frozen by `test_spec_id_tracking_index.py`).

---

## 1 · What this update changes vs the 2026-09-07 master audit

### A · Tracking scheme fixed (STEP 1 close)
- Master audit rows now index requirement-sources by **`{spec_id, filename, sha256}`** through `notes/spec_id_index.json`, not by prose description.
- Tracking invariant `test_spec_id_tracking_index.py` (9 tests) freezes:
  - every BANKED spec-ID has valid filename + matching sha256
  - every BANKED-DERIVED spec-ID names derivation sources on disk
  - every MISSING spec-ID has a zero-hit grep receipt
  - every design-ID (prototype/HTML) has valid filename + matching sha256
  - every docx opening signature appears in the index (closes false-missing at the source)
- Design-IDs added to same scheme (11 prototypes/HTML design drops indexed).

### B · 13th spec added (STEP 2 close)
- New spec: **`agent_containment_spec_v1`** (source: `Agent_Swarm_Containment_Governance_Model_v1.docx`, sha256 `2824796d06d7…`, drop 2026-09-10 files_15).
- **12 requirement rows** added under objective `O15 Agent & Swarm Containment` — AC-1..AC-12, all status `PROPOSED` (per source), with owner rulings applied via `default_class_constants.py`:
  - AC-1 four ceilings: **RATIFIED as proposed** (R-1)
  - AC-2 scope-ratifying authority: **RATIFIED = Syni.ai for early deployments** (R-2)
  - AC-5 sample rate + AC-2 window: **DEFAULT = baseline-period approach** (R-3)
- **5 non-claim rows** LIM-1..LIM-5 banked in `notes/NON_CLAIMS_REGISTER.md` — **NOT counted in the rollup denominator** per owner rule "so nobody later assumes condition 3 was solved".

### C · Missing list rebuilt (STEP 4 core)
Rebuilt against `spec_id_index.json`'s literal-search + docx-opening-signature ground truth.

| Prior state (2026-09-08 audit-update) | Rebuilt state (this update) | Delta |
|---|---|---|
| M-1..M-6 · `rule_criteria_spec_v1 §4/§6/§8` + `ROC-6/10/11` MISSING | BANKED-DERIVED via `System_Rules_Registry` + `Master_Requirements_Registry` + 8-way citations | 6 removed (owner ruling DEFAULT-PENDING-OVERRIDE ROC-1 · ratified 2026-09-09T~11:40Z) |
| M-8 · Doc 20 extraction MISSING | Doc 20 body extracted (see `canon/drops/20260909/extracted/doc20/`) | 1 partially resolved (still tracked as extraction charter) |
| M-17 · `dap_backend_spec_v1` MISSING | BANKED (drop 2026-09-09 raw + text) | 1 removed |
| — | New: 5 truly-missing IDs with zero-hit receipts: `cif_spec_v1` · `eab_tier1_adoption_spec_v1` · `extraction_derisking_spec_v1` · `training_techniques_spec_v1` · `transformation_quality_spec_v1` | +5 (all with receipts under `phase0/tracking_defect_20260908/grep_<id>.txt`) |

**Net missing count: 17 → 5.**

### D · Ruling ledger updated (STEP 3 close)
`notes/RULING_LEDGER.md` created with the 19-row status: **5 RATIFIED · 9 DEFAULT · 1 COUPLED · 4 OPEN**. DEFAULT-class values wired tests-first in `backend/services/rulings/default_class_constants.py` (frozen by 16 invariants).

---

## 2 · Rollup recount

### Denominator
- Prior classified rows: **1,159**
- New AC rows (agent_containment_spec_v1): **+12**
- LIM rows: **NOT counted** (NON-CLAIMS register)
- **New denominator: 1,171 classified rows** (excludes 286-row System Rules Registry inventory, 5 LIM non-claims, and 6,182-line BUILD_JOURNAL claims-to-verify per binding rules).

### Bucket recount (delta from 2026-09-07 audit)

| Bucket | 2026-09-07 count | 2026-09-09 count | Δ | Reason |
|---|--:|--:|--:|---|
| DONE | 89 | 89 | 0 | No new closes this wave (STEPS 1-4 are tracking + ingest, no product surfaces landed) |
| PARTIAL | 104 | 104 | 0 | Same |
| REUSE / REUSABLE | 482 | 482 | 0 | Same |
| BUILD / NEW | 484 | **496** | **+12** | 12 AC-* rows enter as new PROPOSED requirements |
| RETIRED | 0 | 0 | 0 | Same |
| **Total classified** | **1,159** | **1,171** | **+12** | |

### Bucket %s

| Bucket | 2026-09-07 % | 2026-09-09 % |
|---|--:|--:|
| DONE | 7.7% | 7.6% |
| PARTIAL | 9.0% | 8.9% |
| REUSE / REUSABLE | 41.6% | 41.2% |
| BUILD / NEW | 41.8% | 42.4% |
| RETIRED | 0.0% | 0.0% |

**Composite headline (DONE + PARTIAL + REUSE all forms):** 58.3% → 57.7% (arithmetic drift from +12 BUILD-class rows).

---

## 3 · Missing list (rebuilt · 5 rows)

| ID | Class | Citation count | Zero-hit receipt |
|---|---|--:|---|
| `cif_spec_v1` | standalone spec doc absent (CIF content in Canon 2 base canon) | 6 | `phase0/tracking_defect_20260908/grep_cif_spec_v1.txt` |
| `training_techniques_spec_v1` | standalone spec doc absent (adjacent file `canon/w11_new_docs/training_techniques.docx` has no opening signature) | 9 | `phase0/tracking_defect_20260908/grep_training_techniques_spec_v1.txt` |
| `eab_tier1_adoption_spec_v1` | standalone spec doc absent | 3 | `phase0/tracking_defect_20260908/grep_eab_tier1_adoption_spec_v1.txt` |
| `extraction_derisking_spec_v1` | standalone spec doc absent | 2 | `phase0/tracking_defect_20260908/grep_extraction_derisking_spec_v1.txt` |
| `transformation_quality_spec_v1` | standalone spec doc absent | 2 | `phase0/tracking_defect_20260908/grep_transformation_quality_spec_v1.txt` |

Every row above is enforced by `test_every_missing_spec_id_has_zero_hit_receipt_file` — the receipt file MUST exist and MUST name the spec-ID.

---

## 4 · Ruling ledger (5 · 9 · 1 · 4)

Reference: `notes/RULING_LEDGER.md` (verbatim owner text · DECISIONS.md 2026-09-08T~06:15Z).

- **5 RATIFIED:** Rules-Service R-3 R-4 · DAP R-1 · Agent-Containment R-1 R-2
- **9 DEFAULT (wired tests-first):** Rules-Service R-1 countdown 48h/7d · DAP R-4 90-day key rotation · DAP R-5 AI-labs taxonomy · Security R-10 24h window · Security R-8/R-9/R-11 baseline-period · Agent-Containment R-3 baseline-period · Pruning R-12 re-derivation
- **1 COUPLED:** DAP R-3 per-party ceilings (must rule with Security R-7 estate release budget)
- **4 OPEN:** Security R-7 budget number · DAP R-6 pricing · WPW R-2 signatory · DAP named authority

---

## 5 · Cross-links updated

| Artifact | Path | Frozen by |
|---|---|---|
| Spec-ID + design-ID index | `notes/spec_id_index.json` | `test_spec_id_tracking_index.py` (9 tests) |
| AC-1..AC-12 requirements | `notes/canon_agent_containment_spec_v1_requirements.md` | `test_agent_containment_spec_v1_ingest.py` (7 tests) |
| LIM-1..LIM-5 non-claims | `notes/NON_CLAIMS_REGISTER.md` | same 7 tests |
| Ruling ledger | `notes/RULING_LEDGER.md` | `test_default_class_ruled_constants.py` (16 tests) |
| Config constants | `backend/services/rulings/default_class_constants.py` | same 16 tests |

**Total wave invariants ratchet delta: +32** (9 spec-index + 7 ingest + 16 ruled-constants). Concurrent recovery +2 (harness refresh). Net ratchet **3006 → 3040** across two commits (`7f3c8cc` · `a5324dd` on `programme/track-a`).

---

## 6 · Discipline held

- Terminal `pytest` only (no `testing_agent`).
- Every wave landed via mechanical RED → GREEN → double-green byte-match under `BASELINE_GUARD=1`.
- Two-commit pattern: code + tests on `programme/track-a`; STATE + notes + receipts on workspace `master`. No push.
- Owner rulings banked verbatim in `STATE/DECISIONS.md` BEFORE action.
- STANDING_ORDERS §1 boot protocol observed. §2 mission-framed owner reports emitted at STEP-1 close and at this STEP-4 close.

---

## 7 · Next work order (STEP 5 · post-audit)

**W-REGISTRY-FULL-BUILD** commences from **clean floor 3040** (harness receipt fresh, 37 rules bound to rendered DOM, 0 orphans). Owner directive 2026-09-08T~06:15Z STEP 5 verbatim:

> THEN FIRE W-REGISTRY-FULL-BUILD. Standing ruling ("Priority building goes to registry. I need registry fully build") remains. Defaults stand: prototype v3 = binding design, Doc 0 v2 = binding. Build per D.1: 22 missing routes, substitution rules against v3 rendered DOM, mount opportunity_briefs + perception, 77 campaign runs visible, real-Chromium proof, floor 3006 (fix/refresh stale harness-receipt invariant first — refresh the harness, don't relax the threshold). Solva-v2 lift queues immediately behind.

- Binding design: `prototype_v3` at `canon/drops/20260909/raw/RMS_AI_Prototype_standalone_v3.html` (sha256 `ee6ebe77e1c5…`).
- Binding governance: `akki_governance_architecture_v1` (Doc 0 v2, drop 2026-09-09/2026-09-10).
- Substitution rules re-authored against v3 rendered DOM (rule-matches-nothing = RED).
- Registry: 22 missing routes · mount `opportunity_briefs` + `perception` · 77 campaign runs visible in models roster.
- Real-Chromium proof + full test discipline.

Solva-v2 lift queues behind (owner ruled 2026-09-06T~19:20Z).

---

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
