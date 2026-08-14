# Domain 5.6 — Governed Values and Ceremony

Scope (instruction §5.6): four value classes · entitlement as ABAC ·
change ceremony (propose, counter-sign, wait, apply, re-verify) ·
registries and their asymmetry · verification packs · regulator pack.

Spine cited: **Extraction-Akki** (≡ RMS-IQ-Core-2).

## Rows classified in this domain

### Four value classes / rule versioning

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C3-030** | Rulebook is compliance-owner authored, versioned, ceremony-changed | REUSE | `services/checker/{rule_change_request,state_machine,countersign_ledger,effective_delay,consequence_classes}.py`; tests `test_govern_g_g1_to_g_g8.py` (8 gates), `test_govern_ui1b_gates.py`, `test_govern_ui1b_iter15.py`, `test_govern_ui1b_iter16.py`, `live_preview/test_phase3_sc3_govern_live.py` |
| **C3-031** | One rule per row; id, statement, current setting, who set, when, ceremony version, count of automated checks enforcing | REUSE (contract) | `checker/rule_change_request.py`; the count of enforcing checks is derived — Chunk 4 to verify wiring |
| **C3-032** | A rule with zero automated checks = "rule on paper only"; not in force | PARTIAL | policy in place per governance close-reports; the surface flag for "rule on paper" per Canon 5 §23 is 5.7 BUILD |
| **C3-033** | Ceremony: proposed → counter-signed → waited → applied → re-verified | REUSE | full state machine + countersign_ledger; tests cover each transition |
| **C3-034** | While ceremony in countdown, affected ops HOLD if setting would be violated by pending version; countdown visible | REUSE | `checker/effective_delay.py` + Northena HOLD verdict wire (5.2 C3-013) |
| **C3-035** | Rulebook read-back with firing count + refusals produced | PARTIAL | data exists in ledger; the read-back surface is 5.7 |

### Countdown classes

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C3-052 · C3-053** | Three countdown classes (fast/standard/slow); Mkondo charter carries slowest | REUSE (backend) | `checker/consequence_classes.py` — enforce ruling `docs/close_reports/g3_operating_values_v1_1.md` SHA `0a91e1b4…` cited from `Akki-OS-V1/batch_quarantine.py`; `test_g3_op_values_v1_1_execution.py` |

### Verification runner + verification packs

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C3-039** | Verification Runner — plain-language test pack executor against LIVE system | PARTIAL | test packs run in test-time (`invariants/`, `registry/`); Canon-3 §31 the runner as a Compliance-Console-triggered live surface is BUILD |
| **C3-040** | Each pack demonstrates a rail firing with proof | REUSE | `test_p1_custody_closure.py` (six P1-G-R2 gates each demonstrates a rail firing with proof); `test_phase_5_stage_b_async_delivery.py`, `test_phase_6_stage_b_economics.py`, `test_phase_7_stage_b_{1,2,3}_wizard.py`, `test_phase_8_b_{1,2,5a,5b}*.py`, `test_phase_8_seam_3_sub_stage_{1,2,3}.py`, `test_phase_9_sub_stage_9_1_and_9_3.py` — a rich rail-firing test estate |
| **C3-041** | Standard packs: PII masked before model call; deletion needs 2 approvers; unanswerable refused with reason | REUSE (partial) | PII masking: shield custody chain covers; deletion 2-approver: `services/checker/countersign_ledger.py`; unanswerable refusal: refusal_family_classifier — three tests cover collectively |
| **C3-042** | Commissioning certificate signed based on packs firing | PARTIAL | ceremony framework exists; specific "commissioning certificate" artefact is 5.7 |

### Regulator pack

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C3-047 · C3-048** | Prove one run + regulator pack — compiled entirely from the record | **PARTIAL / BUILD** | trust receipts + ledger rows exist as ingredients; the export surface as a single-button action per Canon 5 §21 is BUILD |

### Registries + their asymmetry

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **Registry consolidation byte-identity** | Registry values byte-stable across consolidations | REUSE | `test_registry_v1_consolidation_byte_identity.py` |
| **Sensitivity classes / privacy floor** | Sensitivity classification asymmetry | REUSE | `services/compliance/{data_class_registry.v4.json,consequence_class.v0.json}` + `test_admission_refusal_v0_contract_frozen.py`; tests `test_license_class_config_governs_taxonomy.py`, `test_master_admin_tier_lock_path_a_ledger.py` |
| **Retention rulebook** | Retention rules with settings + last-set metadata | REUSE (partial) | `services/retention/*` + retention test above; the surface (Canon 5 §22) is 5.7 |
| **Feed / rights declarations** | Per-feed declaration baseline (Canon 4 §7 declaration layer — different from Canon 3 §6.1 actor declaration) | REUSE | `services/g1_defensibility/feed_declarations.seed.json` + `services/mtafiti/declaration.py` |

### Entitlement as ABAC

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **ABAC engine** | Attribute-based access control on estate operations | PARTIAL | `services/auth/{engineer_scope,session_binding,dependencies}.py` + `services/master_admin/*.py` — some ABAC surface; a first-class ABAC evaluator with policy version rows is BUILD |
| Retention rows in ledger | Deletion certificates | REUSE | `services/retention/authorized_deletion.py` + test |

### Setup + Day Zero + Working Rhythm (Canon 6)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C6-007 · C6-008 · C6-009 · C6-010 · C6-011 · C6-012** | Setup captures identity + compliance owner + six governed seam values + sources; permanent record; source connectors walked once each; setup ends with signed record | **PARTIAL / BUILD** | wizard + admission_handoff support the flow; Setup Console as a first-class named surface (5.7) is not fully present; the "signed setup record" artefact is BUILD |
| **C6-013 · C6-014 · C6-015 · C6-016 · C6-017 · C6-018 · C6-019 · C6-020 · C6-021 · C6-022** | Day Zero deliverables — estate map + commissioning certificate; Registry Dashboard populated; Verification Runner packs signed; Watch drills | PARTIAL | Registry Dashboard + wizard flows exist; the DAY-ZERO CEREMONY as a single narrative surface is BUILD; Watch drills entirely BUILD (5.8) |
| **C6-023–C6-028** | Exploration — browse registry; opportunity briefs; answer cards; entitlement refusal | PARTIAL | Opportunity Briefs `services/opportunity_briefs/*` + test `test_opportunity_briefs_ob_g1_to_g5.py`; Answer Card surface 5.7 |
| **C6-029–C6-033** | Objective Wizard 5-step commissioning + quote + acceptance = objective of record + operator approval | REUSE (backend) | wizard tests: `test_phase_7_stage_b_1_wizard.py`, `test_phase_7_stage_b_2_wizard.py`, `test_phase_7_stage_b_3_wizard.py` |
| **C6-034–C6-037** | Mining + delivery + shelf | REUSE (backend) | as above (5.4) |
| **C6-038–C6-043** | Ownership + integration + webhook + immediate observability | PARTIAL | engineer_key_grant + shield + memory; webhook is C7-009 BUILD |
| **C6-044 · C6-045** | Trust Center + Prove-one-run + Regulator pack | 5.7 mirror | see 5.7 |
| **C6-046–C6-054** | Watch Day journey | 5.8 mirror | BUILD |
| **C6-057–C6-060** | Loop discipline | REUSE-doctrine + 5.2 mirror | " |
| **C6-061 · C6-062** | Five things every journey rests on simultaneously | N/A-DOCTRINE | " |

## Doctrinal rows landed here for accountability

The following prose-only rows are logged here to prevent silent drop; they generate NO code obligation but govern classifications above:

- **C1-036 · C1-037** (Precedence) — N/A-DOCTRINE
- **C3-049 · C3-050 · C3-051** (Two authorities seam prose) — N/A-DOCTRINE
- **C3-054 · C3-055 · C3-056 · C3-057 · C3-058** (What governance does NOT do) — N/A-DOCTRINE
- **C4-051** (Loop self-limits) — N/A-DOCTRINE
- **C4-061 · C4-062 · C4-063 · C4-064** (What operating engines do NOT do) — N/A-DOCTRINE
- **C3-059 · C3-060 · C3-061** (Enforcement discipline as static analysis + runtime) — REUSE (build gates enumerated across the invariant suite)

## Domain 5.6 subtotals

- REUSE: 12 rows
- PARTIAL: 8
- BUILD: 3 (verification-runner-as-surface; regulator-pack export; setup/day-zero as named consoles)
- N/A-DOCTRINE: 12
