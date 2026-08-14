# Domain 5.4 — Extraction and Quality

Scope (instruction §5.4): five-ring unit · qualification partitions ·
batching and holds · model ladder + registry · MOAC's six criteria ·
quality matrix · three production quality tiers.

## Rows classified in this domain

### Five-ring unit + qualification partitions

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **five-ring unit** | The Ring / DefensibilityClass typed unit that flows through the platform | REUSE | `Extraction-Akki backend/contracts/five_rings.py:1-300+`; `NormalizedUnit` shape; `test_layer_a_handlers.py`, `test_layer_b_providers.py`, `test_layer_c_aggregator.py`, `test_layer_c_signal_ring_conformance.py`, `test_five_rings_v0_zero_mutation_ast_cell.py` |
| **qualification matrix / partitions** | Grain-form dispatch + qualification partitions | REUSE | `services/checker/{consequence_classes,state_machine}.py`; `test_dispatch_grain_form_refusal.py`, `test_dispatch_shape_responsive.py`, `test_grain_compatibility_shared_source.py`, `test_qualified_data_selection.py` |
| **C4-032** | Solva stated-at-class per output (five-ring class binding) | REUSE | assertion + five_rings integration |

### Batching, holds, quarantine

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C4-047** | Batch board — every batch's status + resolution | REUSE (backend); 5.7 for surface | `services/service_1/*.py` (25 files in Extraction-Akki) implement batching; frontend batch board in 5.7 |
| **AKKI-OS-V1 ahead file** | `services/service_1/batch_quarantine.py` — Canon 4 §23 per-batch quarantine + systemic-halt threshold + remediation-to-new-version | **HARVEST from Akki-OS-V1** | `Akki-OS-V1/backend/services/service_1/batch_quarantine.py` (227 LOC); ABSENT in RMS-IQ-Core-2 / Extraction-Akki; docstring cites owner ruling `eab_2_hazard_stop_a_ruling_2026_07_24.md` |
| **C4-034 · C4-035 · C4-036** | Worker output manifest + Critic Seam + independence | PARTIAL (Critic Seam is 5.5 mirror) | manifests are five-ring-tagged; Critic Seam absent from spine (see 5.5) |
| **C4-042** | Census idempotent within stated time boundary | REUSE | `services/mtafiti/census.py`; test `test_freshness_*` (3 tests) |
| **C4-043** | Extraction admit carries objective + plan + standards | REUSE | wizard/admission_handoff.py + Northena admit |
| **C4-044** | Extraction runs write to run ledger; batch-level events are ledger rows | REUSE | service_1 uses ledger; test `test_service_1_invariants.py`, `test_service_1_refusal_envelope.py` |
| **C4-045** | Sampling is first-class + throwaway unless promoted | REUSE (backend) | scoped admission path in wizard; sampling surface (5.7 backend uplift) |
| **C4-046** | Deliverables land on shelf with attestations | REUSE | outer_gate mint/receipt/transform |

### Model ladder + registry + MOAC

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C4-035** | Adapters trained on labelled material; registry entry per adapter | PARTIAL | `services/synisense/shield/llm_router.py:1-322` selects models by tier ("fast/standard/deep") but adapter-training pipeline is NOT in spine; Executive-Core's `services/synisense/{engine/,adapter.py}` is the closer implementation (34-file diverged synisense) | REBUILD-candidate on spine |
| **C4-036** | Empty-error-not-shown; the surface says "no model exists for this class" | REUSE (5.7) | see 5.7 |
| **C4-037 (a–f) MOAC six criteria** | Accuracy on uncurated / coverage / refusal / provenance / cost / time | **BUILD** | no adapter registry with MOAC scorecard shipped in ANY of the four repos; six criteria + measurement pipeline is a build item. `Executive-Core backend/services/synisense/pricing.py` and `pool.py` cover cost/allocation only |
| **C4-038** | MOAC evidence drawn from uncurated composition | BUILD | derivative |
| **C4-039** | Rights lineage per adapter (fully resolved) | BUILD | derivative |
| **C4-040** | Adapters version like every artefact; supersede by new row | BUILD | derivative |
| **C4-067 · C4-068** | MOAC drift measured against currently measured composition; latest reading is the one in circulation | BUILD | derivative |

### Quality matrix + three production quality tiers

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **Critic Seam Tier-1/2/3** | Three production quality tiers per Canon 7 §31-§34 | **HARVEST from Akki-OS-V1** | `Akki-OS-V1/backend/services/critic_pass/` (7 files, 950 LOC) — the ONLY implementation across the four repos. Owner ruling `docs/rulings/critic_pass_e1_2026_07_25.md` (2026-07-25 FINAL). Tests: `test_critic_pass_execution_atomic.py`, `test_cif_manifest_submission_gate.py`. Docstring cites Canon 7 §31 verbatim. |
| **C4-031 · C7-024 · C7-025 · C7-026 · C7-027 · C7-028** | Standing quality layer; versioned rubric; amendments; calibration; independence rule | **HARVEST + BUILD calibration wiring** | Akki-OS-V1's `critic_pass/rubric.py` (147 L) + `critic_pass/calibration_ledger.py` (169 L) + `critic_pass/manifest_gate.py` (137 L) + `critic_pass/seeded_defect_corpus.py` (240 L) provide the layer; calibration STALE-surface at Compliance Console (5.7) is BUILD |
| **Critic Seam calibration observability** | Compliance Console surfaces stale calibration | BUILD (5.7 companion) | Canon 5 §18 + Canon 7 §33 |
| **Answer fluency** | Fluency measurement at answer surface (Canon 5 §37 three-lens) | REUSE | `test_answer_fluency_af_g1_to_g8.py`, `services/synisense/shield/fluency_synthesizer.py` |

### G-13 sequencing harness

Chunk-2 carry-forward (c) RESOLVED. `Akki-OS-V1/backend/services/sequencing_harness/` (7 files, 426 LOC).
- `emitter.py`, `enumerator.py`, `executor.py`, `ingest.py`, `measurement.py`, `optimizer.py`.
- Docstring: "harness that executes registered functions against fixture traffic in candidate orderings and measures real cost — not simulated approximations… Class E pinned parameters N=10, α=0.05 per owner ruling `g_13_e1_e2_e3_2026_07_25.md`."
- Registry Doctrine §5.2 + §8.1(b) anchor.
- Test: `Akki-OS-V1/backend/tests/invariants/test_g_13_execution_atomic.py`; also `test_generated_gates_regeneration_diff.py`.

**Class: HARVEST from Akki-OS-V1 into the spine.** Lands here because it measures real cost of ordering candidates (Canon 4 §26.5 cost per operation + Canon 4 §26.6 time to answer). Ties to `services/registry_context/` (also HARVEST) — sequencing_harness's tests import `injector` + `prompt_builder` + `reader` from registry_context.

### Executive-Core work_studio (see Chunk 2 Q7.2)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| Work-Studio compilation surface | Document/deck compilation wizard (~13k LOC backend + 5k+ LOC frontend) | **RE-POINT (LLM) + REBUILD (storage)** | `Akki-Executive-Core backend/routers/{studio,studio_blocks,work_studio_*}.py`; `backend/services/{work_studio,work_studio_*}`; `frontend/src/components/work_studio/*.jsx` (Chunk 2 Q7.2 evidence). LLM already through `shield_invoke`; storage tightly coupled to direct mongo |

## Domain 5.4 subtotals

- REUSE: 15 rows
- HARVEST from Akki-OS-V1: 4 clusters (critic_pass, batch_quarantine, sequencing_harness, gap_candidate_filer→5.3)
- BUILD: 6 (MOAC six criteria + drift + lineage + version-history + adapters registry + calibration observability)
- RE-POINT/REBUILD (Executive-Core work_studio): 1 cluster
- PARTIAL: 3
