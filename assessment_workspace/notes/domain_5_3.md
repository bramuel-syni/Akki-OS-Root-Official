# Domain 5.3 — Measurement, Targeting, Reasoning

Scope (instruction §5.3): census + registry · two-layer defensibility ·
qualification matrix · Targeta eligibility core + permutation-typed yield guard ·
Solva's two faculties + parameterless assertion boundary · the trace.

Spine cited: **Extraction-Akki** (≡ RMS-IQ-Core-2 byte-identical).

## Rows classified in this domain

### Mtafiti (measurement)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C1-055** | Estate as single measurable object at any scale | REUSE | `services/mtafiti/{measure,census,registry}.py` |
| **C1-056** | Three states per region, equal prominence: sound/degraded/not-yet-measured | REUSE | `services/mtafiti/verdict.py` matrix; test `backend/tests/invariants/test_mtafiti_invariants.py::test_verdict_unmapped_cell_fails_toward_caution` |
| **C1-057** | Unmeasured region never rendered empty/clean/zero | REUSE | verdict.py + composition module; `test_feasibility_honesty_under_absence.py` |
| **C1-058** | Two-layer defensibility: declaration (floor) + inference (overlay) | REUSE | `services/mtafiti/declaration.py`, `inference.py`, `v3_overlay.py`; `contracts/five_rings.py:255-269` runtime_mode Literal["declaration_baseline","inference_overlay"] |
| **C1-059** | Inference contributes only after its own accuracy proven; until then declaration stands alone | REUSE | `test_baseline_stands_alone_when_overlay_not_admitted`; `test_v3_overlay_*` (4 tests) exercise inference admission gates |
| **C1-060** | Neither layer decides meaning — verdict is governed, versioned lookup | REUSE | `test_mtafiti_invariants.py::test_verdict_is_matrix_lookup` |
| **C1-061** | Learning may detect; may never decide (general rule) | REUSE | `test_mtafiti_invariants.py::test_inference_emits_no_verdict_structural` + `::test_inference_returns_only_detections` |
| **C4-003 · C4-004 · C4-005 · C4-006 · C4-007 · C4-008 · C4-009 · C4-010 · C4-011 · C4-012 · C4-013** | Mtafiti canon rows (charter, objective-blind, three states, degraded field, two-layer, meaning lookup, floor confidence render, repeatable) | REUSE | same file cluster + invariants tests above; all canon 4 §5-§10 requirements are met by the current implementation |

### Targeta (targeting)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C4-014** | Charter — Targeta plans extraction against a frozen objective; writes mining plans | REUSE | `services/targeta/{core,gate,interface,plan,yield_layer}.py` |
| **C4-015** | Operates only on frozen objectives (never amending) | REUSE | admit_assist gate at `services/solva_depth/admit_assist.py`; frozen artefact enforced (C3-007) |
| **C4-016** | Plan artefact lists reused stock, extraction volume as range, expected coverage, what CANNOT be covered | REUSE | `test_targeta_invariants.py::test_mining_plan_contract_frozen` |
| **C4-017** | Reuse-first: prior extractions identified before proposing new work | PARTIAL | test coverage lists reused stock in plan; the reuse-lookup mechanism spans `mtafiti/registry.py` — verify in Chunk 4 |
| **C4-018** | Coverage figure as range, drawn from Mtafiti composition | REUSE | `test_targeta_invariants.py::test_yield_candidate_never_carries_floor_or_raw_measure` + plan schema |
| **C4-019** | Shaping wizard renders plan preview before commitment | REUSE (backend) / (see 5.7 for surface) | `services/wizard/*.py`; router `backend/routers/wizard.py`; test `backend/tests/invariants/test_phase_7_stage_b_1_wizard.py` |
| **C4-020** | Plan versioned; material changes → new plan superseding | REUSE | ledger append-only + plan snapshot pattern |
| **Permutation-typed yield guard** | `default_yield_fn(candidates: YieldInput) → Permutation` with `raises_on_drop / raises_on_duplicate` runtime shape checks | **REUSE** | `services/targeta/yield_layer.py:17-29`; `test_targeta_invariants.py::test_yield_output_is_permutation_raises_on_drop` + `::test_yield_output_is_permutation_raises_on_duplicate` |
| **AKKI-OS-V1 ahead file** | `services/targeta/gap_candidate_filer.py` (132 LOC) — Canon 4 §35 gap-ranking with carried demand evidence | **HARVEST from Akki-OS-V1** | present at `Akki-OS-V1/backend/services/targeta/gap_candidate_filer.py`; ABSENT in RMS-IQ-Core-2 / Extraction-Akki | Chunk-2 harvest item; closes the operating-loop gap-ranking |

### Solva (reasoning depth)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C3-022** | Solva reasons — multi-step, cross-source triangulation, hypothesis weighing | REUSE | `services/solva_depth/{admit_assist,assertion,enforce,load_bearing,pipeline,reasoning/*}.py` |
| **C3-023** | Stated-at-class + assertion bar + contradiction surfaced + refuse-with-reason | REUSE | `assertion.py` + `enforce.py`; test `test_solva_assertion_boundary.py` + `test_composed_conclusion_class_from_solva_boundary.py` |
| **C3-024** | No confident-with-caveat (Canon 3 §14.2) | REUSE | assertion.py returns floor-over-load-bearing; test verifies parameterless signature (no `confidence` / `caveat` kwarg) |
| **C3-025** | Reasoning trace as ledger row | REUSE | `services/solva_depth/trace.py`; `test_solva_trace_ledger_integration.py` |
| **C3-026** | Intent audit divergence field emitted for Watch | **PARTIAL** | intent-audit divergence field lives in trace shape; the Watch consumer (5.8) is BUILD, so the field is currently un-consumed |
| **C3-027** | Three refusal shapes: evidence-class, coverage, contradiction | REUSE | refusal families (Chunk-2 Claim 5) map to these shapes via `services/compliance/refusal_family_classifier.py` |
| **C3-028** | Independence rule — reviewing instance must differ genuinely (base or context) | PARTIAL | Solva-pattern invariance is asserted in tests, but a machine-checked independence gate on the reviewer selector is not present | Chunk-4 to build |
| **C3-029** | Solva-pattern is platform-wide validation rubric for every judgement engine | REUSE (via re-use) | five_rings + assertion + enforce reused across Mtafiti, Solva, use_data |
| **C1-042 · C1-043 · C1-044 · C1-046 · C1-047 · C1-048 · C1-049 · C1-050 · C1-051 · C1-052 · C1-053 · C1-054** | Six engines / three axes / two authorities / one identity per task / disagreement / Function & Promise Registry | PARTIAL — 5.9 mirror for the two-authorities pieces; the engines and registry pieces are present here | `contracts/five_rings.py`, `contracts/mtafiti_registry.py`, and the six engines listed above. The Function & Promise Registry as a named artifact is `docs/machine_readable_registry.md` + `docs/close_reports/machine_readable_registry.md` — verified in Chunk 1 |

### The Trace

`backend/services/solva_depth/trace.py` + `test_solva_trace_ledger_integration.py`. Reasoning traces are ledger rows; readers are governance surfaces + auditors (Doc 9 §3). REUSE.

### Cross-engine correlation

`backend/tests/invariants/test_trace_lens_cross_engine_correlation.py` + `test_trace_lens_readonly.py` — verifies traces are joinable across Mtafiti / Solva / outer_gate without shared writes. REUSE.

## Solva-voice-audit (Executive-Core)

Chunk-2 carry-forward (b) — RESOLVED:

- Executive-Core `backend/services/solva_voice_audit/` (24 files) is a **text-based coach-voice audit**, NOT an audio input path. "Voice" = tone/coach-voice (curated deterministic question bank at `voice/question_bank.py`, refusal_voice, synthesis_renderer, invariants). All LLM boundaries go through `shield_invoker.py` (delegates to `SyniSenseContract.shield_invoke`).
- `reasoning/{triangulation_engine,frame_audit_engine,candidate_generation,probability_weighting,refusal_logic,situation_class_classifier,tension_detection}.py` — a coaching reasoning pipeline distinct from Core-2's `solva_depth`.
- `guardrails/classifiers.py` — jailbreak / therapy / coaching classifiers (three concurrent `shield_invoke` per turn with `solva.guardrails.*` purposes; blocked_hard / blocked_soft / ok outcomes).

Classification: **RE-POINT** (Executive-Core surface preserved; the reasoning boundary swaps to Core-2's `solva_depth` assertion boundary). Not BUILD, not REBUILD.

## Domain 5.3 subtotals

- REUSE: 22 rows
- PARTIAL: 4 (C4-017 reuse-first; C3-026 intent-audit un-consumed; C3-028 independence gate; the two-authorities cluster is partially here + 5.9)
- HARVEST from Akki-OS-V1: 1 (gap_candidate_filer.py)
- RE-POINT: 1 (solva_voice_audit surface)
- N/A-DOCTRINE: 0
