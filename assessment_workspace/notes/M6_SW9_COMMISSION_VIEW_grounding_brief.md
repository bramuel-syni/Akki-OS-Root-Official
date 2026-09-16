# M6 Sub-wave 9 · W-M6-COMMISSION-VIEW · grounding brief

**Opened at UTC:** 2026-09-16T~02:40Z
**Canon scope:** Audio Intelligence Plane §13 (P216..P220 · V119..V123 — Commission View surface specification).
**Track-a HEAD at open:** `b7ebccbeffd9795573a0a9f6c1e3ed439fa235a7` (CP-M6-8-2 · Sub-wave 8 close).
**Master HEAD at open:** `7505e2d8fd5c5491f64515d31e04efe74f9f3b58` (CP-M6-8-2 Commit C · SW-8 CLOSED).
**Ratchet floor at open:** 4338 (verified on disk).
**M6 §15 walk position:** 9 of 10 sub-waves.
**Owner GO ref:** Owner standing GO covers SW-9 (synthetic-fixture-safe surface work · session-open ruling 2026-09-16T~02:30Z relayed by user).

---

## §A · Canon anchors (verbatim on single un-wrapped lines)

### §13 · Surface Specification — the Commission View

#### §13.1 Scope

- **V119 · P216:** *"This surface adjustment applies to all commissioned work on the platform — extraction, census, and training commissions alike, across every extraction type. No modality receives its own UI, and no surface is a rendering of backend internals: rendering internals quietly commits the backend to building displayable versions of its own machinery."*

Sub-clauses (for gating tests):

- V119a — *"applies to all commissioned work on the platform — extraction, census, and training commissions alike, across every extraction type"* (case-agnostic scope · duck-typed commission input).
- V119b — *"No modality receives its own UI"* (single-surface discipline · no per-modality branch in the render path).
- V119c — *"no surface is a rendering of backend internals: rendering internals quietly commits the backend to building displayable versions of its own machinery"* (no-internals-projection discipline).

#### §13.2 Behaviour

- **V120 · P217 (LOAD-BEARING · full paragraph):** *"The surface is milestones. The artifacts are evidence behind them. At Sampling & Reflection, the proposed milestone list is presented to the objective owner for agreement. Commission does not open until it is agreed. The Commission View reports against the agreed checklist: each milestone with its done-condition and owner; status in plain terms — done, on track, behind, missed. Missed is shown as plainly as done. Spend against quote is shown at the same plain level. Technical material — calibration results, strata coverage, Collection Schema state — is drill-down evidence for whoever asks why a milestone reads as it does. It is never the front page."*

Sub-clauses (for gating tests):

- V120a — *"The surface is milestones. The artifacts are evidence behind them."* (milestones-first invariant · milestone list is the head projection · calibration/coverage/schema are subordinate).
- V120b — *"Commission does not open until it is agreed."* (composes V114c from CP-M6-8-2 · `assert_commission_open_only_after_agreement` gates the view construction).
- V120c — *"each milestone with its done-condition and owner; status in plain terms — done, on track, behind, missed."* (closed four-status enum · plain-terms discipline · no engineering vocabulary in status).
- V120d — *"Missed is shown as plainly as done."* (parity discipline — missed is not visually or structurally demoted).
- V120e — *"Spend against quote is shown at the same plain level."* (SpendAgainstQuote is a first-class carrier at the milestone-list level · not a technical drill-down).
- V120f — *"Technical material — calibration results, strata coverage, Collection Schema state — is drill-down evidence for whoever asks why a milestone reads as it does. It is never the front page."* (evidence-behind discipline · EvidenceRef carrier is subordinate to milestone rows · front-page projection excludes evidence content).

#### §13.3 Modality leaf

- **V121 · P218:** *"Modality appears at exactly one leaf: evidence inspection. Where provenance resolves to a recording, the source plays at its timestamp rather than rendering as a page region — the existing trust-receipt pattern (\"a disputed number is answered by playing the tape\"), unchanged."*

Sub-clauses (for gating tests):

- V121a — *"Modality appears at exactly one leaf: evidence inspection."* (modality lives ONLY in the drill-down leaf · not at the milestone-list head · not at status · not at spend).
- V121b — *"Where provenance resolves to a recording, the source plays at its timestamp rather than rendering as a page region"* (recording-provenance evidence carries a `plays_at_timestamp` seam; no audio bytes cross the seam · §3.1 P038 preserved).

#### §13.4 Backend cost constraint

- **V122 · P219 (LOAD-BEARING · reads-only discipline):** *"Milestones are records with done-conditions; the platform already stamps events. No new machinery is built for display. Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified."*

Sub-clauses (for gating tests):

- V122a — *"Milestones are records with done-conditions"* (compose CP-M6-8-2 `Milestone`/`MilestoneList` verbatim · no new milestone shape carrier introduced this sub-wave).
- V122b — *"the platform already stamps events"* (SpendAgainstQuote reads existing event stamps · does not compute new totals · caller provides the aggregate).
- V122c — *"No new machinery is built for display. Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified."* (reads-only assertion helper · caller-supplies-all-carriers pattern).

### §14/§15 read-alongside (informational · not gating)

- §14 Interface Summary (line 267): *"Commission View"* listed as the sole audio-plane surface.
- §15 Build Sequence (line 297..298): *"Commission View (§13) · Reads records created in 8; by §13.4 it cannot precede them."* — SW-8 (CP-M6-8-1 calibration + CP-M6-8-2 milestones) is the direct upstream · confirmed SW-8 has closed and both carriers land as one-way imports into SW-9.

---

## §B · CP breakdown

Sub-wave 9 walks two CPs.  Ceilings mirror sub-wave 6/7/8 owner-set discipline (≤10 per CP).

### CP-M6-9-1 · §13.1 + §13.4 Commission View schema + reads-only discipline

**New module:** `services/audio_plane_v1/commission_view.py`.

**Public API target (10 exports · owner-set ≤10 ceiling · WITHIN):**

- `MILESTONE_STATUS_VALUES` — frozenset of four canonical plain-terms tokens: `{"done", "on_track", "behind", "missed"}` (V120c closed-set).
- `MilestoneStatusEntry` — frozen 2-carrier: `milestone_ref: str` (FK by milestone_id) · `status: str` (must be in `MILESTONE_STATUS_VALUES` · refuses `MilestoneStatusInvalidError` at `__post_init__`).
- `SpendAgainstQuote` — frozen 2-carrier: `actual: float` · `cost_quote_ref: str` (opaque ref to a CP-M6-7-3 `CostQuoteWithCI` · reads existing carrier · V122b).  Refuses `SpendAgainstQuoteRefMissingError` on empty ref.
- `EvidenceRef` — frozen 2-carrier: `kind: str` (in a fixed closed-set of drill-down evidence kinds: `{"calibration", "strata_coverage", "collection_schema", "recording"}`) · `ref: str` (opaque · V120f · never the front page).  Refuses `EvidenceKindInvalidError` at `__post_init__`.
- `CommissionViewSnapshot` — frozen 4-carrier: `milestone_list: MilestoneList` (imported from CP-M6-8-2 · V122a) · `statuses: Tuple[MilestoneStatusEntry, ...]` (one entry per milestone · ordering aligned with `milestone_list.milestones`) · `spend: SpendAgainstQuote` · `evidence_refs: Tuple[EvidenceRef, ...]` (drill-down subordinate carrier).
- `construct_commission_view_snapshot(*, milestone_list, statuses, spend, evidence_refs) -> CommissionViewSnapshot` — factory · composes CP-M6-8-2 `MilestoneList` + this-module carriers.  Refuses `MilestoneListNotAgreedError` (V120b · composes CP-M6-8-2 `assert_commission_open_only_after_agreement`).  Refuses `StatusEntryCountMismatchError` when `len(statuses) != len(milestone_list.milestones)` (V120c parity discipline).  Refuses `StatusEntryOrderingMismatchError` when statuses' `milestone_ref` sequence does not align with `milestone_list.milestones[i].milestone_id` in order (V120a milestones-first + V114a ordering-load-bearing).
- `MilestoneStatusInvalidError` — V120c refusal.
- `MilestoneListNotAgreedError` — V120b refusal (subclass of `CommissionOpenBeforeAgreementError` from CP-M6-8-2 · refusal-family cohesion).
- `StatusEntryCountMismatchError` — V120c parity refusal.
- `EvidenceKindInvalidError` — V120f refusal.

**Invariants (target 10):**

1. `test_wm6_9_1_module_fabric` — 10 exports present.
2. `test_wm6_9_1_v119_verbatim_in_module_docstring` — V119 full paragraph anchored.
3. `test_wm6_9_1_v120_verbatim_in_module_docstring` — V120 LOAD-BEARING full paragraph anchored.
4. `test_wm6_9_1_v122_verbatim_in_module_docstring` — V122 LOAD-BEARING full paragraph anchored.
5. `test_wm6_9_1_milestone_status_values_frozen_four_set` — exact canonical four tokens · frozenset immutable.
6. `test_wm6_9_1_milestone_status_entry_refuses_invalid_status` — closed-enum discipline enforced.
7. `test_wm6_9_1_evidence_ref_refuses_invalid_kind` — closed-enum discipline enforced.
8. `test_wm6_9_1_commission_view_snapshot_refuses_ungreed_milestone_list` — V120b composes V114c (subclass identity preserved for family catch).
9. `test_wm6_9_1_commission_view_snapshot_refuses_status_count_mismatch` — V120c parity refusal.
10. `test_wm6_9_1_commission_view_snapshot_refuses_status_ordering_mismatch` — V120a/V114a ordering-alignment refusal.

### CP-M6-9-2 · §13.2 milestones-first render + §13.3 modality leaf · CLOSES SUB-WAVE 9

**Append-only extension of same module** `services/audio_plane_v1/commission_view.py` under a marked header `# Part-B · §13.2 + §13.3 · Render + Modality leaf`.

**Public API target (8 exports · combined 10+8=18 module surface):**

- `CommissionViewProjection` — frozen 4-carrier: `milestones_head: Tuple[MilestoneRow, ...]` (front-page rows · V120a milestones-first) · `spend_head: SpendAgainstQuote` (V120e "same plain level") · `evidence_leaves: Tuple[EvidenceRef, ...]` (V120f drill-down · never front page) · `snapshot_ref: str` (opaque ref back to the snapshot).
- `MilestoneRow` — frozen 4-carrier: `milestone_id` · `done_condition` · `owner` · `status`.  Reads from `Milestone` + status entry.  No new fields.
- `render_commission_view(*, snapshot) -> CommissionViewProjection` — deterministic projection.  Iterates `snapshot.milestone_list.milestones` in order (V114a) · zips with `snapshot.statuses` · assembles `MilestoneRow` list · attaches `spend_head` and `evidence_leaves` at head level · returns immutable projection.  V120b composes: refuses via factory if snapshot's `milestone_list` unagreed (already enforced upstream · this is defence-in-depth).
- `RecordingEvidenceLeaf` — frozen 3-carrier: `evidence_ref: EvidenceRef` (kind must equal `"recording"` at construction · refuses `RecordingEvidenceKindMismatchError` at `__post_init__`) · `plays_at_timestamp: str` (§13.3 V121b timestamp seam · opaque ISO-8601-shaped string) · `recording_provenance_ref: str` (opaque · no audio bytes cross · §3.1 P038 preserved).
- `assert_no_internals_projected(*, projection) -> None` — V119c refusal: refuses `InternalsProjectedError` if the projection carries any field whose name is in a fixed forbidden-set (e.g., `"pytest_stripped_sha256"`, `"ratchet"`, `"invariant"`, `"seam"`, `"mongodb_"`, `"redis_"`, `"http_"`, `"grpc_"`) — statically closed by scanning `dataclasses.fields(projection)` field names.
- `assert_no_new_backend_computation(*, projection, snapshot) -> None` — V122c reads-only defence: refuses `NewBackendComputationError` if the projection introduces any carrier whose dataclass name is not in `{CommissionViewProjection, MilestoneRow, SpendAgainstQuote, EvidenceRef, RecordingEvidenceLeaf}` (allow-list of shape) — statically enforceable by type(x).__name__ walk.
- `RecordingEvidenceKindMismatchError` — V121b refusal.
- `InternalsProjectedError` — V119c refusal.
- `NewBackendComputationError` — V122c refusal.

**Invariants (target 10):**

1. `test_wm6_9_2_part_b_module_fabric` — 8 new exports + 10 prior = 18 total.
2. `test_wm6_9_2_v120_v121_v122_verbatim_in_module_docstring` — V120 + V121 + V122 all anchored (already in Part-A docstring · Part-B does not remove).
3. `test_wm6_9_2_render_commission_view_orders_by_milestone_list` — V120a milestones-first + V114a ordering-load-bearing.
4. `test_wm6_9_2_render_commission_view_missed_shown_at_head_level` — V120d parity discipline: a `missed` status row appears at the head level identically to a `done` row (same MilestoneRow shape · no demotion).
5. `test_wm6_9_2_render_commission_view_evidence_at_leaf_not_head` — V120f evidence-behind: `evidence_leaves` are on the projection body but MilestoneRow carries no evidence-content field.
6. `test_wm6_9_2_recording_evidence_leaf_refuses_non_recording_kind` — V121a modality-at-one-leaf discipline (only `kind=="recording"` accepted).
7. `test_wm6_9_2_recording_evidence_leaf_carries_plays_at_timestamp_no_audio_bytes` — V121b/§3.1 P038 preserved: field-set frozen to timestamp + provenance ref · negative-scan on `audio_bytes`/`waveform`/`samples`/`raw_audio`.
8. `test_wm6_9_2_assert_no_internals_projected_refuses_forbidden_field_names` — V119c internals-projection refusal fires on forbidden field name (synthetic dataclass fixture with `ratchet` field).
9. `test_wm6_9_2_assert_no_new_backend_computation_refuses_off_allowlist_carrier` — V122c refuses a synthetic off-allowlist dataclass injected as an `evidence_leaves` entry via monkey-patching.
10. `test_wm6_9_2_compose_v120b_render_refuses_ungreed_snapshot` — defence-in-depth: even if a caller bypasses the CP-M6-9-1 factory, `render_commission_view` refuses via re-check on `snapshot.milestone_list.commission_agreement_ref is None`.

---

## §C · §3.3 3-commit pattern (per CP; twice over)

Standard §3.3 pattern applies (per M6 SW7 grounding brief §C · per M6 SW8 grounding brief §C).

Per-CP: Commit A (code · programme/track-a) → Commit B (state · master · master TBD) → Commit C (state fixup · master landed).  Both SHAs recorded in seal + DECISIONS + NEXT at CP close.

---

## §D · Wave-honest limits

1. **Synthetic-fixture-safe.**  All tests construct their own `MilestoneList`/`CostQuoteWithCI`/`CalibrationOutput` inputs (already-supported by CP-M6-7-3 + CP-M6-8-1 + CP-M6-8-2 frozen carriers).  No real estate data · no audio bytes.
2. **V121b recording-modality leaf is a *ref*-carrier only.**  `RecordingEvidenceLeaf.plays_at_timestamp` is an opaque timestamp string; `recording_provenance_ref` is an opaque ref.  The actual "playback" is a Watch/UI concern; the audio-plane surface carries only the pull-seam references (§3.1 P038 preserved · no audio bytes cross).
3. **§13.4 V122 reads-only enforcement is at authoring boundary.**  `assert_no_new_backend_computation` walks the projection's own carriers; it does NOT prove absence of backend computation in caller code — that discipline lives in future integration tests at the caller boundary.  Documented as a wave-honest limit.
4. **V120c closed four-status enum is EXACT.**  No new status tokens accepted this CP.  Any future expansion (e.g., "awaiting-input") is a §13.2 amendment — banked as an owner-desk item, not a silent addition.
5. **V119c internals-projection refusal is REDACTED-FIELD-NAME based.**  A forbidden field-name set is fixed at authoring time; future engineering vocabulary additions to the ban-list require a new CP.  Not a total defence against internals leakage (e.g., a benign-named field carrying an internals-shaped value is not caught by name-scan alone).  Documented as a wave-honest limit.
6. **No LLM / HTTP / filesystem / network. Case-agnostic. §3.1 P038 preserved.**
7. **HALT boundary preserved.**  If any mechanism this sub-wave requires real estate voice/biometric material → HALT to owner immediately.  §11.6 is the primary HALT trigger and lands sub-wave 10.

---

## §E · Definition of Done

**Per-CP DoD** — as §C above.

**Sub-wave 9 DoD:**

- CP-M6-9-1 sealed under §3.3.
- CP-M6-9-2 sealed under §3.3.
- Wave-close report `notes/W_M6_COMMISSION_VIEW_close.md` authored.
- Ratchet delta target: +18..+22 (two CPs at 8-10 each).
- Boundary probes #60 + #61 target: all NOTE-SKIPPED per SEC halt (probe loop resumes only after JUMP custody rotation to JSON).
- Word-boundary executive-domain + audio-material negative-scan CLEAN on every seal.
- §3.1 P038 tokens-not-waveforms discipline preserved on every new API surface.
- Composes with CP-M6-8-2 `MilestoneList` and CP-M6-7-3 `CostQuoteWithCI` via import-only (no refactor of upstream modules).
- HALT boundary held.

**Owner-facing report cadence:** at sub-wave 9 seal OR genuine HALT.

**Owner-desk items still open (unchanged this shift):**

- SEC incident ratification in `STATE/DECISIONS.md`.
- JUMP root credential rotation (+ optional custody-format migration to JSON).
- Admin SG binds for CD + Visitors + NAS-username spelling correction (`bramuel` vs `bramwel`).
- Audio-source unblocks + Audio-plane sensitivity declarations (parked).
- Path α/β ruling for M6-INGEST-STAGE-1 (parked).

---

## §F · Onward (post-sub-wave-9)

- **Sub-wave 10 · W-M6-FULL-TRAINING-RUNS · §11.6 full training runs — MANDATORY HALT-TO-OWNER at sub-wave open.**  Grounding brief authored to surface the HALT · no CP-M6-10-* work fires until owner rules on real-estate audio access (§4.1 language corpus · §4.3 channel classes · §6.4 P102 read-scope enforcement · Audio-bytes-retention Path A/B/C).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
