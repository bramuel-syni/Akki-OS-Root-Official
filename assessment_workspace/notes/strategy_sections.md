# strategy_sections.md — BUILD_STRATEGY level sections

Post-Part-2 sections per Orchestrator Ruling B: sequencing · transition windows (T1 = Ruling 1 gate) · no-regression contract · waste register · fidelity ledger freeze.

---

## §1 · Proposed sequence with dependency logic

**Not a schedule.** A dependency ordering — items whose predecessors are not landed cannot lawfully proceed. Sequencing is Owner territory; this is the logical earliest each item CAN start.

### 1.1 Dependency ordering (topological, coarse)

**Wave 0 — Foundational registers, must land before any authority-consuming work.**
- `WS-BUILD-MKONDO-CHARTER` — Mkondo is the register-of-registers.
- `WS-BUILD-RECORD-MATRIX` — defines every writer-role.
- `WS-BUILD-TASK-IDENTITY-REGISTER` — Canon 8 W11 substrate.
- `WS-WIRE-PARITY-EXTENSION` — every new contract lands only through this.
- `WS-BUILD-HANDOFF-REGISTRY` — six handoff shapes.

Rationale: Every subsequent item names one or more of these as a dependency. Land them first; land them once.

**Wave 1 — Ports and boundary.**
- `WS-BUILD-STREAMING-PORT` — anchors `WS-HARVEST-STREAMING`.
- `WS-BUILD-OBJECT-STORAGE-PORT` (FL-P1-03 pending owner ratification) — anchors work-studio migration.
- `WS-BUILD-INPUT-SEAT`, `WS-BUILD-INPUT-SEAT-DUAL`.
- `WS-WIRE-LEDGER-MATRIX` — anchors Northena in the matrix.
- `WS-WIRE-ADMISSION-HANDOFF` — registers existing admission handoff.

**Wave 2 — Governance and declaration.**
- `WS-BUILD-DECL` — declaration seat + check + supersession (Ruling-1 precondition a).
- `WS-WIRE-CUSTODY-DECL` — wires DECL into admit fail-closed.
- `WS-BUILD-RULEBOOK-SURFACE`, `WS-BUILD-CEREMONY-REVERIFY`, `WS-BUILD-VERIFICATION-RUNNER`.

**Wave 3 — Watch foundation and three actors.**
- `WS-BUILD-WATCH-FOUNDATION`.
- `WS-BUILD-WATCH-ACTORS`.
- `WS-BUILD-WATCH-RECORD-CLASSES`.
- `WS-BUILD-WATCH-MARK-REGISTRY`, `WS-BUILD-WATCH-SIGNATURE-STORE`, `WS-BUILD-WATCH-CONTAINMENT`, `WS-BUILD-WATCH-MIRAGE`, `WS-BUILD-WATCH-ATTESTATION-WITNESS`.
- `WS-BUILD-WATCH-AUTHORITY-PEERAGE`.
- `WS-BUILD-WATCH-RECONCILER` (Ruling-1 precondition b).
- `WS-BUILD-WATCH-DRILL-HARNESS`.
- `WS-BUILD-WATCH-TO-CIF`.
- `WS-BUILD-S6-WATCH-SERVICE`.

**Wave 4 — Extraction quality + CIF spine.**
- `WS-HARVEST-BATCH-QUARANTINE`, `WS-HARVEST-GAP-FILER`, `WS-HARVEST-REGISTRY-CONTEXT`, `WS-HARVEST-PARTITIONS`, `WS-HARVEST-SEQUENCING-HARNESS` (pending FL-P1-01), `WS-HARVEST-FAR-ENDPOINT`.
- `WS-BUILD-MOAC-SCORECARD`, `WS-BUILD-ADAPTER-REGISTRY`.
- `WS-CIF-COACH-SEAT`, `WS-CIF-ARCHIVE`, `WS-CIF-DETECTION`, `WS-CIF-METABOLISATION`, `WS-CIF-MONITORING`, `WS-CIF-PARAMETERS`.
- `WS-WIRE-SOLVA-CIF`.

**Wave 5 — Critic seam in-flight + Loop.**
- `WS-HARVEST-CRITIC-SEAM`.
- `WS-WIRE-CRITIC-INTO-ANSWERING`.
- `WS-WIRE-LOOP-ORCH`, `WS-WIRE-REGISTRY`, `WS-WIRE-INTENT-AUDIT-WATCH`, `WS-WIRE-WATCH-PLANE-ACTIVITY`.
- `WS-BUILD-INDEPENDENCE-GATE`, `WS-BUILD-STANDING-QUERY-SURFACE`.

**Wave 6 — RE-POINT + REBUILD.**
- `WS-HARVEST-STREAMING` (already Wave 1 — landing point for the port).
- `WS-HARVEST-TWO-PASS-AMENDMENT`.
- `WS-REPOINT-ANSWERING-SURFACES` (XL — the estate-wide adapter swap).
- `WS-REPOINT-SOLVA-V2`.
- `WS-REPOINT-SOLVA-VOICE-AUDIT` (path A or B pending FL-P1-02).
- `WS-REPOINT-WORK-STUDIO-LLM`.
- `WS-REBUILD-WORK-STUDIO-STORAGE` (XL — user-data migration; shadow-write phase then reader cutover; owner sign-off on the commissioning certificate).

**Wave 7 — Interface (harvest + tile-grid grammar).**
- `WS-HARVEST-SHELL-GRAMMAR` (donates the tile-grid).
- `WS-HARVEST-COMPONENT-LIBRARY`, `WS-HARVEST-CLASS-CHIP-LIBRARY`, `WS-HARVEST-REFUSAL-CARD`, `WS-HARVEST-DORMANT-STATE`.
- Console harvests: `WS-HARVEST-CONSOLE-EXTRACTION`, `WS-HARVEST-CONSOLE-COMPLIANCE`, `WS-HARVEST-CONSOLE-INTEGRATION`, `WS-HARVEST-CONSOLE-ADMINISTRATION`.
- Placement modifiers: `WS-MODIFY-PLANE-OBSERVABILITY`, `WS-MODIFY-PROVE-ONE-RUN-EXPORT`, `WS-MODIFY-AUDIT-TRAIL-PLACEMENT`, `WS-MODIFY-USE-DATA-PLACEMENT` (pending FL-P1-10), `WS-MODIFY-VERDICT-DEMO` (pending FL-P1-11).

**Wave 8 — Interface BUILD (no donor) + Watch Console.**
- `WS-BUILD-FIVE-PILLARS`, `WS-BUILD-CONTROL-BAND`.
- `WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE`, `WS-BUILD-BATCH-BOARD-SURFACE`, `WS-BUILD-QUALITY-OBSERVATION`.
- `WS-BUILD-REFUSAL-CARD-COPY`, `WS-WIRE-REFUSAL-FAMILY`, `WS-BUILD-AGENT-ASSUMED-CHIP`.
- `WS-BUILD-THREE-LENSES`, `WS-BUILD-ANSWER-CARD`.
- `WS-BUILD-REFERENCE-APP`.
- `WS-BUILD-PULSE-NEWS`, `WS-BUILD-STUDIO` (pending FL-OQ-05), `WS-BUILD-LEARN-PILLAR`.
- `WS-BUILD-CONSOLE-WATCH` (Instruction 02 exception — fourth tile-group, watch-officer gated).
- `WS-BUILD-SETUP-CONSOLE`, `WS-BUILD-DAY-ZERO`.

**Wave 9 — Governance ceremony completion + retirements.**
- `WS-BUILD-PROVE-ONE-RUN`, `WS-BUILD-DELIVERABLE-ATTESTATIONS` (Part 1).
- `WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL`, `WS-BUILD-READING-DISCIPLINE`.
- `WS-BUILD-WEBHOOK`, `WS-BUILD-PLANE-PRECOMPUTE`.
- `WS-BUILD-WATCH-DECISIONS-PANEL`, `WS-BUILD-WATCH-DAY` (Watch Console operational).
- `WS-RETIRE-APP-TERRITORY`, `WS-RETIRE-XCUT-SECURITY`, `WS-RETIRE-FRONTEND-ARCHIVES`, `WS-RETIRE-PROTOTYPE-DIVERGENCE`, `WS-RENAME-PROTOTYPE-TAXONOMY`.

**Wave 10 — Purpose-gate transition (T1 window).**
- Verify `WS-BUILD-DECL` and `WS-BUILD-WATCH-RECONCILER` both fire in drills (both attested in the ledger).
- On confirmation, `WS-CONTRADICTION-PURPOSE-GATE` strip proceeds via Canon 3 §24 rule-change ceremony (path FL-R1-01 pending owner ruling).

### 1.2 Guardrails on the sequence

- **No Wave-N item lands with an unlanded Wave-(N-1) dependency.** Enforced by the completeness audit script pre-submission.
- **XL items require review pack + one-paragraph defence.** Nine XL items: `WS-REPOINT-ANSWERING-SURFACES`, `WS-REBUILD-WORK-STUDIO-STORAGE`, `WS-BUILD-OBJECT-STORAGE-PORT`, `WS-BUILD-WATCH-FOUNDATION`, `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`. Each carries the defence in its Part-1 or Part-2 entry.
- **Reversal-cost gates.** Every VERY HIGH item requires an owner sign-off on the commissioning certificate before completing the reader-cutover.

---

## §2 · Transition windows

Transitions between old-and-new operating states of the estate. Named windows have named guards.

### 2.1 T1 — Purpose-gate transition (Ruling 1 gate)

**Window definition.** Between `WS-BUILD-DECL` demonstrated-firing AND `WS-CONTRADICTION-PURPOSE-GATE` strip ceremony completion.

**Guards (from Ruling 1 + `WS-CONTRADICTION-PURPOSE-GATE`):**
- G-T1-A: Executive-Core's `purpose_validator.validate_purpose()` gate STAYS in force. Refusals from it continue to write to the ledger.
- G-T1-B: `WS-BUILD-DECL` demonstrated-firing evidence is recorded in the ledger (a drill exports a declaration-refusal event).
- G-T1-C: `WS-BUILD-WATCH-RECONCILER` demonstrated-firing evidence is recorded in the ledger (a drill exports a governance×Watch reconciliation event).
- G-T1-D: A Canon 3 §24 rule-change ceremony executes the strip. Path (Canon-3 §24 ceremony OR Watch verdict) resolves per FL-R1-01 owner ruling.

**Prohibited during window:** any code deletion of the purpose gate. Any downstream service assuming the gate is stripped.

**Exit:** Strip event ledgered + parity-seat entries confirmed for both new contracts + Compliance Console read-back shows the gate stripped.

### 2.2 T2 — Executive-Core to application transition

**Window definition.** Between `WS-REPOINT-ANSWERING-SURFACES` start AND `WS-RETIRE-APP-TERRITORY` completion.

**Guards.**
- G-T2-A: Application-territory services (`services/cohort/`, `stripe_webhook.py`, etc.) run in parallel until adapter swap completes per surface.
- G-T2-B: Every RE-POINTed surface's adapter is atomic — no partial adapter states.
- G-T2-C: FL-OQ-10 owner ruling defines whether Executive-Core becomes an application, is archived, or is maintained parallel. Window cannot close without ruling.

**Prohibited during window:** any answer surface running on two adapters simultaneously.

**Exit:** All application-territory services either archived or moved to application layer; platform boundary contains none of the retired names (Canon 1 §12 audit).

### 2.3 T3 — Work-Studio storage migration

**Window definition.** Between `WS-BUILD-OBJECT-STORAGE-PORT` completion AND `WS-REBUILD-WORK-STUDIO-STORAGE` reader-cutover.

**Guards.**
- G-T3-A: Shadow-write phase — new writes go to BOTH mongo + plane; reads stay on mongo. Reversible.
- G-T3-B: Reader-cutover — reads move to plane. **Not reversible** for reads that landed during shadow-write against plane-only edits (see WS-REBUILD REVERSAL COST).
- G-T3-C: Owner sign-off on the commissioning certificate BEFORE reader-cutover. Certificate is the Canon 6 §11 shape.
- G-T3-D: Migration certificate lists every one of the 200+ exports with pre-and-post hash.

**Prohibited during window:** any user-visible loss of prior work.

**Exit:** Reader-cutover ledgered; commissioning certificate signed; all 200+ exports byte-identical pre-and-post.

### 2.4 T4 — Interface tile-grid landing

**Window definition.** Between `WS-HARVEST-SHELL-GRAMMAR` start AND `WS-BUILD-CONSOLE-WATCH` complete.

**Guards.**
- G-T4-A: Reference screenshot MUST have arrived in the workspace before any interface item lands rendering code. Fixture-pending on every interface item (FL-P1-14).
- G-T4-B: Watch Console NEVER nests under Trust Center at any point in the transition — placement invariant enforced by inventory audit.
- G-T4-C: Every retired prototype label (`WorkStudio`, `Trust Center`, `*Shield` naming) removed only after its replacement is live.

**Exit:** Nav audit confirms 100% Canon-5 conformance + Watch Console fourth-group present.

---

## §3 · No-regression contract

Every item's DoD depends on existing standing invariant tests continuing to hold, AND on new invariant tests landing before the item's completion. This section names both sets.

### 3.1 Existing standing invariant tests that MUST continue to hold (Extraction-Akki HEAD `b150c21`)

Cited from `Extraction-Akki/backend/tests/invariants/` (verified via direct `find`):

| Test file | Guards |
|---|---|
| `test_invariant_contract_snapshots.py` | Parity seat — freezes every listed contract shape. Extended by `WS-WIRE-PARITY-EXTENSION`. |
| `test_northena_ledger_row_v0.py` | Ledger row shape frozen. Guarded by `WS-WIRE-LEDGER-MATRIX`. |
| `test_admission_refusal_v0_contract_frozen.py` | Admission refusal shape frozen. Used by `WS-WIRE-CUSTODY-DECL`. |
| `test_ast_egress_gate.py` | Content-boundary AST gate. Model for new AST tests in `WS-WIRE-WATCH-PLANE-ACTIVITY`, `WS-WIRE-LEDGER-MATRIX`, `WS-BUILD-WATCH-SIGNATURE-STORE`, `WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL`. |
| `test_v0_paths_byte_identical_after_4a.py` | Loop replay byte-identical. Guards `WS-WIRE-LOOP-ORCH`. |
| `test_targeta_invariants.py` (mining_plan_contract, yield-layer permutation guard) | Loop invariants. Guards `WS-WIRE-LOOP-ORCH`. |
| `test_solva_assertion_boundary.py` (conclusion_class_signature, class_is_floor_over_load_bearing_all_fact) | Solva boundary. Guards `WS-WIRE-SOLVA-CIF`, `WS-REPOINT-SOLVA-V2`. |
| `test_govern_g_g1_to_g_g8.py` | Rule-change ceremony state-machine. Guards `WS-BUILD-CEREMONY-REVERIFY`. |
| `test_g_13_execution_atomic.py` | Governance-13 execution atomicity. Guards `WS-WIRE-REGISTRY`. |
| `test_partition_schema_v0_envelope.py` | Partition envelope shape. Guards `WS-HARVEST-PARTITIONS`. |
| `test_registry_context_block_golden_snapshot.py` | Registry context snapshot. Guards `WS-HARVEST-REGISTRY-CONTEXT`. |
| `test_generated_gates_regeneration_diff.py` | Gate regeneration byte-identical. Guards `WS-HARVEST-FAR-ENDPOINT`. |
| `test_critic_pass_execution_atomic.py` (in Akki-OS-V1) | Critic seam execution atomicity. Guards `WS-HARVEST-CRITIC-SEAM`. |
| `test_cif_manifest_submission_gate.py` (in Akki-OS-V1) | Manifest gate. Guards `WS-WIRE-CRITIC-INTO-ANSWERING`. |
| `test_memory_service_m_g1_to_m_g9.py` (spine) | Memory service invariants. Guards `WS-REBUILD-WORK-STUDIO-STORAGE`. |
| `gate1_class_inseparable.test.js` (frontend) | Class chip inseparable from claim. Guards `WS-HARVEST-CLASS-CHIP-LIBRARY`, `WS-BUILD-AGENT-ASSUMED-CHIP`. |
| `gate2_refusal_firstclass.test.js` | Refusal card first-class. Guards `WS-HARVEST-REFUSAL-CARD`, `WS-BUILD-REFUSAL-CARD-COPY`. |
| `test_auth_denied_notice_not_refusal_card.test.js` | Auth-denied ≠ refusal card. Guards `WS-HARVEST-REFUSAL-CARD`. |
| `test_shared_components_single_source.test.js` | Component library single-source. Guards `WS-HARVEST-COMPONENT-LIBRARY`. |

### 3.2 New standing invariant tests to write FIRST (before the item they gate lands)

| New test | Gates item(s) |
|---|---|
| `test_declaration_v0_contract_frozen.py` | `WS-BUILD-DECL` |
| `test_input_seat_envelope_v0_contract_frozen.py` | `WS-BUILD-INPUT-SEAT` |
| `test_input_seat_identity_one_per_task.py` | `WS-BUILD-INPUT-SEAT-DUAL` |
| `test_moac_scorecard_v0_contract_frozen.py` | `WS-BUILD-MOAC-SCORECARD` |
| `test_adapter_registration_v0.py` | `WS-BUILD-ADAPTER-REGISTRY` |
| `test_streaming_frame_v0_contract_frozen.py` | `WS-BUILD-STREAMING-PORT` |
| `test_object_storage_blob_v0_contract_frozen.py` | `WS-BUILD-OBJECT-STORAGE-PORT` |
| `test_webhook_envelope_v0.py` | `WS-BUILD-WEBHOOK` |
| `test_verification_pack_v0_contract_frozen.py` | `WS-BUILD-VERIFICATION-RUNNER` |
| `test_prove_one_run_pack_v0.py` | `WS-BUILD-PROVE-ONE-RUN` |
| `test_setup_record_v0_contract_frozen.py` | `WS-BUILD-SETUP-CONSOLE` |
| `test_commissioning_certificate_v0.py` | `WS-BUILD-DAY-ZERO` |
| `test_rulebook_rule_v0_contract_frozen.py` | `WS-BUILD-RULEBOOK-SURFACE` |
| `test_watch_verdict_v0.py`, `test_watch_action_v0.py`, `test_watch_attestation_v0.py` | `WS-BUILD-WATCH-ACTORS` |
| `test_watch_reconciliation_v0.py` | `WS-BUILD-WATCH-RECONCILER` (Ruling-1 firing evidence lives here) |
| `test_watch_mark_v0_contract_frozen.py` | `WS-BUILD-WATCH-MARK-REGISTRY` |
| `test_watch_containment_v0.py` + `test_watch_no_auto_extend.py` | `WS-BUILD-WATCH-CONTAINMENT` |
| `test_watch_mirage_no_render.py` (AST) | `WS-BUILD-WATCH-MIRAGE` |
| `test_watch_signature_no_reader.py` (AST) | `WS-BUILD-WATCH-SIGNATURE-STORE` |
| `test_watch_reserved_no_machine_execute.py` | `WS-BUILD-WATCH-DECISIONS-PANEL` |
| `test_watch_day_no_threshold_render.py` | `WS-BUILD-WATCH-DAY` |
| `test_watch_drill_receipt_v0.py` | `WS-BUILD-WATCH-DRILL-HARNESS` |
| `test_watch_disagreement_v0.py` | `WS-BUILD-WATCH-AUTHORITY-PEERAGE` |
| `test_record_matrix_writer_sole.py` (AST) | `WS-BUILD-RECORD-MATRIX` |
| `test_task_identity_one_per_call.py` (AST) | `WS-BUILD-TASK-IDENTITY-REGISTER` |
| `test_credential_scope_no_dual.py` (AST) | `WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL` |
| `test_handoff_contract_v0.py` | `WS-BUILD-HANDOFF-REGISTRY` |
| `test_coach_seat_single_origination_port.py` (AST) | `WS-CIF-COACH-SEAT` |
| `test_cif_archive_four_state.py` | `WS-CIF-ARCHIVE` |
| `test_cif_metabolisation_four_step.py` | `WS-CIF-METABOLISATION` |
| `test_watch_console_placement_not_trust_center.py` | `WS-BUILD-CONSOLE-WATCH` (Instruction 02 constraint) |
| `test_watch_console_four_tiles.py` | `WS-BUILD-CONSOLE-WATCH` |
| `test_five_pillars_router.py` | `WS-BUILD-FIVE-PILLARS` |
| `test_three_lenses_class_chip_present.py` | `WS-BUILD-THREE-LENSES` |
| `test_answer_card_v0.py` | `WS-BUILD-ANSWER-CARD` |
| `test_agent_assumed_chip_present.test.js` | `WS-BUILD-AGENT-ASSUMED-CHIP` |
| `test_ceremony_re_verified_state.py` | `WS-BUILD-CEREMONY-REVERIFY` |
| `test_independence_gate_v0.py` | `WS-BUILD-INDEPENDENCE-GATE` |
| `test_deliverable_attestation_v0.py` | `WS-BUILD-DELIVERABLE-ATTESTATIONS` |
| `test_standing_query_v0.py` | `WS-BUILD-STANDING-QUERY-SURFACE` |
| `test_work_studio_migration_byte_identical.py` | `WS-REBUILD-WORK-STUDIO-STORAGE` |
| `test_console_placement_uniqueness.py` | `WS-MODIFY-PLANE-OBSERVABILITY`, `WS-MODIFY-PROVE-ONE-RUN-EXPORT`, `WS-MODIFY-AUDIT-TRAIL-PLACEMENT` |

Every new test is a Canon-3 §31 verification-pack shape.

---

## §4 · Waste register

Things reversed, abandoned, or redundant in the strategy. Ledgered so the honest history persists.

| id | waste | reason | reversibility |
|---|---|---|---|
| W-01 | Chunk-1 §-anchor drift (72 rows) | Extraction script counted sub-paragraphs beyond heading boundaries. | REMEDIATED via Ruling A tools (`drift_map.py`, `drift_apply.py`, `drift_downstream.py`). Audit clean. |
| W-02 | 47 unassigned Canon-2 CIF rows in initial Chunk-3 domain tables | Domain-table drafting missed the CIF-specific rows. | REMEDIATED in `row_to_item_index.md` — CIF items WS-CIF-* opened. |
| W-03 | 4 folded WIRING items (critic-into-answering, parity-extension, refusal-family, ledger-matrix) | Folded silently under HARVEST/BUILD items. | REMEDIATED via Ruling 2 — promoted to standalone. |
| W-04 | 13 interface BUILD items folded before Instruction 02 | Chunk-3 defaulted interface to BUILD; Instruction 02 fixed Extraction-Akki as donor. | REMEDIATED via Ruling 3 — reclassified to HARVEST/MODIFY. |
| W-05 | Reference screenshot delay | Owner has not delivered the tile-grid-plus-detail-card grammar screenshot. | OPEN — interface items carry `FIXTURE PENDING` (FL-P1-14). |
| W-06 | FL-P1-05, FL-P1-06, FL-P1-07 — specific-file identification for three MODIFY items deferred | Focused reads not done in Part-1 drafting. | Requires re-read pass; substance-anchored citations hold. |
| W-07 | `WS-CIF-METABOLISATION`-style adopting frames vs Solva's parameterless assertion boundary | Potential seam conflict: CIF metabolisation claims frames adopted; Solva assertion boundary refuses caveated claims. | RESOLVED by design — CIF submits ratified frames back to Solva via `WS-WIRE-SOLVA-CIF`, no self-certification permitted (Canon 2 permanent bound). |
| W-08 | `AuthLoginPage.js`, `AuthRegisterPage.js` — application territory but present in Extraction-Akki frontend | Auth is application-layer per Canon 1 §13; drift into Extraction-Akki is a Canon-1 §12 breach. | REMEDIATED via Ruling 3 → folded into `WS-RETIRE-APP-TERRITORY`. |

---

## §5 · Fidelity ledger freeze note

At `BUILD_STRATEGY.md` assembly, `notes/fidelity_ledger.md` is FROZEN in its current form. Any new open question found after assembly requires a re-open through the same discipline (owner ruling + new entry).

**Frozen state at assembly:**
- Section A (8 owner open questions inherited): FL-OQ-03 through FL-OQ-10.
- Section B (7 Part-1 field-level entries): FL-P1-01 through FL-P1-07.
- Section C (12 Instruction-02 rendering decisions): FL-P1-08 through FL-P1-19.
- Section D (1 Ruling-1 leftover): FL-R1-01.
- Section E (citation-drift disclosure with full remediation trail): FL-P1-20 — retained per Orchestrator Ruling A (defect history part of the honest record).
- Section F (Part-2 field-level entries — appended during Part 2 drafting): FL-P1-03 upgraded with PROPOSAL (new engine BUILD, XL); FL-OQ-05 additional note re Studio scope XL reclass.

Total open items at freeze: **27** (8 + 7 + 12 + 1 + 1 disclosure + 0 net new from Part 2 that weren't already in Section B).
