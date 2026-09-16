READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M8-CROSS-TABLE-CONSISTENCY-CHECK · CP-M8-CTCC-1 · Grounding brief

**Wave:** W-M8-CROSS-TABLE-CONSISTENCY-CHECK (M8 catch-all P6 · SPRINT_PLAN.md 2026-09-06).
**CP:** CP-M8-CTCC-1 · Cross-Table Identifier Reconstruction refusal contract (case-agnostic · preventive).
**Track-a HEAD at open:** `2c7a8f0c`.
**Ratchet floor at open:** 4384.
**Milestone home:** M8 catch-all (per MILESTONE_STRUCTURE_REHOMED_20260915.md · rehomed 2026-09-15 from SPRINT_PLAN P6).

---

## §A · Owner ruling verbatim (this-shift authorization)

Owner directive 2026-09-16T~07:30Z verbatim:

> "Path A — build CP-M8-CTCC-1 (W-Cross-Table-Consistency-Check) now under full §3.3 protocol, then produce the M8 status rollup and hold with utilization interleave."

> "Your Lane-1/Lane-2 triage is accepted in full — good catches all three: the quarantine class being already-retired (from-disk truth beats my stale instruction; that's POST-2 discipline paying off again), TaskEval correctly blocked on Campaign-B settlement (owner scope), and the on-host watchdog deferral under SO §5 zero-perturbation during the live campaign (do NOT touch the GPU hosts' dispatch config until the 72h run completes; bank it as a chartered post-campaign operator action)."

Charter source (verbatim `STATE/SPRINT_PLAN.md:61-66`):

> "**W-Cross-Table-Consistency-Check** — for waves emitting multiple identifier-shaped columns.
> - Charter source: W-Multi-Table-Extract wave-honest-limit F.2 (cross-table PII correlation not checked when both columns excluded).
> - Scope: static + runtime check that no combination of emitted columns across tables can reconstruct an identifier.
> - Prerequisites: any wave emitting >1 identifier-shaped column from >1 table (preventive charter).
> - Outcome: refuses-unclassified-by-construction extends per-emitted-set, closing a theoretical cross-table leak channel.
> - Estimate: S (~250 LOC)."

---

## §B · Module architecture (case-agnostic thin-kernel)

**Home:** `services/governance_plane/cross_table_consistency.py` (composes with existing `governance_plane/retention_policy.py` sub-tree · NO new parallel package per POST-2 lesson).

**Export shape (5 primitives):**

1. `EmittedColumnRef` — frozen dataclass · 2 carriers exact order: `table_id: str · column_name: str`.
2. `IdentifierClass` — frozen dataclass · 2 carriers exact order: `class_id: str · columns_in_class: tuple[EmittedColumnRef, ...]`.
   - **Case-agnostic doctrine:** `class_id` is OPEN string (not Literal · not closed Enum · matches CP-M7-W1-POST-1 Resource Registry precedent per 2026-09-13 owner correction).
3. `assess_reconstruction_risk(*, emitted_columns, identifier_class_declarations) -> tuple[str, ...]` — pure data-in / data-out function. Returns tuple of `class_id`s at cross-table reconstruction risk. Empty tuple = safe. Deterministic sorted output.
4. `assert_no_cross_table_identifier_reconstruction(*, emitted_columns, identifier_class_declarations) -> None` — refusal wrapper. Raises `CrossTableIdentifierReconstructionRefused` when `assess_reconstruction_risk` returns non-empty.
5. `CrossTableIdentifierReconstructionRefused(Exception)` — refusal exception class.

**Reconstruction risk rule (verbatim):** an identifier class `ic` is at cross-table reconstruction risk iff the subset of `ic.columns_in_class` that appear in `emitted_columns` spans **more than one distinct `table_id`**. I.e., if `{c.table_id for c in ic.columns_in_class if c in emitted_set}` has cardinality ≥ 2, refuse.

**Static + runtime bindings.** Both wave-authoring-time (static, before emission spec finalises) and wave-emission-time (runtime, before actual emission fires) callers use `assert_no_cross_table_identifier_reconstruction(...)`. The check is data-in / data-out; the caller decides *when* to invoke.

---

## §C · Case-agnostic doctrine

Per owner correction 2026-09-13 (banked in DECISIONS.md · re-cited at CP-M7-W1-POST-1 close · CP-M7-W1-POST-3 verified 0 domain tokens across W1b modules):

- Zero closed enums on identifier-class discriminator.
- Zero domain tokens (`asr` · `audio` · `transcript` · `diarization` · `nas` · `obs` · `mysql` · `harvest`) in module source or docstring examples.
- Zero imports of dispatch surfaces (`training_runner` · `runner` · `ssh_seam` · `run_queue` · `audio_poc.hf_transcribe` · `campaign_infra.production_trainer`).
- Zero refuse_dispatch / kill_ / terminate_ / unregister on public surface.

**Verified negatively via invariants** (grep-based tests in the test file).

---

## §D · Test invariants (tests-first · ~14 items)

Test file: `backend/tests/invariants/test_wm8_ctcc_1_cross_table_consistency.py`.

1. `test_module_fabric_present` — module + all 5 exports importable from `services.governance_plane.cross_table_consistency`.
2. `test_module_re_exported_from_package` — 5 exports available from `services.governance_plane`.
3. `test_emitted_column_ref_frozen_two_carrier_exact_order` — `EmittedColumnRef` is `@dataclass(frozen=True)` · fields in exact order `(table_id, column_name)`.
4. `test_identifier_class_frozen_two_carrier_exact_order` — `IdentifierClass` is `@dataclass(frozen=True)` · fields in exact order `(class_id, columns_in_class)` · `columns_in_class` type is `tuple[EmittedColumnRef, ...]`.
5. `test_class_id_is_open_string_not_closed_enum` — inspection: `IdentifierClass.class_id` annotation is `str` · not a Literal · not a closed Enum.
6. `test_assess_risk_empty_emissions_returns_empty` — empty `emitted_columns` yields empty risk tuple.
7. `test_assess_risk_empty_identifier_classes_returns_empty` — empty `identifier_class_declarations` yields empty risk tuple.
8. `test_assess_risk_single_table_single_class_returns_empty` — 1 table · 1 class · safe.
9. `test_assess_risk_two_tables_disjoint_classes_returns_empty` — 2 tables · classes covering only within-table columns · safe.
10. `test_assess_risk_two_tables_shared_class_returns_class_id` — 2 tables · shared identifier class with columns from both tables · returns that class_id.
11. `test_assess_risk_three_tables_two_shared_classes_returns_sorted_tuple` — determinism · sorted tuple returned.
12. `test_assert_no_cross_table_reconstruction_raises_on_risk` — refusal path fires `CrossTableIdentifierReconstructionRefused`.
13. `test_assert_no_cross_table_reconstruction_silent_when_safe` — non-refusal path returns None.
14. `test_case_agnostic_zero_domain_tokens_in_module_source` — grep negative: 0 hits for `asr|audio|transcript|diarization|nas|obs|mysql|harvest` in module source.
15. `test_module_no_banned_enforcement_tokens_on_public_surface` — grep negative: 0 hits for `def kill|def terminate|def refuse_dispatch|def unregister`.
16. `test_module_zero_imports_of_dispatch_surfaces` — grep negative: 0 `import` or `from` lines referencing dispatch surfaces.

Total: **16 invariants**. Target ratchet bump 4384 → **4400** (+16 · no cross-benefit expected).

---

## §E · Wave-honest limits

- **D.1** Preventive charter · zero triggering wave has landed yet. Contract lands as shape-frozen refusal; runtime enforcement fires only when a caller invokes `assert_no_cross_table_identifier_reconstruction(...)` from within an actual multi-table emission wave. This is a preventive contract, not a global gate.
- **D.2** Reconstruction rule is **coarse** (cardinality of contributing table_ids). It does NOT reason about statistical linkability, k-anonymity, or entropy. A stricter rule (e.g. cross-column mutual information) is a chartered-forward refinement.
- **D.3** `EmittedColumnRef` uses `(table_id, column_name)` as opaque strings. There is no `column_type` or `column_schema` carrier — matching contributing columns to an identifier class is the caller's declared responsibility, not inferred here.
- **D.4** No I/O · no logging · pure data-in / data-out. Composes cleanly with any dispatch surface without coupling.

---

## §F · Commit protocol (§3.3 3-commit pattern)

- **Commit A (code):** `programme/track-a` in `repos/Extraction-Akki/` — mechanism (`services/governance_plane/cross_table_consistency.py`) + tests (`tests/invariants/test_wm8_ctcc_1_cross_table_consistency.py`) + `__init__.py` export update + `baseline_failures.json` ratchet bump (4384 → 4400 target).
- **Commit B (state):** `master` in `/app/assessment_workspace/` — this grounding brief + RED drill receipt + GREEN1/GREEN2 receipts + seal file (Track-a HEAD = Commit-A SHA · Master HEAD = TBD) + close note + DECISIONS entry + NEXT pin + GPU util check-in artefacts.
- **Commit C (fixup):** `master` — replace `Master HEAD: TBD` in seal file + DECISIONS + NEXT with the actual Commit-B SHA.

**No push. Local commits only.** Owner Clarification 1 (2026-08-14) verbatim.

**GPU util interleave at CP-M8-CTCC-1 seal:** fire `check_in` between RED drill and GREEN1 (workload continuity) + at seal boundary (post-Commit-B). Both check-ins bank telemetry+workload jsonl to state repo.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
