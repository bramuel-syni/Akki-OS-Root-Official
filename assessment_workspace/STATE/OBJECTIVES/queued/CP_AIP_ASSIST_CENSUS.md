---
card_id: CP_AIP_ASSIST_CENSUS
title: Census Assistant · objective-shape-and-evolve dialogue as first-class Census Autonomy Service behavior · §1.2 extension of sealed CP-AIP-6 Objective Wizard agent interface + Census Autonomy conversational surface
ratified_at_utc: 2026-02-23T10:35:00Z
ratified_by: Owner Standing Directive 1 (2026-02-23) verbatim: "This is the work of the assistants in census and training. Card two objectives (on-ledger, owner-directed, not PARKED): CP-AIP-ASSIST-CENSUS and CP-AIP-ASSIST-TRAINING."
card_sha256: DRAFT-PENDING-COMMIT-B
milestone_status: DRAFT (owner-directed · not PARKED · on active ledger · card draft banked at CP-AIP-9 boundary for review in CP-AIP-10 REPORT-AND-CONTINUE · ratification then build)
---

# CP-AIP-ASSIST-CENSUS — Census Assistant

## OBJECTIVE

Extend (§1.2 modality-extension, NOT parallel) the sealed CP-AIP-6 Objective Wizard agent interface + sealed Census Autonomy conversational surface (Phase 3 A''/A'''/A'''' chain: `services.census_autonomy.response_required_queue` + `data_source_adapter` + `producer_bridge` + `portal_census_autonomy_producer` router) into a **Census Assistant** that conducts the shape-and-evolve dialogue with tenant/owner as **first-class Census Autonomy Service behavior**.

The assistant runs **inside Akki autonomy** (not the E1 pod) per Ruling (b) 2026-02-23: proposes census scope options with rationale, refines against tenant custody + data-source availability + budget constraints, records each turn as a one-record receipted ledger entry, carries **§6.9 markers** (unmeasured / INFERRED / honest-gap) rather than refusing where a marker makes the state honest, and re-derives the census objective as new leads land (e.g., the na7p4 cost lead, the Newvault pairing, the google-transcripts corpus).

`canon_ref: AIP v1.0 §1.2 modality-extension + §8 Objective Wizard + §9 Collection Schema + §12.1 Registry Namespace + §1.5 unrepresentable-not-policed + SO §6.9 desk discipline + Ruling (b) 2026-02-23 verbatim + Standing Directive 1 2026-02-23 verbatim.`

**Extends sealed carriers (unchanged per SO §3.8):**
- `services.wizard.objective_compile.compile_target_outcome` + `compile_collection_schema` (CP-AIP-6 · sealed)
- `services.census_autonomy.response_required_queue.bank_response_required_item` (Phase 3 A''' · sealed)
- `services.census_autonomy.data_source_adapter.route_asset_registry_write` (Phase 3 A'''' · sealed)
- `services.census_autonomy.producer_bridge` (Phase 3 A''''-cont-A · sealed)
- `routers.portal_census_autonomy_producer` (Phase 3 A''''-cont-A · sealed)

## MUST DO

1. **Assistant-turn record shape (frozen carrier)** — every dialogue turn is stored as a `CensusAssistantTurn_v0` frozen record: `{turn_id · session_id · tenant_id · role: 'assistant' | 'owner' · content · proposed_objective_delta · rationale · markers_carried: [] · superseded_by: turn_id | None · created_at_utc}`. Additive alongside sealed `ObjectiveSession_v0` (CP-AIP-6).
2. **Proposal-without-rationale refused** — an assistant turn with `role='assistant'` and a `proposed_objective_delta` but empty `rationale` MUST raise `ProposalWithoutRationaleRefused`. Enforced by RED-first invariant.
3. **Evolved-objective supersedes-additively (nothing relabelled/rewritten)** — a turn's `superseded_by` points to a NEW turn ID; the superseded turn record is **NEVER edited**. Enforced by structural check + append-only ledger.
4. **Markers-over-refusal per §6.9** — where a canon marker (unmeasured / INFERRED / honest-gap / fallback) makes the state honest, the assistant emits the marker and the dialogue continues; refusal reserved for cases where a marker cannot make the state honest. Enforced by structural invariant scanning the assistant module for refusal calls that lack a `marker_alternative_considered` annotation.
5. **Autonomy-wiring per Ruling (b)** — the assistant registers itself as a **Census Autonomy Service job** (via `routers.portal_census_autonomy_producer` + `producer_bridge`), so the running Akki system schedules and executes assistant turns autonomously. E1's role ends at the wiring; execution is Akki-side.
6. **Objective-shape-and-evolve dialogue closure** — the assistant re-derives the census objective when a new lead lands (e.g., a data-source producer job banks a new artifact via `bank_response_required_item`). The re-derivation is a NEW `CensusAssistantTurn_v0` with `proposed_objective_delta` referencing the new lead.
7. **RED-first pins (planned; not yet written):**
   - `test_census_assistant_proposal_without_rationale_refused`
   - `test_census_assistant_evolved_objective_supersedes_additively_never_relabels`
   - `test_census_assistant_marker_over_refusal_enforced_structurally`
   - `test_census_assistant_registers_as_census_autonomy_service_job`
   - `test_census_assistant_turn_record_frozen_shape`
   - `test_census_assistant_re_derives_objective_on_new_lead`
   - `test_census_assistant_extends_not_parallels_sealed_wizard_compile_boundary`
   - `test_new_module_carries_assistant_v1_posture_marker_citing_standing_directive_1_verbatim`

## MUST NOT

- Edit any sealed CP-AIP-6 wizard carrier or sealed Census Autonomy Service carrier.
- Run the assistant inside the E1 pod. `Ruling (b) verbatim: E1 to wire it into Akki's autonomy so Akki runs it, then step back.`
- Relabel or rewrite historical assistant turns. `Standing Directive 1 verbatim: evolved objective supersedes additively; nothing relabelled/rewritten.`
- Refuse where a §6.9 marker makes the state honest.
- Sprawl beyond the ledger item.

## EXIT

**RED-first invariants (8 planned):** all listed under MUST DO §7 above; specific test node IDs finalize at slice authorship.

**Autonomy-pickup receipt as exit evidence** — a receipt from the Akki autonomy engine's run log showing it scheduled and executed at least one assistant turn on its own cadence.

## STOP

Stop at owner ratification of this draft card (in CP-AIP-10 REPORT-AND-CONTINUE report). If ratified, build after SO-6.9 wave completes.

If a SPEC-CONFLICT is discovered between this card and sealed CP-AIP-6 wizard / sealed Census Autonomy Service primitives / AIP v1.0 §1.2 modality-extension discipline, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report immediately.

## ANCHORS

- **Owner Ruling (b) verbatim (2026-02-23):** 'E1 to wire it into Akki's autonomy so Akki runs it, then step back.'
- **Standing Directive 1 verbatim (2026-02-23):** 'note the natural back and forth you and i are having when shaping the objectives and evolving it both for training and census. This is the work of the assistants in census and training.'
- **Owner drop verbatim (2026-02-23):** `STATE/OWNER_DROPS/ruling_b_akki_runs_it_plus_standing_directives_20260223/DROP.md` §1-3.
- **Sealed carriers extended (unchanged):** listed under OBJECTIVE above.
- **Standing Orders:** SO §3 RED-first · SO §3.8 additive-only · SO §6.2 objective-card + hash-pin · SO §6.9 desk discipline (markers-over-refusal + one-sentence protected-objective on every refusal/hold/gate) · SO §7 17-guard consolidated set.
- **Ledger check:** this card owner-directs `CP-AIP-ASSIST-CENSUS` and nothing else. Build sequenced after SO-6.9 wave.
