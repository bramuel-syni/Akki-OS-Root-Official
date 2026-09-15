# M6 · Sub-wave 6 · W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA — Grounding brief

**Opened at UTC:** 2026-09-15T~21:35Z
**Milestone:** M6 · Audio-Plane v1.0 · Sub-wave 6 of ~10
**Prior sub-wave sealed:** Sub-wave 5 (W-M6-CLUSTERING-HUMAN-VALIDATION) · 3 CPs · +27 invariants · ratchet 4213 → 4240 · fully sealed under §3.3 3-commit pattern (see `notes/W_M6_CLUSTERING_HUMAN_VALIDATION_close.md`).
**Baseline ratchet floor at open:** 4240 · `counts_at_baseline.passed=4240` · `passed_floor=4240` (fields match per SO §1).
**Track-a HEAD at open:** `62e5a1d` · **Master HEAD at open:** `ccb161ab`.

---

## §A · Owner ruling (verbatim, banked 2026-09-15T~21:25Z in `STATE/DECISIONS.md`)

> "GO — open sub-wave 6 (W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA, §8 + §9 + §12.1, N7 fold-in): author the grounding brief with verbatim anchors, then walk the CPs tests-first under §3.3, autonomously.
>
> Steer on your recommendations:
> 1. Rec 1 RATIFIED — wire assert_cluster_carries_no_human_name into sub-wave 6's objective→cluster write path as a mandatory gate, not a downstream check. Make it an explicit invariant in the sub-wave 6 brief.
> 2. Rec 2 — escalated to the owner again (49 timeouts / 17h since ratification is definitive). Keep the every-CP probe loop; not blocking sub-wave 6.
> 3. Rec 3 RATIFIED as a small single-CP addition — the ratified-vs-INFERRED backend registry surface. Home it wherever cleanest: appended CP at sub-wave 6 close or an M8 mini-wave; your call, keep it tight (~+6-8 invariants). It becomes the M6-seal story's 'what is truly live' table.
>
> Discipline notes accepted: the ValidatedStratum value-equality fill and the fifth leak-vocabulary attribute were exactly right; HUMAN_NAME_ATTRIBUTE_NAMES stays owner-extendable. HALT boundary unchanged (synthetic fixtures only; real voice/biometric material halts to owner — §7 voice verification territory especially). Report at sub-wave 6 seal or genuine HALT."

---

## §B · Verbatim canon anchors (source of truth — no paraphrase)

**Source:** `notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md` (Audio-Plane v1.0 verbatim requirements register · authored 2026-09-14) + `notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:98` (N7 verbatim).

### §B.1 · §8 The Objective Wizard — Schema Compiler (P123..P145)

- **V78 · §8.1 P125** (elicitation-hand-write-refusal): *"No business user hand-writes a Target Outcome. The Objective Wizard — a new variant of the existing shaping wizard, reusing its agent interface, guards, session persistence, and ledger sidecar — elicits an objective in plain language and compiles two governed artifacts:"*
- **V79 · §8.1 P126** (output 1): *"TargetOutcome (§10) — handed to the Training Planner."*
- **V80 · §8.1 P127** (output 2): *"Collection Schema (§9) — the data dictionary for this objective: which data points are extracted from the sound, at what granularity, at what quality bar."*
- **V81 · §8.2 P129** (elicit carrier 1): *"The question the model must answer — operational and falsifiable."*
- **V82 · §8.2 P130** (elicit carrier 2 · unresolved → census): *"The population — resolved against existing register strata; unresolved populations are flagged as unmeasured and generate census work."*
- **V83 · §8.2 P131** (elicit carrier 3): *"The acceptance bar — per stratum, two-dimensional (§10), with the gate-or-document decision recorded explicitly."*
- **V84 · §8.2 P132** (elicit carrier 4 · price-before-commission): *"The collection consequences — the wizard derives required columns, shows which are already collected (baseline tier), which exist but are uncollected, and the cost of collecting them. The owner sees the price of the schema before commissioning."*
- **V85 · §8.3 P134** (propose): *"Propose. The agent side may propose novel data points no prior objective collected. This is where innovation enters."*
- **V86 · §8.3 P135** (qualify): *"Qualify. A proposed column never enters collection directly. It is admitted as a candidate: collected on a sample only, its evidence of value measured against the objective — the same qualification path any fact travels."*
- **V87 · §8.3 P136** (graduate · ceremony-governed): *"Graduate. Qualified candidates graduate into the objective tier for that commission. Graduation into the baseline tier is ceremony-governed (proposal, countersignature, waiting period), because a baseline column is paid on every hour ingested for the life of the estate."*
- **V88 · §8.3 P137** (deterministic compile · mechanical-guards-before-LLM): *"The compile stage is deterministic throughout: the agent proposes; only qualified columns compile. Mechanical guards prove against a stub agent before any LLM is plugged in, per the existing standing disposition."*
- **V89 · §8.4 P139** (compile-time rejection preamble): *"The wizard cannot emit an artifact the downstream contracts would refuse. Rejected at compile, not warned:"*
- **V90 · §8.4 P140** (rejection 1 — test_set_ref): *"An Outcome without an existing test_set_ref."*
- **V91 · §8.4 P141** (rejection 2 — per-stratum dimension): *"An acceptance bar missing the per-stratum dimension."*
- **V92 · §8.4 P142** (rejection 3 — §6.2 custody): *"A Collection Schema requiring a column whose capture violates the custody conditions of §6.2."*
- **V93 · §8.5 P144** (turn-ledger stamping · options-considered-and-rejected · Targeta handoff): *"Every session stamps to the ledger via the existing turn-ledger pattern under a distinct data class (objective_session), including options considered and rejected — which is what makes a later 'why was the model built this way' answerable. Compiled artifacts hand off to Targeta through the existing admission-handoff pattern. Objective → schema → plan → run is one provenance chain."*
- **V94 · §8.5 P145** [VERIFY]: *"[VERIFY] The B-2/B-3 landing state of the current wizard, before choosing between extending the existing state machine with an objective variant or standing up a sibling machine sharing the agent interface and ledger sidecar."*

### §B.2 · §9 The Collection Schema (P146..P152)

- **V95 · §9.1 P148** (definition): *"The declared data dictionary of a commission: what is extracted from the sound, for what purpose, at what quality bar. It is the admission standard of the audio estate, per objective (§1.1). It has two tiers."*
- **V96 · §9.2 P150** (baseline tier · v1.0 five-item content set · seam-governed changes): *"Standing, objective-independent, collected at first ingestion for all admitted material. Membership criterion: cheap to collect now, unaffordable to collect later. Contents at v1.0: language identification, code-switch points, condition profile, dedup instance condition map, synthesis-relevant group-level acoustics (§4). Changes to the baseline are seam-governed — ceremony, countersignature, waiting period — because silently narrowing the baseline is how an estate quietly becomes unre-readable."*
- **V97 · §9.3 P152** (objective tier · priced-before-collection · candidates through §8.3 only): *"Declared per commission by the Objective Wizard. Collected against material already in governed scope, priced before collection starts, recorded in the commission's registry namespace. Candidate columns enter through propose–qualify–graduate (§8.3) only."*

### §B.3 · §12.1 Record and Registry Integration — per-commission scoped namespace (P195)

- **V121 · §12.1 P195** (per-commission namespace · declared-but-not-yet-collected first-class · sealed-not-deleted): *"Per commission, a scoped namespace within the registry holds: the Collection Schema (versioned), collected data points mapped against it — with declared-but-not-yet-collected as first-class state — the strata referenced by the Outcome, and coverage state per stratum. Reads compose with the global registry; writes are namespace-scoped. On close, the namespace is sealed, not deleted: it is the record of what was collected and why, and the next objective's wizard session queries prior schemas and coverage so the second project starts from the first project's map."*

### §B.4 · N7 fold-in (verbatim from drift audit line 98)

> **N7** (v1.0 §8.4 P139..P142 · `AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:98` · `[VERIFY]` status per §16.1 P245): *"The wizard cannot emit an artifact the downstream contracts would refuse. Rejected at compile, not warned: An Outcome without an existing test_set_ref. An acceptance bar missing the per-stratum dimension. A Collection Schema requiring a column whose capture violates the custody conditions of §6.2."*

**N7 is `[VERIFY]` (partial · needs verify).** The Objective Wizard exists at B-2/B-3 stage per prior notes (§8.5 P145). Sub-wave 6 anchors N7 in mechanism-and-test terms. The B-2/B-3 landing state verification per V94 is a `DEFAULT-PENDING-OVERRIDE` — sub-wave 6 builds the compile-refusal mechanism as a standalone contract (does NOT extend the existing wizard state machine); owner may later re-home it into the existing wizard per V94 disposition without breaking the compile-refusal invariants.

---

## §C · Sub-wave 6 CP breakdown (4 CPs · §3.3 3-commit pattern each)

### CP-M6-6-1 · Objective Wizard audio-variant compile-refusal + Rec-1-M6SW6 gate (N7 fold-in · §8.4 P139..P142)

**Discharge:** §8.4 P139 preamble + P140..P142 three refusals as first-class mechanism, plus Rec-1-M6SW6 mandatory §5.3-clause-2 write-path gate.

**Public API target (`services/audio_plane_v1/objective_wizard.py`):**
- `TargetOutcomeStub` — frozen 3-carrier: `outcome_id` · `test_set_ref: Optional[str]` · `acceptance_bar` (dict-like or None).  Deliberately a STUB (not the full §10 TargetOutcome) — sub-wave 6 owns compile-refusal territory only; full §10 lands at sub-wave 7 CP-M6-7-1.
- `AcceptanceBar` — frozen 2-carrier: `has_per_stratum_dimension: bool` · `per_stratum_thresholds: Tuple[Tuple[str, float, float], ...]` (stratum_id · accuracy · coverage; empty tuple when `has_per_stratum_dimension=False`).
- `CollectionSchemaColumnStub` — frozen 3-carrier: `column_name: str` · `captures_custody_violating_field: bool` · `bound_cluster: Optional[Any]` (the cluster carrier the column binds to; None when unbound).  Custody-violating column marker deliberately explicit — sub-wave 6 does NOT re-import §6.2 conditions here (no refactor; CP-M6-3-3 remains the source of truth); a downstream CP wire may promote this to a live §6.2 check without breaking the sub-wave 6 contract.
- `compile_objective_artifact(*, outcome, columns) -> None` — refuses at compile with one of four errors:
  1. `TargetOutcomeMissingTestSetRefError` — refuses V90 (P140) verbatim: *"An Outcome without an existing test_set_ref."*
  2. `AcceptanceBarMissingPerStratumDimensionError` — refuses V91 (P141) verbatim: *"An acceptance bar missing the per-stratum dimension."*
  3. `CollectionSchemaCustodyViolationError` — refuses V92 (P142) verbatim: *"A Collection Schema requiring a column whose capture violates the custody conditions of §6.2."*
  4. **[Rec-1-M6SW6 mandatory gate]** `CollectionSchemaClusterHumanNameLeakError` — refuses when any column's `bound_cluster` (if non-None) fails `assert_cluster_carries_no_human_name` from `services.audio_plane_v1.cluster_stability`.  This is a WRITE-PATH invariant: any objective→cluster binding is refused at compile if the cluster carrier surfaces a human-readable name.  The Objective Wizard cannot emit an artifact whose downstream data-plane contracts would surface a human-readable cluster name.  Owner ruling 2026-09-15T~21:25Z RATIFIED.

**Refusal ordering (P036 receipt-before-result carrier discipline):** test_set_ref → per_stratum_dimension → custody_violation → [Rec-1-M6SW6] cluster_human_name_leak.  First refusal wins; no partial success.

**Invariants (target: ~10):**
1. Module fabric: 8 public exports.
2. `compile_objective_artifact` passes silently on well-formed input (test_set_ref present · per-stratum acceptance · no custody-violating columns · all bound_cluster carriers pass §5.3 clause 2 gate).
3. Refuses V90 (test_set_ref absent) — verbatim quote in docstring.
4. Refuses V91 (per-stratum dimension absent) — verbatim quote in docstring.
5. Refuses V92 (custody-violation column) — verbatim quote in docstring.
6. Refuses Rec-1-M6SW6 (bound_cluster carries `human_name` non-None) — verbatim owner ruling quote in docstring.
7. Refuses Rec-1-M6SW6 on all 5 leak-vocabulary attributes (parametric over `HUMAN_NAME_ATTRIBUTE_NAMES`).
8. Refusal ordering P036-preserved (test_set_ref beats other refusals when multiple violations present).
9. Bound_cluster None (unbound column) passes the Rec-1-M6SW6 gate (unbound is legitimate at qualify/graduate stage).
10. Frozen dataclass discipline: all four carrier classes reject mutation with `dataclasses.FrozenInstanceError`.

**No-refactor:** cluster_stability.py + character_register.py + all sub-wave 1..5 modules untouched.

---

### CP-M6-6-2 · Collection Schema type (§9 P148..P152 · baseline tier + objective tier)

**Discharge:** §9.1 P148 definition + §9.2 P150 baseline tier + §9.3 P152 objective tier as frozen carriers.

**Public API target (`services/audio_plane_v1/collection_schema.py`):**
- `BASELINE_TIER_CONTENTS_V1_0` — frozen 5-tuple (v1.0 P150 verbatim in canonical order): `("language_identification", "code_switch_points", "condition_profile", "dedup_instance_condition_map", "synthesis_relevant_group_level_acoustics")`.  Changes require ceremony (§9.2 P150 verbatim discipline) — enforced by making the constant a module-level frozen tuple, extension only via owner-authored code change.
- `SCHEMA_TIER_VALUES` — frozenset `{"baseline", "objective"}` (§9.1 P148 verbatim two-tier).
- `CollectionSchemaColumn` — frozen 4-carrier: `column_name: str` · `tier: str` (∈ SCHEMA_TIER_VALUES) · `quality_bar: str` · `provenance_ref: Optional[str]` (points to propose–qualify–graduate ceremony for objective-tier columns; None allowed for baseline-tier).  Refuses invalid tier at `__post_init__`.
- `CollectionSchema` — frozen 3-carrier: `schema_id: str` · `commission_id: str` · `columns: Tuple[CollectionSchemaColumn, ...]`.  Baseline-tier columns MUST include all 5 v1.0 contents (§9.2 P150 verbatim); enforced at `__post_init__`.
- `construct_collection_schema(*, schema_id, commission_id, columns) -> CollectionSchema` — refuses:
  1. `SchemaTierInvalidError` on tier outside SCHEMA_TIER_VALUES.
  2. `BaselineTierIncompleteError` if any of the 5 v1.0 baseline contents is missing.
  3. `ObjectiveTierProvenanceMissingError` if any objective-tier column has None provenance_ref (§9.3 P152 verbatim: candidates enter through propose–qualify–graduate ONLY).

**Invariants (target: ~9):**
1. Module fabric: 7 public exports.
2. `BASELINE_TIER_CONTENTS_V1_0` is a frozen 5-tuple in verbatim canonical order.
3. `SCHEMA_TIER_VALUES` is verbatim frozenset {baseline, objective}.
4. `CollectionSchemaColumn` refuses invalid tier at `__post_init__`.
5. `construct_collection_schema` passes on well-formed input (5 baseline + 0..N objective with provenance).
6. Refuses `BaselineTierIncompleteError` when any of 5 v1.0 baseline contents is missing.
7. Refuses `ObjectiveTierProvenanceMissingError` when objective-tier column has None provenance_ref.
8. Frozen dataclass discipline: all mutation-refusal contracts.
9. `CollectionSchema.columns` is a tuple (immutable) — Sequence input coerced.

**No-refactor:** CP-M6-6-1 objective_wizard.py unchanged.  Composition-only: CP-M6-6-1's `CollectionSchemaColumnStub` remains a STUB for compile-refusal territory; CP-M6-6-2's `CollectionSchemaColumn` is the full §9 carrier for downstream data-plane use.  Distinct types by design (compile refuses stub-level violations; downstream data-plane uses full type).

---

### CP-M6-6-3 · Registry namespace per §12.1 P195 (per-commission scoped namespace · sealed-not-deleted)

**Discharge:** §12.1 P195 verbatim per-commission scoped namespace + declared-but-not-yet-collected as first-class + sealed-not-deleted on close.

**Public API target (`services/audio_plane_v1/commission_registry_namespace.py`):**
- `NAMESPACE_STATE_VALUES` — frozenset `{"open", "sealed"}`.
- `COLUMN_COLLECTION_STATE_VALUES` — frozenset `{"declared_not_yet_collected", "collected"}` (§12.1 P195 verbatim: "declared-but-not-yet-collected as first-class state").
- `NamespaceColumnEntry` — frozen 3-carrier: `column_ref: str` · `collection_state: str` (∈ COLUMN_COLLECTION_STATE_VALUES) · `coverage_metric: Optional[float]` (per-stratum coverage; None when not yet collected).
- `NamespaceStratumCoverageEntry` — frozen 2-carrier: `stratum_id: str` · `coverage_state: str`.
- `CommissionRegistryNamespace` — frozen 6-carrier: `commission_id: str` · `state: str` (∈ NAMESPACE_STATE_VALUES) · `collection_schema_versioned_ref: str` · `column_entries: Tuple[NamespaceColumnEntry, ...]` · `stratum_coverage_entries: Tuple[NamespaceStratumCoverageEntry, ...]` · `sealed_at_utc: Optional[str]` (ISO-8601; None when open).
- `open_namespace(*, commission_id, collection_schema_versioned_ref, ...) -> CommissionRegistryNamespace` — constructs a namespace in state `"open"` with empty entries.
- `record_declared_column(*, namespace, column_ref) -> CommissionRegistryNamespace` — appends a `declared_not_yet_collected` entry to a `"open"` namespace.  Refuses `NamespaceSealedError` on sealed namespace.
- `record_column_collected(*, namespace, column_ref, coverage_metric) -> CommissionRegistryNamespace` — flips a declared entry to `collected` with coverage metric.  Refuses `NamespaceColumnUnknownError` on unknown column_ref.  Refuses `NamespaceSealedError` on sealed namespace.
- `seal_namespace(*, namespace, sealed_at_utc) -> CommissionRegistryNamespace` — flips state to `"sealed"`, records `sealed_at_utc`.  Refuses `NamespaceAlreadySealedError` on already-sealed namespace.
- `NamespaceSealedError` · `NamespaceAlreadySealedError` · `NamespaceColumnUnknownError` · `NamespaceStateInvalidError` · `ColumnCollectionStateInvalidError`.

**§12.1 sealed-not-deleted invariant:** a sealed namespace's `column_entries` and `stratum_coverage_entries` are **preserved** (frozen dataclass immutability guarantees this).  The sealed namespace remains queryable by the next objective's wizard session.

**Invariants (target: ~11):**
1. Module fabric: ~12 public exports.
2. `NAMESPACE_STATE_VALUES` verbatim frozenset {open, sealed}.
3. `COLUMN_COLLECTION_STATE_VALUES` verbatim frozenset {declared_not_yet_collected, collected}.
4. `open_namespace` returns state=`"open"`, sealed_at_utc=None.
5. `record_declared_column` on open namespace appends entry with state=`"declared_not_yet_collected"`, coverage_metric=None.
6. `record_column_collected` on open namespace flips entry to state=`"collected"`, records coverage_metric.
7. `record_declared_column` refuses `NamespaceSealedError` on sealed namespace.
8. `record_column_collected` refuses `NamespaceSealedError` on sealed namespace.
9. `record_column_collected` refuses `NamespaceColumnUnknownError` on unknown column_ref.
10. `seal_namespace` refuses `NamespaceAlreadySealedError` on already-sealed namespace.
11. Sealed-not-deleted: after `seal_namespace`, `column_entries` and `stratum_coverage_entries` remain populated (queryable by next-objective wizard).

**No-refactor:** CP-M6-6-1 objective_wizard.py + CP-M6-6-2 collection_schema.py both unchanged.

---

### CP-M6-6-4 · Rec-3-M6SW6 · Ratified-vs-INFERRED backend registry surface (CLOSES SUB-WAVE 6)

**Discharge:** owner ruling 2026-09-15T~21:25Z RATIFIED — homed as appended CP at sub-wave 6 close (agent's call per owner delegation).  Rationale: (a) directly composes with CP-M6-1-1..1-4 audio-plane pluggable seams + CP-M6-5-1 ClusteringBackend — the exact set the registry surfaces; (b) produces the M6-seal-story "what is truly live" table WITHOUT delaying M6-seal narrative behind a separate M8 mini-wave; (c) sub-wave 6 already touches registry-namespace territory (§12.1 P195), so the second registry-shape surface composes naturally.

**Public API target (`services/audio_plane_v1/backend_registry.py`):**
- `BACKEND_RATIFICATION_STATES` — frozenset `{"ratified", "inferred_pending_ratification"}` (matches D10 pluggable-seam discipline vocabulary).
- `RegisteredBackendEntry` — frozen 5-carrier: `seam_name: str` · `backend_name: str` · `ratification_state: str` (∈ BACKEND_RATIFICATION_STATES) · `canon_anchor: str` (verbatim canon quote or anchor ref) · `ratified_at_utc: Optional[str]` (ISO-8601 when ratified; None when inferred_pending_ratification).
- `BackendRegistrySurface` — frozen 1-carrier: `entries: Tuple[RegisteredBackendEntry, ...]`.  Case-agnostic: no coupling to any specific pluggable seam class.
- `register_backend(*, registry, seam_name, backend_name, ratification_state, canon_anchor, ratified_at_utc=None) -> BackendRegistrySurface` — appends an entry.  Refuses `BackendRatificationStateInvalidError` on invalid state.  Refuses `BackendRatifiedButMissingRatifiedAtError` when `ratification_state="ratified"` but `ratified_at_utc=None`.
- `list_ratified_backends(*, registry) -> Tuple[RegisteredBackendEntry, ...]` — filters to `ratification_state="ratified"` entries.  Provenance for M6-seal-story "what is truly live" table.
- `list_inferred_backends(*, registry) -> Tuple[RegisteredBackendEntry, ...]` — filters to `ratification_state="inferred_pending_ratification"` entries.  Provenance for M6-seal-story "pending owner ratification" table.
- `assert_seam_has_ratified_backend(*, registry, seam_name) -> None` — refuses `SeamHasNoRatifiedBackendError` when no ratified backend is registered for the seam.  Load-bearing gate for future live-invocation paths.
- `BackendRatificationStateInvalidError` · `BackendRatifiedButMissingRatifiedAtError` · `SeamHasNoRatifiedBackendError`.

**Owner-set ceiling:** ≤ +8 invariants (per owner ruling "keep it tight ~+6-8 invariants").

**Invariants (target: 6-8):**
1. Module fabric: ~8 public exports.
2. `BACKEND_RATIFICATION_STATES` verbatim frozenset {ratified, inferred_pending_ratification}.
3. `register_backend` refuses `BackendRatificationStateInvalidError` on invalid state (e.g. "approved", "pending").
4. `register_backend` refuses `BackendRatifiedButMissingRatifiedAtError` when ratified without timestamp.
5. `register_backend` passes on ratified backend with ISO-8601 timestamp.
6. `register_backend` passes on inferred_pending_ratification backend with None timestamp.
7. `list_ratified_backends` returns only ratified entries in insertion order.
8. `list_inferred_backends` returns only inferred entries in insertion order.
9. `assert_seam_has_ratified_backend` refuses `SeamHasNoRatifiedBackendError` on seam with no ratified backend (only inferred backends).
10. `assert_seam_has_ratified_backend` passes silently on seam with ≥1 ratified backend.

Note: 10 exceeds the owner-set ≤8 ceiling.  **Consolidation:** merge invariant #7 + #8 into a single parametric test (`list_ratified_backends` and `list_inferred_backends` are exact mirror surfaces); merge invariant #5 + #6 into a single positive-path test.  Post-consolidation target: **8 invariants**.  Sits at owner-set ceiling · WITHIN.

**No-refactor:** No modifications to any pluggable seam module (CP-M6-1-1..1-4 · CP-M6-5-1).  The registry is a passive metadata surface — seams do NOT self-register at import time (case-agnostic; the registry is populated by explicit `register_backend` calls at composition points, not by seam-side static initializers).

**M6-seal-story deliverable:** on CP-M6-6-4 seal, populate `phase0/backend_ratification_snapshot.json` with the current live-registered state of all M6 seams (all currently `inferred_pending_ratification` per D10; ratified state is post-owner-ratification).  This snapshot becomes the source-of-truth "what is truly live" table for the M6-seal report.

---

## §D · §3.3 3-commit pattern (per CP; four times over)

Each CP walks:
1. **RED**  — author test file → run `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/ -q` → capture right-reason RED receipt at `phase0/drill_receipts/<utc>_wm6_6_<n>_RED_pre_impl.log`.  Failure reason: mechanism module missing → import fails on every CP test.
2. **Mechanism** — author `services/audio_plane_v1/<module>.py` in code repo.
3. **Targeted green** — run `BASELINE_GUARD=1 python -m pytest tests/invariants/test_wm6_6_<n>_*.py -v` for fast sanity (~0.5s).
4. **Ratchet bump** — bump `counts_at_baseline.passed` and `invariants_enforced_when_baseline_guard_1.passed_floor` by the invariant delta; append `ratchet_history` entry (with `ensure_ascii=True` to preserve JSON storage format).
5. **Double-green** — run full pytest twice back-to-back; strip timing line; verify byte-identical stripped-sha256.
6. **Rider** — capture `pip_freeze.txt` + `collect_only_summary.txt` at `phase0/wave_riders/w_m6_objective_wizard_cp<n>/`; assert pip zero-drift vs prior CP rider.
7. **Boundary probes** — fire probe at CP open + CP seal.
8. **Seal file** — write `phase0/output_verified_seals/cp_m6_6_<n>_<module>.seal.txt` with `Kind: cp_m6_6_<n>_<module>` first line; both track-a HEAD (after Commit A) and master HEAD `TBD` at seal-write; C-fixup will land master SHA.
9. **STATE updates** — append CP entry to `STATE/DECISIONS.md` + `STATE/NEXT.md`; keep track-a SHA at both files; master SHA `TBD` at commit B; landed at commit C.
10. **Commit A** (track-a code): stage mechanism + test + baseline_failures.json; commit.
11. **Commit B** (master state · master TBD): stage seal + STATE + phase0 receipts; commit.
12. **Commit C** (master state fixup · master landed): replace `TBD` with actual master SHA in seal + DECISIONS + NEXT; commit.

---

## §E · Wave-honest limits

1. **Objective Wizard STUB territory only.** CP-M6-6-1 lands the compile-refusal machinery over a STUB `TargetOutcomeStub`.  The full §10 `TargetOutcome` carrier lands at sub-wave 7 CP-M6-7-1.  The compile-refusal contract composes with the future full carrier without breaking (STUB has all fields the compile-refusal reads; full carrier is a superset).
2. **§8.5 V94 [VERIFY] B-2/B-3 landing state.** Sub-wave 6 does NOT extend the existing shaping-wizard state machine.  It builds compile-refusal as a standalone contract.  Owner may later re-home into existing wizard per V94 disposition; the invariants transfer verbatim.
3. **§9.2 P150 baseline tier changes are seam-governed.** Sub-wave 6 lands the FROZEN v1.0 five-item baseline set; changes are ceremony-governed (proposal, countersignature, waiting period).  No autonomous baseline changes in this or future sub-waves — extension is an owner-ratification-only path (same discipline as HUMAN_NAME_ATTRIBUTE_NAMES).
4. **CP-M6-6-1 `CollectionSchemaColumnStub.captures_custody_violating_field: bool`** is a MARKER field — sub-wave 6 does not re-import §6.2 conditions.  A future CP may wire this marker to a live §6.2 predicate without breaking the sub-wave 6 refusal contract (only mechanism internals change; the refusal surface stays).
5. **Rec-3-M6SW6 registry is METADATA-ONLY.**  It does not call backends; it records their ratification state.  Live-invocation paths remain untouched (each seam already refuses on invocation of an unratified backend per D10 discipline).  The registry adds a QUERY surface, not an enforcement path.

---

## §F · Definition of Done (sub-wave 6)

**Per-CP DoD** — as §D above.

**Sub-wave 6 DoD:**
- CP-M6-6-1 sealed under §3.3 (both SHAs banked).
- CP-M6-6-2 sealed under §3.3 (both SHAs banked).
- CP-M6-6-3 sealed under §3.3 (both SHAs banked).
- CP-M6-6-4 sealed under §3.3 (both SHAs banked).
- Wave-close report `notes/W_M6_OBJECTIVE_WIZARD_COLLECTION_SCHEMA_close.md` authored.
- `phase0/backend_ratification_snapshot.json` populated at CP-M6-6-4 seal.
- Ratchet delta target: +34..+38 invariants (10 + 9 + 11 + 8 target-band) · 4240 → ~4276..4280.
- Boundary probes #50..#57 fired (2 per CP × 4 CPs) — CD + Visitors expected FAIL throughout (blocker parked per owner Rec-2 escalation).
- Word-boundary executive-domain negative-scan CLEAN on every seal.
- §3.1 P038 tokens-not-waveforms discipline preserved on every new API surface.
- HALT boundary held: if any mechanism requires real estate voice/biometric material → HALT immediately.
- Word-boundary "audio_bytes" / "waveform" / "samples" / "raw_audio" / "voiceprint" / "speaker_embedding" negative-scan CLEAN on every new module.

**Owner-facing report cadence:** at sub-wave 6 seal OR genuine HALT.  No CP-level owner-facing reports.

---

## §G · Onward

Post-sub-wave-6 seal:
- Sub-wave 7 · W-M6-TARGET-OUTCOME-PLANNER · §10 + §11.1 + §11.4.
- Sub-wave 8 · calibration + acceptance (§11.2 + §11.3).
- Sub-wave 9 · Commission View surface (§13).
- Sub-wave 10 · M6 seal wrap-up.
- Then M7 opens (W0..W9 · ALREADY RATIFIED).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
