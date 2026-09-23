---
card_id: CP_AIP_9_COMMISSION_VIEW
title: AIP v1.0 §13.2 milestones-first-render-boundary + §13.3 modality-leaf-recording + §13.4 reads-only-no-new-backend-computation · Item 5.9 CP-AIP-9
ratified_at_utc: 2026-02-23T08:19:00Z
ratified_by: Owner cadence directive verbatim (2026-02-23 CP-AIP-4 GO) 'run CP-AIP-5 → CP-AIP-10 sequentially · brief report-and-continue after CP-AIP-6 seals · HALT after CP-AIP-10 for full plane completion report · immediate HALT on any SPEC-CONFLICT-<n>' + Item-4 checkpoint GO + Owner CP-AIP-9 constraint verbatim (2026-02-23 at CP-AIP-8 report-and-continue): 'CP-AIP-9 (§13: milestones-first, artifacts as drill-down evidence only, ZERO new backend computation — any surface element needing computation beyond reading existing artifacts is out of spec per §13.4 and must be pinned as such).'
card_sha256: 3d44f89ddad5fa87335db90395e0485be25236071a8b1ec6b8a0eb4b9af55cd7
milestone_status: OPEN (Item 5.9 CP-AIP-9 · in-flight for this seal · continues sequential cadence · continues to CP-AIP-10 post-seal)
---

# CP-AIP-9-COMMISSION-VIEW · AIP v1.0 §13.2 + §13.3 + §13.4

## OBJECTIVE

Land the additive Commission-View compose-boundary as pure §1.2 modality-extension of sealed CP-M6-9-1 + CP-M6-9-2 Commission-View primitives (`MILESTONE_STATUS_VALUES` frozen four-set `{done, on_track, behind, missed}` · `MilestoneStatusEntry` · `SpendAgainstQuote` · `EvidenceRef` · `CommissionViewSnapshot` · `construct_commission_view_snapshot` · `CommissionViewProjection` · `MilestoneRow` · `render_commission_view` · `RecordingEvidenceLeaf` · `assert_no_internals_projected` · `assert_no_new_backend_computation` · `MilestoneStatusInvalidError` · `MilestoneListNotAgreedError` · `StatusEntryCountMismatchError` · `StatusEntryOrderingMismatchError` · `SpendAgainstQuoteRefMissingError` · `EvidenceKindInvalidError` · `RecordingEvidenceKindMismatchError` · `InternalsProjectedError` · `NewBackendComputationError`) + sealed CP-M6-8-2 §11.3 milestone primitives (`Milestone` · `MilestoneList` · `assert_commission_open_only_after_agreement` · `CommissionOpenBeforeAgreementError`) + sealed CP-M6-7-3 `CostQuoteWithCI` + sealed CP-AIP-8 `SamplingReflectionBoundaryResult_v1`. Zero sealed-carrier edit per SO §3.8.

The compose-boundary binds: (i) render refused if the source `MilestoneList` has not been agreed (§13.2 V120b verbatim 'Commission does not open until it is agreed'); (ii) status outside the closed four-set refused (§13.2 V120c verbatim 'status in plain terms — done, on track, behind, missed'); (iii) internals projected onto the surface refused (§13.1 V119c verbatim 'no surface is a rendering of backend internals'); (iv) new-backend-computation carrier or leaf outside the reads-only allow-list refused (§13.4 V122c verbatim 'No new machinery is built for display. Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification'); (v) modality leaf refused when kind != 'recording' (§13.3 V121a verbatim 'Modality appears at exactly one leaf: evidence inspection'); (vi) the new module carries a `NO_BACKEND_COMPUTATION_V1_POSTURE` Final marker citing §13.4 P219 V122c verbatim owner-pinned constraint.

`canon_ref: AIP v1.0 §13.1 V119c verbatim + §13.2 V120a..V120f verbatim + §13.3 V121a..V121b verbatim + §13.4 V122a..V122c verbatim + §1.2 modality-extension + §1.5 unrepresentable-not-policed.`

**OWNER-PINNED §13.4 CONSTRAINT VERBATIM (2026-02-23 at CP-AIP-8 report-and-continue):** 'CP-AIP-9 (§13: milestones-first, artifacts as drill-down evidence only, ZERO new backend computation — any surface element needing computation beyond reading existing artifacts is out of spec per §13.4 and must be pinned as such).'

## MUST DO

1. **§13.2 V120b verbatim · agreement-required-at-view-boundary** — `enter_view_boundary_with_snapshot(snapshot=<snapshot-with-unagreed-list>)` invokes sealed `render_commission_view` which raises sealed `MilestoneListNotAgreedError` (a subclass of `CommissionOpenBeforeAgreementError`); the boundary surfaces this refusal via `AgreementMissingAtViewBoundary`. Enforced by `test_view_boundary_refuses_render_when_milestone_list_unagreed`. `canon_ref: AIP §13.2 V120b verbatim + §11.3 V114c verbatim + P217.`

2. **§13.2 V120c verbatim · status-outside-closed-set-refused** — construction of `MilestoneStatusEntry` with a status outside the sealed frozen four-set raises sealed `MilestoneStatusInvalidError`; the boundary composes this refusal via `StatusValueRefusedAtViewBoundary`. Enforced by `test_view_boundary_refuses_status_outside_closed_four_set`. `canon_ref: AIP §13.2 V120c verbatim + P217.`

3. **§13.1 V119c verbatim · internals-projection-refused** — `assert_projection_is_internals_free_at_view_boundary(projection=<with-forbidden-field>)` composes sealed `assert_no_internals_projected` which raises sealed `InternalsProjectedError`; the boundary surfaces this refusal via `InternalsProjectedAtViewBoundary`. Enforced by `test_view_boundary_refuses_internals_projection`. `canon_ref: AIP §13.1 V119c verbatim + P216.`

4. **§13.4 V122c verbatim · new-backend-computation-refused (OWNER-PINNED CONSTRAINT)** — `assert_projection_is_reads_only_at_view_boundary(projection=<with-non-allowlisted-carrier>, snapshot=...)` composes sealed `assert_no_new_backend_computation` which raises sealed `NewBackendComputationError`; the boundary surfaces this refusal via `NewBackendComputationAtViewBoundary`. Enforced by `test_view_boundary_refuses_new_backend_computation_carrier`. `canon_ref: AIP §13.4 V122c verbatim + P219 + owner CP-AIP-9 constraint verbatim 2026-02-23.`

5. **§13.3 V121a verbatim · modality-leaf-only-recording-refused** — `serve_recording_evidence_leaf(evidence_ref=<kind_not_recording>, ...)` composes sealed `RecordingEvidenceLeaf.__post_init__` which raises sealed `RecordingEvidenceKindMismatchError`; the boundary surfaces this refusal via `ModalityLeafNotRecordingAtViewBoundary`. Enforced by `test_view_boundary_refuses_modality_leaf_not_recording`. `canon_ref: AIP §13.3 V121a verbatim + P218.`

6. **§1.2 no-redeclaration scan · sealed commission-view + milestone + cost-quote-with-CI carriers** — the NEW module does NOT redeclare `MILESTONE_STATUS_VALUES` / `MilestoneStatusEntry` / `SpendAgainstQuote` / `EvidenceRef` / `CommissionViewSnapshot` / `construct_commission_view_snapshot` / `CommissionViewProjection` / `MilestoneRow` / `render_commission_view` / `RecordingEvidenceLeaf` / `assert_no_internals_projected` / `assert_no_new_backend_computation` / `Milestone` / `MilestoneList` / `assert_commission_open_only_after_agreement` / `CostQuoteWithCI` (15 sealed symbols). Structural class-declaration + def scan (bounded pattern, no false-positive on refusal subclasses whose names contain sealed tokens). Enforced by `test_new_module_does_not_redeclare_sealed_carriers`. `canon_ref: AIP §1.2 verbatim + BL #4.`

7. **§13.4 · NO_BACKEND_COMPUTATION_V1_POSTURE Final marker present (OWNER-PINNED CONSTRAINT)** — the NEW module MUST carry a `NO_BACKEND_COMPUTATION_V1_POSTURE` Final str marker whose value cites §13.4 P219 V122 verbatim: 'No new machinery is built for display. Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified.' Enforced by `test_new_module_carries_no_backend_computation_v1_posture_marker`. `canon_ref: AIP §13.4 V122c verbatim + P219 + owner CP-AIP-9 constraint verbatim 2026-02-23.`

8. **Anti-drift §3 + §5 anchor scan · §13 citations + ledger-check** — the NEW module cites its exact AIP section anchors + carries the ledger-check anchor. Enforced by `test_new_module_cites_section_anchors_and_ledger_check`. `canon_ref: Anti-drift standing guard §3 + §5.`

9. **8 RED-first pytest invariants** — RED_pre 8/8 failed → GREEN_post 8/8 passed. `canon_ref: SO §3 RED-first.`

10. **Ratchet floor 6317 → 6325** — +8 canonical measured pins · `ensure_ascii=False, indent=2` per BL #11 + BL #7. `canon_ref: SO §3 no-silent-rebaselining + BL #6/7/11.`

11. **5-commit seal on dual branches + /app companion** — Terminal `pytest` only · BASELINE_GUARD double-green. `canon_ref: SO §3.3 5-Commit-Seal.`

## MUST NOT

- Edit any sealed §13 / §11.3 / §11.4 carrier (`audio_plane_v1/commission_view.py` CP-M6-9-1/9-2 · `audio_plane_v1/milestones.py` sealed · CP-M6-7-3 `CostQuoteWithCI` inside `training_planner.py` · CP-AIP-8 `sampling_reflection_boundary_v1.py` · any prior CP-AIP-1..8 or CP-CENSUS carrier). `canon_ref: SO §3.8 additive-only.`

- Redeclare any sealed commission-view / milestone / cost-quote carrier. `canon_ref: AIP §1.2 verbatim + BL #4.`

- **Introduce ANY new backend computation beyond reading existing artifacts (OWNER-PINNED §13.4 CONSTRAINT).** Any surface element in this section found to require new backend computation is out of specification and MUST be pinned as such. Additive-only reads composing sealed primitives · no arithmetic, no comparisons producing status decisions, no aggregation logic. `canon_ref: AIP §13.4 V122c verbatim + P219 + owner CP-AIP-9 constraint verbatim 2026-02-23.`

- Render internals onto the surface (§13.1 V119c verbatim). Composes sealed `assert_no_internals_projected`. `canon_ref: AIP §13.1 V119c verbatim.`

- Emit a modality projection that is not the sealed `RecordingEvidenceLeaf` shape (§13.3 V121a verbatim). `canon_ref: AIP §13.3 V121a verbatim.`

- Render a Commission View for an unagreed `MilestoneList` (§13.2 V120b verbatim). Composes sealed `MilestoneListNotAgreedError`. `canon_ref: AIP §13.2 V120b verbatim.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-9-COMMISSION-VIEW and nothing else. Frontend surface / router / persistence adapters DEFERRED (this slice enforces only the additive compose-boundary as §1.2 modality-extension of sealed CP-M6-9-1/9-2). `canon_ref: SO §7 guard 5.`

## EXIT

**8 RED-first invariants (RED_pre 8/8 failed · GREEN_post 8/8 passed):**

- tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py::test_view_boundary_refuses_render_when_milestone_list_unagreed
- tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py::test_view_boundary_refuses_status_outside_closed_four_set
- tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py::test_view_boundary_refuses_internals_projection
- tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py::test_view_boundary_refuses_new_backend_computation_carrier
- tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py::test_view_boundary_refuses_modality_leaf_not_recording
- tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py::test_new_module_does_not_redeclare_sealed_carriers
- tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py::test_new_module_carries_no_backend_computation_v1_posture_marker
- tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py::test_new_module_cites_section_anchors_and_ledger_check

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6317 → 6325 (+8 canonical measured)
- baseline_failures list unchanged
- both sweeps byte-identical `stripped_sha256` (banked in receipt post-seal)

## STOP

Stop at 5-commit seal landing. Continue immediately to CP-AIP-10-TRAINING-RUNS.

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §13 / sealed CP-M6-9-1/9-2 primitives / sealed §11.3 milestone primitives / sealed CP-AIP-8 sampling-reflection boundary / sealed CP-M6-7-3 CostQuoteWithCI, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report immediately.

## ANCHORS

**Spec anchors (AIP v1.0):**
- §13.1 P216 verbatim (V119c LOAD-BEARING): 'no surface is a rendering of backend internals: rendering internals quietly commits the backend to building displayable versions of its own machinery.'
- §13.2 P217 verbatim (V120 LOAD-BEARING): 'The surface is milestones. The artifacts are evidence behind them.'
- §13.2 V120a verbatim: 'The surface is milestones' + V114a ordering-load-bearing.
- §13.2 V120b verbatim: 'Commission does not open until it is agreed.'
- §13.2 V120c verbatim: 'status in plain terms — done, on track, behind, missed. Missed is shown as plainly as done.'
- §13.2 V120e verbatim: 'Spend against quote is shown at the same plain level.'
- §13.2 V120f verbatim: 'Technical material — calibration results, strata coverage, Collection Schema state — is drill-down evidence for whoever asks why a milestone reads as it does. It is never the front page.'
- §13.3 P218 verbatim (V121): 'Modality appears at exactly one leaf: evidence inspection.'
- §13.3 V121a verbatim: 'Modality appears at exactly one leaf: evidence inspection.'
- §13.3 V121b verbatim: 'Where provenance resolves to a recording, the source plays at its timestamp rather than rendering as a page region.'
- §13.4 P219 verbatim (V122 LOAD-BEARING · reads-only · OWNER-PINNED CONSTRAINT): 'No new machinery is built for display. Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified.'
- §13.4 V122c verbatim: 'No new machinery is built for display.'
- §14 Interface Summary verbatim: 'Commission View — Reads milestones, statuses, spend, and existing artifacts only; introduces no new backend computation.'
- §15 Build Sequence #9 verbatim: 'Reads records created in 8; by §13.4 it cannot precede them.'

**Owner directives (verbatim):**
- Item 4 GO (2026-02-23): 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
- CP-AIP-4 GO + Cadence GO (2026-02-23 post-INTERIM REPORT): 'run CP-AIP-5 → CP-AIP-10 sequentially; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>.'
- **CP-AIP-9 constraint (2026-02-23 at CP-AIP-8 report-and-continue) verbatim:** 'CP-AIP-9 (§13: milestones-first, artifacts as drill-down evidence only, ZERO new backend computation — any surface element needing computation beyond reading existing artifacts is out of spec per §13.4 and must be pinned as such).'

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/services/audio_plane_v1/commission_view.py` (CP-M6-9-1 + CP-M6-9-2 · §13 · sealed · NOT edited).
- `backend/services/audio_plane_v1/milestones.py` (CP-M6-8-2 · §11.3 · sealed · NOT edited).
- `backend/services/audio_plane_v1/training_planner.py` (CP-M6-7-2/3 · sealed · CostQuoteWithCI · NOT edited).
- `backend/services/audio_plane_v1/sampling_reflection_boundary_v1.py` (CP-AIP-8 · sealed · NOT edited).
- All CP-AIP-1..8 modules — untouched this seal.

**New additive module landed by this seal (1 file):**
- `backend/services/audio_plane_v1/commission_view_boundary_v1.py` (~200 lines · `CommissionViewBoundaryResult_v1` frozen 3-carrier + 5 refusal classes all subclassing `CommissionViewBoundaryRefused` (`AgreementMissingAtViewBoundary` · `StatusValueRefusedAtViewBoundary` · `InternalsProjectedAtViewBoundary` · `NewBackendComputationAtViewBoundary` · `ModalityLeafNotRecordingAtViewBoundary`) + 4 boundary callables `enter_view_boundary_with_snapshot` + `assert_projection_is_reads_only_at_view_boundary` + `assert_projection_is_internals_free_at_view_boundary` + `serve_recording_evidence_leaf` · composes sealed CP-M6-9-1/9-2 Commission-View primitives + sealed §11.3 milestone + sealed CP-M6-7-3 CostQuoteWithCI + sealed CP-AIP-8 SamplingReflectionBoundaryResult_v1 · `NO_BACKEND_COMPUTATION_V1_POSTURE` Final marker citing §13.4 P219 V122c verbatim · **§13.4 owner-pinned zero-new-backend-computation posture**).

**Test file:**
- `backend/tests/invariants/test_cp_aip_9_commission_view_aip_v1_0_section_13.py` (~320 lines · 8 pins).

**Standing Orders anchors:**
- SO §3 RED-first · SO §3.3 5-Commit Seal · SO §3.8 additive-only · SO §6.2 objective-card + hash-pin · SO §7 17-guard consolidated set · Six Standing Bans.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-9-COMMISSION-VIEW and nothing else.
