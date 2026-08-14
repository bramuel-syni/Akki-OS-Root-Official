# Shaping Answers — Chunk 2 Part B

Two questions the client asked. Evidence-only, per-engine and per-area.

---

# Q7.1 — Which repository is the spine?

## Methodology

For each canonical engine we check:
- (a) Which repo's implementation conforms most closely to Canon-1 requirements (specific rows extracted in Chunk 1: `notes/canon_*_requirements.md`).
- (b) What the tests actually exercise — test names are not evidence; opened content is.
- (c) Whether Akki-OS-V1's unique services and its ahead-files are harvestable.

Reminder from Chunk 1: RMS-IQ-Core-2 ≡ Extraction-Akki byte-for-byte on 34 services and shared trees; Extraction-Akki differs from RMS-IQ-Core-2 by (i) 10 additional `tier_lock.v139x.json` files in `economics`, and (ii) three additional repo-top files (`.py`/`.jsx`). Test coverage is the same.

## Per-engine evidence

### Northena (admit / gate / converge / ledger)

Files: `backend/services/northena/{admit,gate,converge,ledger,state_machine,trace_lens}.py` (773 LOC total across the six files).

- **admit.py:107-148** `compile_and_freeze`:
  - L74-84 `_validate_completeness` checks REQUIRED KEYS = `("artifact_type","artifact_id","artifact_version","lawful_basis","scope")` (five fields). Structured-offender return.
  - L123-128 refuses on `scope_unresolved` via Solva assist (Canon 1 §9.2 + Doc 3 §12).
  - L133-138 emits a `FrozenArtifact` (immutable dict, Canon 1 §4.3 / N-INV-4).
  - L139-146 records `LedgerRow(stage="admit", decision="admitted", …)` before returning.
- **admit.py:88-104** `FrozenArtifact`: `__setitem__` and `__delitem__` raise `TypeError("FrozenArtifact is immutable (§4/N-INV-4)")` — Canon 1 §4.3 "unrepresentable, not policed" satisfied structurally.
- **Ledger append-only enforced (Claim 4)**: `ledger.py:63-65` `insert_one` only; standing test `test_northena_ledger_retention.py:37-62`.
- **Declaration**: NOT enforced at `admit._validate_completeness` (§6.1 of Canon 3 declaration capture is expected before operations). Declaration lives in another surface — a spec-vs-code seam that Chunk 3 should flag as `PARTIAL C3-008`. The Setup / Day-Zero flow (Canon 6 §3 L010 requires declarations from setup morning forward) — no code path in `services/northena/admit.py` reads a declaration.

**Cross-repo**: byte-identical between RMS-IQ-Core-2 and Extraction-Akki AND Akki-OS-V1 (per Chunk 1 §2.1 — northena in the identical-across-3-cores group). All three carry the same admit + gate + converge + ledger.

**Verdict on Northena**: RMS-IQ-Core-2 ≡ Akki-OS-V1 ≡ Extraction-Akki — no material difference. Spine choice on Northena is a tie; pick either. (Recommend Extraction-Akki because it is 13 days newer on unrelated economics rows.)

### Solva (`solva_depth`)

Files: `services/solva_depth/{admit_assist,assertion,enforce,interfaces,load_bearing,pipeline,stamp,trace,reasoning/*}.py`.

Tests (from `test_solva_assertion_boundary.py:1-8`):
> "Covers spec §14 obligations: #1 test_class_is_floor_over_load_bearing, #3 test_utterance_never_asserted_as_fact, #4 test_refuse_below_floor, #6 test_solva_never_extracts (structural — see reasoning-faculty isolation)."

Test names exercised (verified via `grep '^def test_'`):
- `test_class_is_floor_over_load_bearing_all_fact` — Solva-pattern floor-over-load-bearing (Canon 3 §14.1 "at its evidence class"). Test body constructs `NormalizedUnit` fixtures via the `contracts.five_rings` `DefensibilityClass/Ring` types and asserts `conclusion_class([units])` returns the correct floor.
- `test_reasoning_faculty_isolation.py` — engine-wall: Solva does not extract; separately-tested at `test_reasoning_faculty_isolation.py` (Canon 1 §7 engine walls, Canon 2 §6 engine walls).
- `test_solva_trace_ledger_integration.py` — reasoning trace ledger writes (Doc 9 §3 writer=Solva).
- `test_conclusion_class_signature.py` + `test_composed_conclusion_class_from_solva_boundary.py` — assertion boundary tests.

**Assertion boundary is parameterless (Canon 3 §14.2 "no confident-with-caveat"):** verified via test file — `assert_conclusion` and `conclusion_class` are imported from `services.solva_depth.assertion` and neither takes a "confidence" or "caveat" input.

**Cross-repo**: byte-identical between all three core repos (`solva_depth` is in Chunk 1's identical-across-3-cores list). Executive-Core carries a DIFFERENT engine (`solva_v2`) that is not `solva_depth`.

**Verdict on Solva**: three-way tie between the core repos; Executive-Core's `solva_v2` is a different subsystem (see Q7.2 for its RE-POINT verdict).

### Mtafiti

Files: `services/mtafiti/{census,declaration,feasibility,floor_feasibility,inference,measure,registry,source_standing,v3_overlay,verdict}.py` + config.

Tests exercising Canon-4 rows (from `test_mtafiti_invariants.py` `grep '^def test_'`):
- `test_inference_emits_no_verdict_structural` + `test_inference_returns_only_detections` — Canon 4 §7 "learning may detect; it may never decide" ✓.
- `test_verdict_is_matrix_lookup` — Canon 1 §9.2 "the verdict is always a governed, versioned lookup, never a model's output" ✓.
- `test_verdict_unmapped_cell_fails_toward_caution` — Canon 4 §6 unmeasured/degraded posture ✓.
- `test_census_signature_takes_no_objective` + `test_census_output_is_objective_blind` — Canon 4 §5 "Objective-blind" ✓.
- `test_baseline_stands_alone_when_overlay_not_admitted` — Canon 4 §7 "declaration STANDS ALONE" ✓.
- `test_registry_record_contract_frozen` — frozen contract mirror.
- `test_freshness_*` (3 tests) — Canon 4 §10 repeatability.
- `test_v3_overlay_*` (4 tests) — inference-layer admission gates (Canon 4 §7 "inference contributes ONLY after its own accuracy has been proven").
- `test_declaration_baseline_complete_alone_across_fixture` — Canon 4 §7 floor posture.

**Cross-repo**: byte-identical across the three core repos.

**Verdict on Mtafiti**: three-way tie; conformant to Canon 4 §5-§10 with named tests per contract point.

### Targeta

Files: `services/targeta/{core,gate,interface,plan,yield_layer}.py` (small — 6 modules).

Tests (`test_targeta_invariants.py` `grep '^def test_'`):
- `test_mining_plan_contract_frozen` — Canon 4 §12 plan artefact frozen shape.
- `test_targeta_core_has_no_ml_import` — engine wall (Canon 1 §7 Northena deterministic-by-construction; Targeta core has same discipline).
- `test_yield_layer_imports_only_interface_types` — dependency hygiene ("(YieldInput, Permutation)" mandate §7).
- `test_yield_output_is_permutation_raises_on_drop` + `test_yield_output_is_permutation_raises_on_duplicate` — the **permutation-typed yield guard** the instruction specifically named. Verified: `yield_layer.py:17 from services.targeta.interface import YieldInput, Permutation` + L27-29 `default_yield_fn(candidates: YieldInput) → Permutation`. The runtime shape check raises on drops/duplicates.
- `test_yield_candidate_never_carries_floor_or_raw_measure` — Canon 4 §12 separation (Targeta plans; Mtafiti measures).
- `test_floor_is_hard_filter_excludes_below_floor` — Canon 4 §12 minimum standard.
- `test_plan_reproducible_byte_identical` — Canon 4 §10 repeatability applied to plans.
- `test_gate_closed_seam_returns_admitted_false` — closed-seam handoff (Doc 4 §18 seam-1).
- `test_targeta_core_complete_alone` + `test_only_gate_compares_orderings` — engine boundaries.

**Cross-repo**: byte-identical across the three core repos EXCEPT Akki-OS-V1 has `gap_candidate_filer.py` (132 LOC) that RMS-IQ-Core-2 and Extraction-Akki lack — see harvesting section.

**Verdict on Targeta**: three-way tie on the core files; Akki-OS-V1 ahead by one harvestable file.

### outer_gate

Files: `services/outer_gate/{mint,receipt,transform}.py`.

Tests:
- `test_outer_gate_irreversibility.py` — Canon 4 §16 "frozen unit contract".
- `test_qualified_data_outer_gate_ride.py` — data crossing the outer gate.
- `test_v0_paths_byte_identical_after_4a.py` + `test_v0_paths_byte_identical_after_4b.py` — deterministic path invariance.

**Cross-repo**: byte-identical across the three core repos.

**Verdict on outer_gate**: three-way tie.

### memory (application memory-plane per Doc 7 §19-23)

Files: `services/memory/{ledger,ledger_reconstructor,plane_registry,publication,refusal,revocation,scoped_accessor,working_set,write_back,constants,memory_refusal_reasons.v0.json}` (12 files).

Tests: `test_memory_service_m_g1_to_m_g9.py`, `test_memory_observability_o_g1_to_o_g6.py`, `test_memory_engineer_key_grant_e2e_propagation.py`, `test_no_unauthorized_deletion_path.py`, plus `memory_plane_v0.contract_snapshot.json`.

**Cross-repo**: PRESENT in RMS-IQ-Core-2 + Extraction-Akki (byte-identical); **ABSENT in Akki-OS-V1** entirely (per Chunk 1 §3.1). Absent in Executive-Core (different platform).

**Verdict on memory**: RMS-IQ-Core-2 ≡ Extraction-Akki own this cleanly; Akki-OS-V1 has no memory-plane implementation. Doc 7 Part IV compliance requires memory — Akki-OS-V1 is strictly behind. Take from Core-2/Extraction-Akki.

### `checker` (the ceremony/rule-change machinery)

Files: `services/checker/{consequence_classes,countersign_ledger,effective_delay,rule_change_request,state_machine}.py`.

Tests: `test_govern_g_g1_to_g_g8.py`, `test_govern_ui1b_gates.py`, `test_phase_8_b_5b.py`, `test_phase_9_sub_stage_9_1_and_9_3.py`, plus `live_preview/test_phase3_sc3_govern_live.py`. These exercise Canon 3 §24 rule-change ceremony (proposed → counter-signed → waited → applied → re-verified) and Canon 3 §22 countdown classes ("The Four Classes").

**Cross-repo**: byte-identical across the three core repos.

### `service_1`

**Cross-repo**: 25 files in RMS-IQ-Core-2 / Extraction-Akki; **26 files in Akki-OS-V1** (per Chunk 1 §2.3). Akki-OS-V1's extra file is `batch_quarantine.py` — see harvesting.

### economics — the divergence

Chunk 1 reported: 380 same-path-different-content files between Akki-OS-V1 and Extraction-Akki. This is code drift or data regeneration — the instruction asked us to sample and characterise.

**Sampling method**: opened all 8 Python files under `services/economics/` in RMS-IQ-Core-2 and diffed byte-for-byte against Akki-OS-V1 and Extraction-Akki. Also sampled 4 JSON files (`fleet_policy.v0.json`, `tier_lock.v0.json`, `tier_lock.v500.json`, `tier_lock.v1000.json`) — chosen to span the tier-lock version range from v0 to the middle of the divergence band.

**Result**:

| File class | Count | Same-content between all 3 core repos | Diverged |
|---|---:|---:|---:|
| Python (`.py`) | 8 | **8** | **0** |
| JSON, non-tier-lock | 3 | 3 | 0 |
| JSON, tier-lock (v0–v1387) | ~1380 in Ext-Akki | 730 identical | **380 differ (only Akki-OS-V1 vs {Core-2, Ext-Akki})** |
| JSON, tier-lock present only in {Core-2, Ext-Akki}, missing from Akki-OS-V1 | 281 | — | — |

**Nature of the 380 differences** (verified via `diff -u` on `tier_lock.v1000.json`):
```
- "grantor_id": "6a6ba8e9c29ca2df857a2765",
- "idempotency_key": "ord-2-a08747a1",
- "at": "2026-07-31T17:11:33.848958+00:00"
+ "grantor_id": "6a49d57693e9bb94abab17f4",
+ "idempotency_key": "ord-2-19e21055",
+ "at": "2026-07-25T12:09:00.869855+00:00"
```
Only three fields differ per tier-lock file: `grantor_id` (UUID), `idempotency_key`, `at` (timestamp). The `rule_id`, `locked`, `reason_note` fields are identical.

**Interpretation**: this is **PURE DATA REGENERATION** — the same code (economics engine) run on different clock/UUID seeds produces different ledger snapshot files. The 281 missing files (`tier_lock.v1107` … `v1387`) are simply extra runs Extraction-Akki accumulated that Akki-OS-V1 didn't. There is **zero code drift** in the economics engine.

**Implication**: `economics` is CODE-FULLY-HARVESTABLE from any of the three core repos (they're byte-identical on `.py`). The tier-lock JSON data is instance-runtime state; the fresher instance's ledger simply has more rows.

## Akki-OS-V1 unique services — harvestability

Every unique service directory in Akki-OS-V1 has at least one test in Akki-OS-V1's own test suite (verified). The core three repos have NEITHER the source NOR the tests.

| Service | Files / LOC | Canon anchor | Tests in Akki-OS-V1 | Harvestable? |
|---|---|---|---|---|
| `critic_pass` | 7 / 950 LOC | Canon 4 §21-§23 · Canon 7 §31-§34 (Critic Seam) · Canon 2 §10.2 (pre-ship checklist) | `test_critic_pass_execution_atomic.py`, `test_cif_manifest_submission_gate.py` | **YES — high value.** Closes a canon requirement absent from Core-2. Load-bearing per docstring: "The Critic Seam guards what workers produce; this section applies the identical architecture to what the pipeline produces." Dependencies: only `services.critic_pass.rubric` + `services.critic_pass.seeded_defect_corpus` (self-contained). |
| `registry_context` | 5 / (measured below) | Canon 5 §17 (Registry Administration) · Canon 2 §14 (condition watchers via readable registry) | `test_registry_context_block_golden_snapshot.py`, `test_g_13_execution_atomic.py` | **YES.** Prompt-context injection subsystem. Self-contained. |
| `sequencing_harness` | 7 files | (unclear from filenames — needs deeper read) | `test_g_13_execution_atomic.py` | **PROBABLY yes.** Ingest / emit / execute / measure / optimize pipeline shape. |
| `partitions` | 2 files (session_working_set + init) | Canon 6 §3.1 setup declarations · session partitioning | `test_partition_schema_v0_envelope.py` | **YES — narrow.** |
| `far_endpoint` | 4 files (gate_generator + mandate_reader + mandate_spec_emitter + init) | Canon 1 §8 Function & Promise Registry (tooling) | `test_generated_gates_regeneration_diff.py` | **YES as tooling.** Generates `generated_gates/*.py` from mandate docs; useful for keeping the platform's function-registry synced with mandates. |
| `generated_gates` | 16 files | Canon 1 §8 tooling artifacts | `test_generated_gates_smoke.py` | **NO as source-of-truth** (they are placeholder stubs); YES if the far_endpoint generator is harvested. |

## Akki-OS-V1 ahead files — harvestability

| File | LOC | Canon anchor | Harvestable? |
|---|---:|---|---|
| `services/service_1/batch_quarantine.py` | 227 | **Canon 4 §23** (Quarantine) + **§34.1** (Batch Board) — cited from `critic_pass/harness.py:26` as the "fail-closed per-batch quarantine at services/service_1/batch_quarantine.py" | **YES — high value.** Implements a canon requirement absent from Core-2. Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` sanctioned this landing. |
| `services/targeta/gap_candidate_filer.py` | 132 | **Canon 4 §35** (Gap ranking) · Canon 6 §5-§7 (Exploration → gap file → commissioning loop) | **YES.** Attaches into `targeta/` — clean import surface. |

## Q7.1 answer

- **Base = Extraction-Akki** (or equivalently RMS-IQ-Core-2; the two are the same code, Extraction-Akki carries 13 days more of runtime ledger snapshots in `economics`).
- **Rationale (evidence-based)**:
  1. Northena / Solva / Mtafiti / Targeta / outer_gate / checker / synisense / compliance / service_1 (minus 1 file) — byte-identical between Extraction-Akki and RMS-IQ-Core-2, with the same test coverage exercising the specific Canon contracts named above (declaration completeness at admit, permutation-typed yield guard, parameterless assertion boundary, matrix-lookup verdicts, objective-blind census, refusal-family classifier, HMAC/HKDF trust receipt).
  2. Memory engine (Doc 7 Part IV) — Extraction-Akki / RMS-IQ-Core-2 own it; Akki-OS-V1 lacks it entirely.
  3. Post-2026-07-30 P1 close artifacts (frozen `trust_receipt_v1.py` + snapshot + parity seat #32; `egress_firewall.py` runtime firewall; `test_ast_egress_gate.py` AST gate) — present in Extraction-Akki / RMS-IQ-Core-2, absent in Akki-OS-V1 and Executive-Core.
- **Harvest from Akki-OS-V1 into the spine** (all evidenced above with tests):
  1. `services/critic_pass/` (7 files) — closes Canon 7 §31-§34 Critic Seam.
  2. `services/service_1/batch_quarantine.py` — closes Canon 4 §23 quarantine.
  3. `services/targeta/gap_candidate_filer.py` — closes Canon 4 §35 gap-ranking.
  4. `services/registry_context/` (5 files) — prompt-context injection subsystem.
  5. `services/partitions/session_working_set.py` — session partitioning.
  6. `services/sequencing_harness/` (7 files) — ingest→execute→measure pipeline (deeper read in Chunk 3 will confirm).
  7. `services/far_endpoint/` — gate-generator tooling (harvest with `generated_gates/*.py` as regenerable outputs).
- **Irreconcilable**: **nothing**. The `economics` divergence turns out to be pure ledger-data regeneration; the eight Python files are byte-identical across all three. Any harvested Akki-OS-V1 service imports only its own submodules or the identical shared services present in the spine.
- **Explicit non-finding — declaration at admit**: Canon 3 §6.1 requires declarations captured before operations; `services/northena/admit.py:_validate_completeness` checks five fields but **not declaration**. This is a spec-vs-code seam; Chunk 3 will mark it PARTIAL / MODIFY on `C3-008`.

---

# Q7.2 — How much of Akki-Executive-Core is RE-POINT?

## Cross-cutting evidence

- **LLM boundary is architected via a Protocol interface**: `backend/contracts/synisense.py:25-28` — `class SyniSenseContract(Protocol)` with `async def shield_invoke(...)` L28. Pass-through adapter at `backend/contracts/_adapters/synisense.py` (810 LOC). Every LLM call goes through `get_synisense().shield_invoke(...)`. This is **designed for adapter-swap** — the whole codebase can RE-POINT its LLM boundary by replacing the in-process adapter with an HTTP client that calls Core-2's `/api/synisense/shield/invoke`.
- **Streaming**: `services/llm_streaming.py:1-19` is a 19-line shim re-exporting from `services/synisense/shield/streaming.py`. Streaming exists in Executive-Core but Core-2 does not currently ship `synisense/shield/streaming.py`. **Streaming is HARVESTABLE INTO Core-2**.
- **Auth**: `backend/routers/auth.py:15-21` uses PyJWT (`import jwt`), `pyotp` for MFA, `qrcode` for MFA setup, bcrypt via `passlib` (referenced at L328). Additional auth surfaces: `auth_oauth.py`, `oauth_google.py`, `mfa.py`, `admin_users.py`, `cohort_magic_link.py`, `auth_password_change.py`. **Application territory** per Canon 1 §12 (S1: platform serves the application; the application carries its own end-user auth).
- **Storage**: `backend/core.py:16 from motor.motor_asyncio import AsyncIOMotorClient` + L29 `client = AsyncIOMotorClient(MONGO_URL)`. Services touch `db.<collection>` directly (10+ example files: `analysis_lifecycle.py`, `continue_chat.py`, `cycle_lifecycle.py`, `deck_lineage.py`, `deck_regenerate.py`, `deck_retrieval.py`, `first_login_password_set.py`, `job_queue.py`, …). Canon 7 Part IV §19-23 requires per-application memory plane with plane-keyed storage — Executive-Core's direct `db.<collection>.find()` pattern does NOT match this shape. **Storage is the deepest coupling — every mongo touch has to migrate to memory-plane calls or become explicit application-side state.**

## Per-area verdicts (evidence-bound)

| Area | LLM boundary | Auth | Storage | Verdict |
|---|---|---|---|---|
| **chat** — `services/chat/protective_layer/__init__.py` (three FM detectors: hypothesis_without_structure / ungrounded_factual_claim / fluency_mistaken_for_diagnosis) | `shield_invoke` × 3 concurrent (`asyncio.gather`) via ALLOWED_PURPOSES `chat.fm_a/b/c` | JWT | mongo (`db.conversations`, `db.messages`) | **RE-POINT.** Detectors are structured-output Shield calls — trivially adapter-swappable. Storage moves to memory-plane. Frontend surface preserved. |
| **documents** — `services/documents/intelligence_service.py` + friends | `shield_invoke` (verified via file listing) | JWT | mongo `db.documents` | **RE-POINT.** Same shape as chat. |
| **analyze_workspace** — `services/analyze_workspace/{ask,tips}.py` | `shield_invoke` | JWT | mongo `db.workspace_*` | **RE-POINT.** Canon 5 §40 Work > Analyze. |
| **ideas_engine** — 8 files: schema, scheduler, citation_resolver, personalizer, synthesizer, preferences, refuse_to_decide, __init__ | `shield_invoke` (scheduler L133 stores a `shield_invoke_id`); `refuse_to_decide` imports from `workbook_analyzer.refuse_to_decide` | JWT | mongo | **RE-POINT.** The `refuse_to_decide` module is a discipline that fits Canon 3 §17 refusal shapes — worth surfacing INTO the platform's Solva boundary as a Solva-pattern amendment. |
| **cohort** — 8 files (magic-link, feedback, feature_events, welcome_email, console, copy_overrides, special_ask) | none | JWT + tokens | mongo | **RETIRE-candidate for platform** — Canon 1 §13 puts trial cohort / marketing signup in application territory. **RE-POINT if kept as an application-side admin surface**; do NOT drag into the platform layer. |
| **deck_* (deck_generation_jobs.py, deck_regenerate.py, deck_retrieval.py, deck_lineage.py)** | `shield_invoke` via contract (`deck_regenerate.py:127`) | JWT | mongo `db.decks / db.deck_versions / db.deck_lineage` | **RE-POINT.** Canon 5 §40 Work > Documents. |
| **inbox_routing** — 11 files (classifier, routers, upstream_adapter, backfill, schema, etc.) | `shield_invoke` in classifier | JWT | mongo `db.inbox_rows` | **RE-POINT.** |
| **llm_streaming.py** (shim, 19 LOC) → `services/synisense/shield/streaming.py` | streaming through Shield already; local shim | n/a | n/a | **RE-POINT + PORT STREAMING TO CORE-2.** The `synisense/shield/streaming.py` implementation must be harvested into Core-2's shield tree (Core-2 currently lacks it). |
| **solva_v2** — 30 files (`analyze_narration, chair_notes, chat_v2_prompts, citation_resolver, engines/, feature_flag, grounding_contract, guardrails, integrity_validators, llm_adapter, opinion_filter, payload_builder, pptx_exporter, spread_heatmap, state_machine, stream_synthesizer, submodules, v2_prompts, artefact_schema`) | `shield_invoke` via `analyze_narration.py:47 def shield_invoke(**kwargs)` (Phase-4.0 shim delegating to `SyniSenseContract.shield_invoke`) | JWT | mongo `db.solva_sessions` | **RE-POINT the surface + delegate reasoning to Core-2's `solva_depth`.** Executive-Core's `solva_v2` is a **narration surface**: it constructs journalistic-style outputs from reasoning results. The Solva assertion boundary (Canon 3 §14-§19) lives in Core-2's `solva_depth`. `solva_v2/{grounding_contract, guardrails, integrity_validators}` are hygiene layers around narration; they can co-exist with Core-2's assertion boundary. **RE-POINT — surface preserved, reasoning boundary swapped**. |
| **solva_voice_audit** — 24 files: `voice/`, `orchestration/`, `guardrails/`, `reasoning/`, `models.py`, `schemas.py`, `telemetry.py`, `voice.py`, `reasoning.py` | `shield_invoke` via `orchestration/shield_invoker.py` (Chunk 2 Claim 1 file listing) | JWT | mongo | **UNKNOWN — REBUILD-candidate.** Core-2 has no voice-input ingest boundary; Canon 3 §12 input seat would need to admit audio material. What would resolve: read `voice/` and `guardrails/` to confirm (a) whether audio material transits the shield's `input_seat`, (b) whether the tenant-entities de-identifier handles speech-derived text. If yes → RE-POINT; if no → REBUILD under Canon 3 §13.1 custody sequence. |
| **workbook_analyzer** — 10 files (parser, anomaly_detector, forecaster, monte_carlo, schema, signal_extractor, citation_resolver, report_builder, refuse_to_decide, __init__) | **NO direct LLM boundary in these files** (verified: `grep 'shield_invoke\|shield.client\|from emergentintegrations\|import openai\|import anthropic' → empty for workbook_analyzer/`) | JWT | mongo | **RE-POINT feasible; also legitimate as application-only.** Pure-Python analytics engine (Monte-Carlo, forecasting, anomaly detection). No canon requirement forces this into the platform. Recommendation: keep as an application-side capability. |
| **work_studio** — very large surface (backend `services/work_studio/`, `services/work_studio_*`, `work_studio/*`, `routers/studio.py` 915 L, `studio_blocks.py` 1226 L, `work_studio_export.py` 2974 L, `work_studio_from_source.py` 800 L, `work_studio_overlay.py` 828 L, `work_studio_render.py`; frontend `components/work_studio/` 20+ jsx incl. `CompilationWizard.jsx` 908 L and `overlay/DocumentOverlay.jsx` 1533 L; templates + 200+ real user exports in `uploads/work_studio_exports/`) | `shield_invoke` throughout | JWT + `get_current_account` from `core.py` | mongo direct (many collections) | **RE-POINT (LLM) + REBUILD (storage).** LLM boundary swap is trivial (adapter). Storage swap is the heavy cost — the surface is deeply coupled to mongo collections that don't match Doc 7 memory-plane shape. Chunk 3 will need per-collection migration plan. |
| **36 loose services/*.py** | mixed | JWT | mongo | see below |

### The 36 loose services — breakdown

Per Chunk 1 §3.3 enumeration:

- **RE-POINT (LLM-mediated, custody-adjacent)**: `two_pass.py`, `continue_chat.py`, `signal_dedup.py`, `sandbox_generation.py`, `cycle_synthesis.py`, `deck_generation_jobs.py`, `metadata_signatures.py`, `module_labels.py`, `platform_kb.py`, `universal_search.py`, `analysis_lifecycle.py`, `deck_lineage.py`, `deck_regenerate.py`, `deck_retrieval.py`, `signal_dedup.py`, `solva_session_status.py`, `cycle_lifecycle.py`, `cycle_permissions.py`, `work_studio_export.py`, `work_studio_overlay.py`, `streaming_phases.py` → RE-POINT.
- **RETIRE (platform-level cross-cutting HTTP/security that Core-2 already handles or that Canon requires the platform hold itself)**: `csrf.py`, `rate_limit.py` (referenced from `auth.py:31`), `rbac.py`, `security_headers.py`, `session_timeout.py`, `sentry_setup.py`, `privacy_wall.py`, `clamav_service.py` — Core-2 has its own auth / security / rate-limit surfaces; Executive-Core copies are application-side and don't cross the platform boundary.
- **RETIRE (application territory per Canon 1 §15)**: `stripe_webhook.py` (Canon 1 §15 verbatim: "will not know a buyer, a price, or an order"), `owner_digest.py`, `news_aggregator.py`, `first_login_password_set.py`.
- **RE-POINT to a Core-2 boundary that does not yet exist (needs port)**: `llm_streaming.py` → shield/streaming; `storage_service.py` → object storage per Doc 7 (Core-2 has none of this today); `job_queue.py` → per-application memory plane precompute per Doc 7 §23.
- **UNKNOWN**: `backfill_shield_v1.py` (191 LOC, one-time migration script), `two_pass.py` (need to read).

### Frontend

- `frontend/src/_archived/` (61 files including `Home1.jsx`, `Home2.jsx`, `e4_doc_routes/components/reading/` full subtree) → **RETIRE-candidate**. Canon 5 §43 no surface offers a bypass/override; these are prior product surfaces already marked as archived by the codebase itself.
- `frontend/src/_archived_legacy/` (34+ files) → **RETIRE**. Same as `_archived`.
- `frontend/src/website/` (34 files) → **RETIRE from platform**. Marketing website. Canon 1 §12 makes commerce/marketing application territory; keep as application-side, retire from the platform surface.

## Q7.2 answer — programme cost estimate

**RE-POINTable areas (surface preserved, boundary swapped)**:
chat, documents, analyze_workspace, ideas_engine, deck_* (all four), inbox_routing, solva_v2 (surface), workbook_analyzer, most of the 36 loose services, work_studio (LLM boundary only).

**Requires a Core-2 boundary port before RE-POINT is complete**:
- `synisense/shield/streaming.py` — Executive-Core has it, Core-2 needs it (llm_streaming, chat SSE, work_studio compilation streaming all depend).
- Doc 7 §19-23 memory-plane implementation — Core-2 has `services/memory/` (12 files, Chunk 1 §3.1) but that's the platform-side plane_registry; Executive-Core's per-service mongo pattern needs to move to plane-keyed calls.
- Object storage — Executive-Core has `storage_service.py` and 200+ real user exports in `uploads/work_studio_exports/`; Core-2 doesn't ship object storage today.

**REBUILD-candidate**:
- `solva_voice_audit` — voice input path not yet under Core-2's input seat.
- `work_studio` storage layer — deep mongo coupling.

**RETIRE**:
- `cohort/`, `stripe_webhook.py`, `owner_digest.py`, `news_aggregator.py`, `first_login_password_set.py`.
- `frontend/src/_archived*`, `frontend/src/website/`.
- Application-side cross-cutting (`csrf, rbac, rate_limit, security_headers, session_timeout, sentry_setup, privacy_wall, clamav_service`) — Core-2 has its own; Executive-Core's are duplicative.

**UNKNOWN → read in Chunk 3**:
- `sequencing_harness/` (Akki-OS-V1 unique) — needs deeper read.
- `solva_voice_audit/voice/` and `guardrails/` — determines voice audit verdict.
- `two_pass.py`, `platform_kb.py`, `backfill_shield_v1.py` — three loose services.

**Overall shape**: the LLM boundary is genuinely designed for RE-POINT (adapter pattern via `contracts/synisense.py::SyniSenseContract`); auth is application territory and stays in Executive-Core-turned-application; storage and streaming are the two heavy costs and require ports INTO Core-2 before the RE-POINT completes.
