READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_SOLVA_V2_LIFT_close.md — wave close manifest

**Wave:** `W-SOLVA-V2-LIFT` · standalone reasoning component (owner directive 2026-09-13: NOT a sub-component of Registry or DAP).
**Closes:** delivers the reasoning-plane primitives (two-faculty seam, parameterless assertion-boundary signature, load-bearing set, three-action refusal, trace, intent audit, Critic Seam Tier 2 binding) canon-grounded first-hand; case-agnostic donor lift from `Akki-Executive-Core` with executive-domain tokens stripped and ambiguous constructs HALTED.
**Wave opened:** 2026-09-13 · ratchet floor 3531 (post-W-REGISTRY-EXTENSION-G3).
**Wave closed:** 2026-09-13 · ratchet floor **3562** (+31 invariants).
**Output seal:** `phase0/output_verified_seals/solva_v2_lift.seal.txt` · `Kind: solva_v2_lift` · sha256 `f929f026209e02b1d929100ff091e39321fa5125d4632f9626b9920f2ea06023`.

---

## §A · CP roll-up (8 CPs · +31 invariants · 0 push)

CP-S2 landed FIRST per owner directive ("the parameterless assertion-boundary signature must be built and asserted BEFORE the load-bearing reasoning function").

| CP | Order | Δ | Focus | Grounding test |
|--:|--:|--:|---|---|
| **CP-S2** | **1st** | 5 | Parameterless assertion-boundary signature — `compute_class(load_bearing: LoadBearingSet) -> AssertionClass`. Exactly one parameter; no confidence/strength/weight/evidence/score. Signature-as-guard invariants under `typing.get_type_hints`. `AssertionClass` closed 3-value enum. | `test_wsolvalift_cp_s2_assertion_boundary_signature.py` |
| CP-S1 | 2nd | 3 | Two-faculty seam via **import assertion** (Doc-0 §BR-2.1). `services/solva_v2/reasoning_faculty.py` does not import `assertion_boundary.compute_class` or the whole module; `assertion_boundary.py` does not import `reasoning_faculty` (any symbol). AST-parsed negative-scan. | `test_wsolvalift_cp_s1_two_faculty_seam.py` |
| CP-S3 | 3rd | 3 | Load-bearing function returns `UnitRef`s only (Canon-4 §22). Return type includes `UnitRef` (via `LoadBearingSet` or `Sequence[UnitRef]`); no parameter typed as `AssertionClass`. | `test_wsolvalift_cp_s3_load_bearing_returns_refs.py` |
| CP-S4 | 4th | 4 | Three-action refusal envelope (Canon-4 §24) — `{accept_as_stated, narrow_objective, lower_standard}`; nothing else. Fourth action refused at pydantic validation. Donor's `{clean, jailbreak_attempt, out_of_scope, distress_flag, extraction_marker}` NOT present (negative-scan). | `test_wsolvalift_cp_s4_three_action_refusal.py` |
| CP-S5 | 5th | 3 | Trace from the first commit (Canon-4 §26). `SolvaTrace` schema has 5 canon fields (session_id, reasoning_path, load_bearing_units, computed_class, conclusion) + `au_3b_defensible=False` R-C2 marker asserted. | `test_wsolvalift_cp_s5_trace_from_first_commit.py` |
| CP-S6 | 6th | 3 | Intent audit (Canon-4 §21.1) — declared vs demonstrated distinct fields. Append-only update returns a new record; original unchanged (Canon-3 §9.3 spirit). | `test_wsolvalift_cp_s6_intent_audit.py` |
| CP-S7 | 7th | 4 | Critic Seam Tier 2 (Canon-7 §44/§44.1). `CriticInvocation` carries `{artefact, canon, authorising_instrument, rubric}` only — negative-scan for `author_rationale/worker_rationale/reasoning_draft` (blind-spot rule). `CriticFindings` has no blocks/edits/override fields. | `test_wsolvalift_cp_s7_critic_seam.py` |
| CP-S8 | 8th | 5 | Case-agnostic donor lift from `Akki-Executive-Core`. Three engine skeletons (`candidate_generation`, `tension_detector`, `reflection`) under `services/solva_v2/engines/`. Word-boundary negative-scan across `services/solva_v2/` for executive-domain tokens (ceo/cfo/cto/coo/boardroom/c-suite/non-executive director/chair notes/mckinsey/executive briefing/board-grade/corporate governance). HALTED constructs (DPO-S1 refusal categories, DPO-S2 LOCKED_QUESTIONS, sector-tag triangulation) absent as active code. Each engine module names its canon anchor; `reflection.run()` raises `NotImplementedError` with HALT message per DPO-S2. | `test_wsolvalift_cp_s8_donor_lift_case_agnostic.py` |
| Snapshot parity | +1 | 1 | `contracts/solva_reasoning.py` registered in `CONTRACT_TO_SNAPSHOT` (headline `SolvaTrace`). Five secondaries registered: `refusal_envelope`, `intent_audit_record`, `critic_invocation`, `critic_findings`, `load_bearing_set`. | `test_frozen_contract_snapshot_parity.py` |

## §B · Donor-lift summary — what lifted, what stripped, what HALTED

**Donor source**: `/app/assessment_workspace/repos/Akki-Executive-Core/backend/services/solva_v2/` (30+ Python files, executive-domain product).

**Lifted (structural pattern, case-agnostic form)**:
- Engine-step module structure — the case-agnostic English words `candidate_generation`, `tension_detector`, `reflection` for reasoning primitives named in Canon-4 §21 ("candidate weighing, tension surfacing"). Each is a minimal skeleton exposing `run()` and importing only from canon-grounded contracts.

**Stripped executive-domain tokens (negative-scan enforced by CP-S8, word-boundary)**:
- `ceo`, `cfo`, `cto`, `coo`, `boardroom`, `c-suite`, `c_suite`
- `non-executive director`, `non_executive_director`
- `chair notes`, `chair_notes`, `mckinsey`
- `executive briefing`, `board briefing`, `board grade`, `board-grade`, `corporate governance`

**HALTED (not lifted; owner ruling required for case-agnostic form)**:
- **DPO-S1 · Donor refusal categories** `{clean, jailbreak_attempt, out_of_scope, distress_flag, extraction_marker}` from `Akki-Executive-Core/backend/services/solva_v2/engines/refusal.py`. These are a DIFFERENT refusal shape from Canon-4 §24's three actions `{accept_as_stated, narrow_objective, lower_standard}`. Case-agnostic reconciliation is a design decision, not a token-strip. Canon-4 §24 adopted; donor shape not lifted.
- **DPO-S2 · Donor reflection `LOCKED_QUESTIONS`** from `Akki-Executive-Core/backend/services/solva_v2/engines/reflection.py`. Three specific questions about "diagnosis" (executive-domain vocabulary). Case-agnostic reflection question set requires re-authoring, not token-stripping. `engines/reflection.py::run()` raises `NotImplementedError` with a HALT message so the case-agnostic reflection contract cannot be silently substituted with domain-shaped content by a subsequent wave. Owner ruling requested to close.
- **DPO-S3 · Sector-tag triangulation** from `Akki-Executive-Core/backend/services/solva_v2/engines/triangulation.py`. Domain-specific (sector matching). Not lifted; no corresponding case-agnostic primitive in this wave.
- **LLM adapter proxy / probability weighting with LLM calls**. Cross-boundary integration outside this wave's platform-primitive scope; deferred.

**HALT raised at run-time**: one — `services/solva_v2/engines/reflection.py::run()`. This is a **structural HALT** (SO §3 no-silence): the primitive shape is preserved (input: tension pairs; output: load-bearing set), the implementation refuses to fabricate a domain answer, and the CP-S8 invariant `test_cp_s8_engine_modules_have_halt_or_canon_anchor` + `test_cp_s8_engines_expose_run_callable` both pass because `run()` exists and the module names its canon anchor and marks the HALT with the exact word "HALT" in its docstring and NotImplementedError message.

## §C · What was built

**Code (Commit A, `programme/track-a`)**:
- `backend/contracts/solva_reasoning.py` (new · 172 lines) — headline `SolvaTrace` + secondaries (`AssertionClass`, `UnitRef`, `LoadBearingSet`, `RefusalAction`, `RefusalEnvelope`, `IntentAuditRecord`, `CriticInvocation`, `CriticFindings`). R-C2 marker on `SolvaTrace`.
- `backend/services/solva_v2/__init__.py` (new · package)
- `backend/services/solva_v2/assertion_boundary.py` (new · CP-S2 mechanism — landed first)
- `backend/services/solva_v2/reasoning_faculty.py` (new · CP-S1 + CP-S3)
- `backend/services/solva_v2/trace.py` (new · CP-S5)
- `backend/services/solva_v2/intent_audit.py` (new · CP-S6)
- `backend/services/solva_v2/critic_seam.py` (new · CP-S7)
- `backend/services/solva_v2/engines/__init__.py` (new · CP-S8 package)
- `backend/services/solva_v2/engines/candidate_generation.py` (new · CP-S8 skeleton)
- `backend/services/solva_v2/engines/tension_detector.py` (new · CP-S8 skeleton)
- `backend/services/solva_v2/engines/reflection.py` (new · CP-S8 HALTED skeleton)
- 8 grounding-test files under `backend/tests/invariants/test_wsolvalift_*.py`
- `backend/tests/invariants/test_frozen_contract_snapshot_parity.py` (edit · +6 registrations for `solva_reasoning.py` headline + 5 secondaries)
- 6 new contract snapshot files under `backend/tests/invariants/*.contract_snapshot.json`
- `backend/tests/invariants/baseline_failures.json` — ratchet bump 3531→3562 + book-keeping fix (previous entry `new_floor` renamed to canonical `passed`) + new ratchet_history entry with canonical schema

**State (Commit B, `master`)**:
- `notes/W_SOLVA_V2_LIFT_grounding_brief.md` (new · wave open)
- `notes/W_SOLVA_V2_LIFT_close.md` (this file)
- `phase0/drill_receipts/20260913T104207Z_solva_v2_lift_RED_pre_impl.log`
- `phase0/drill_receipts/20260913T105216Z_solva_v2_lift_GREEN1_authoritative.log`
- `phase0/drill_receipts/20260913T105526Z_solva_v2_lift_GREEN2.log`
- `phase0/output_verified_seals/solva_v2_lift.seal.txt`

## §D · Honest limits (declared, SO §3 no-silence)

- **DPO-S1**: donor's refusal category set (`{clean, jailbreak_attempt, out_of_scope, distress_flag, extraction_marker}`) is a DIFFERENT refusal shape from Canon-4 §24. Adopted Canon-4 §24 three-action set; donor set not lifted.
- **DPO-S2 · run-time HALT**: `engines/reflection.py::run()` raises `NotImplementedError`. Case-agnostic reflection question set requires owner ruling to close. Structural pattern preserved; content refused.
- **DPO-S3**: no LLM binding this wave. Structural contracts + typed boundaries land; LLM adapter and real reasoning-content wiring is a subsequent wave's concern.
- **R-C1**: Solva reads floor and matrix through opaque handles per Canon-4 §23 "read-only" doctrine. No direct R-C1 dependency in this wave.
- **R-C2**: `SolvaTrace.au_3b_defensible=False` invariant-asserted. Silent flip when Doc-0 G-8 closes is forbidden.
- **Book-keeping fix in same commit**: previous wave's ratchet_history entry used non-canonical field `new_floor`; renamed to canonical `passed` to align with `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` schema. Same value (3531). No test outcome silently changed; the fix made a previously-failing manifest-monotonic test pass, which is why the pass count moved 3561→3562 with the schema alignment alone (+1 above the pure-Solva-CPs delta of +30).

## §E · Ratchet trace

- Wave opened at floor **3531** (post-W-REGISTRY-EXTENSION-G3).
- Mechanical RED at 28 right-reason failures (module-missing / file-missing), banked `20260913T104207Z_solva_v2_lift_RED_pre_impl.log`. 2 tests passed at RED time (they were negative-scans that trivially passed against empty rglob results — expected).
- GREEN #1 (authoritative, post-bump): **3562 passed, 1 skipped, 438 warnings in 111.39s** · `status: OK`.
- GREEN #2: **3562 passed, 1 skipped, 438 warnings in 112.27s** · `status: OK`.
- Byte-match on pass count: **TRUE (3562 · 3562)**.
- Ratchet bumped **3531 → 3562 (+31)** in `backend/tests/invariants/baseline_failures.json`.

## §F · Discipline held

- **BASELINE_GUARD=1** tests-first: RED banked before mechanism.
- **CP-S2 LANDED FIRST** per owner directive.
- **Double-green byte-match** at close.
- **`output_verified_seal Kind: solva_v2_lift`** written.
- **Two-commit pattern**: Commit A (code, `programme/track-a`) + Commit B (state, `master`). NEVER push.
- **testing_agent BANNED** — verification terminal pytest only.
- **No egress. No Radio traffic.** T4 / timezone / host-key verification still HELD for owner.
- **W-JOURNEY-ASSISTANT** stays out of scope.
- **W-DAP-STACK** stays gated behind this wave.
- **Prior-wave lineage untouched**: `W-REGISTRY-FULL-BUILD` (2026-09-09) and `W-REGISTRY-EXTENSION-G3` (2026-09-13) code, tests, seals, close manifests preserved verbatim.

## §G · What this wave does NOT open

- **W-DAP-STACK** — sequenced next per Phase C plan §D. Carries R-C1 and R-C2 at open; DAP-14 falls back to custody-class-only routing until Rules Service is built.
- **CP10 of prior `W-REGISTRY-FULL-BUILD`** — still on owner HOLD.
- **W-JOURNEY-ASSISTANT** — candidate wave; owner has not ruled in.
- **Case-agnostic reflection contract** — DPO-S2 HALT; owner ruling requested to close.
- **LLM binding for Solva engines** — deferred to subsequent wave.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
