"""CP-AIP-9-COMMISSION-VIEW · additive compose-boundary · AIP v1.0 §13 (Surface Specification — the Commission View).

Ledger check - this module implements EXECUTION_ORDER.md item 5 CP-AIP-9-COMMISSION-VIEW and nothing else.

Owner CP-AIP-9 constraint verbatim (2026-02-23 at CP-AIP-8 report-and-continue):
  'CP-AIP-9 (§13: milestones-first, artifacts as drill-down evidence only, ZERO new
   backend computation — any surface element needing computation beyond reading
   existing artifacts is out of spec per §13.4 and must be pinned as such).'

Verbatim canon anchors (§13.1 P216 · §13.2 P217 · §13.3 P218 · §13.4 P219):

- §13.1 P216 verbatim (V119c LOAD-BEARING): 'no surface is a rendering of backend
  internals: rendering internals quietly commits the backend to building displayable
  versions of its own machinery.'

- §13.2 P217 verbatim (V120 LOAD-BEARING): 'The surface is milestones. The artifacts
  are evidence behind them. At Sampling & Reflection, the proposed milestone list is
  presented to the objective owner for agreement. Commission does not open until it
  is agreed. The Commission View reports against the agreed checklist: each milestone
  with its done-condition and owner; status in plain terms — done, on track, behind,
  missed. Missed is shown as plainly as done. Spend against quote is shown at the
  same plain level. Technical material — calibration results, strata coverage,
  Collection Schema state — is drill-down evidence for whoever asks why a milestone
  reads as it does. It is never the front page.'

- §13.3 P218 verbatim (V121): 'Modality appears at exactly one leaf: evidence
  inspection. Where provenance resolves to a recording, the source plays at its
  timestamp rather than rendering as a page region — the existing trust-receipt
  pattern ("a disputed number is answered by playing the tape"), unchanged.'

- §13.4 P219 verbatim (V122 LOAD-BEARING · reads-only · OWNER-PINNED CONSTRAINT):
  'Milestones are records with done-conditions; the platform already stamps events.
  No new machinery is built for display. Any surface element in this section found
  to require new backend computation beyond reading existing artifacts is out of
  specification and must be removed or re-specified.'

This module is a pure §1.2 modality-extension composing sealed CP-M6-9-1 + CP-M6-9-2
Commission-View primitives (`MILESTONE_STATUS_VALUES` · `MilestoneStatusEntry` ·
`SpendAgainstQuote` · `EvidenceRef` · `CommissionViewSnapshot` ·
`construct_commission_view_snapshot` · `CommissionViewProjection` · `MilestoneRow` ·
`render_commission_view` · `RecordingEvidenceLeaf` · `assert_no_internals_projected` ·
`assert_no_new_backend_computation` · sealed refusals) + sealed CP-M6-8-2 §11.3
milestone primitives (`Milestone` · `MilestoneList` ·
`assert_commission_open_only_after_agreement`) + sealed CP-M6-7-3 `CostQuoteWithCI`
+ sealed CP-AIP-8 `SamplingReflectionBoundaryResult_v1`.

**Zero sealed-carrier edit per SO §3.8 additive-only. ZERO NEW BACKEND COMPUTATION
per owner CP-AIP-9 constraint verbatim + §13.4 P219 V122c.**

Wave-honest limits:
- Synthetic-fixture-safe · no LLM / HTTP / filesystem / network / MongoDB.
- Reads-only: this module contains NO arithmetic, comparison-derived status
  decisions, aggregation, or any computation beyond composing sealed reads.
- §3.1 P038 tokens-not-waveforms preserved · modality leaf is a REF-carrier only
  (opaque timestamp + provenance ref).
- Refusal subclasses use word-boundary-safe names to keep the §1.2 no-redeclaration
  scan false-positive-free (e.g. `AgreementMissingAtViewBoundary` does NOT contain
  the exact sealed carrier name as a class-declaration substring).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Tuple

# Sealed CP-M6-9-1 + CP-M6-9-2 Commission-View primitives (imported by name;
# never redeclared per §1.2 verbatim).
from services.audio_plane_v1.commission_view import (
    CommissionViewProjection,
    CommissionViewSnapshot,
    EvidenceRef,
    MilestoneListNotAgreedError,
    NewBackendComputationError,
    InternalsProjectedError,
    RecordingEvidenceKindMismatchError,
    RecordingEvidenceLeaf,
    assert_no_internals_projected,
    assert_no_new_backend_computation,
    render_commission_view,
)
# Sealed CP-M6-8-2 §11.3 milestone primitives (imported by name; never
# redeclared per §1.2 verbatim).
from services.audio_plane_v1.milestones import (
    MilestoneList,
    assert_commission_open_only_after_agreement,
    CommissionOpenBeforeAgreementError,
)


__all__ = (
    # Owner-pinned constraint posture marker (§13.4 · CP-AIP-9 constraint verbatim)
    "NO_BACKEND_COMPUTATION_V1_POSTURE",
    # Boundary carrier (compose-boundary result)
    "CommissionViewBoundaryResult_v1",
    # Base refusal + five refusal subclasses (§13.1 · §13.2 · §13.3 · §13.4)
    "CommissionViewBoundaryRefused",
    "AgreementMissingAtViewBoundary",
    "StatusValueRefusedAtViewBoundary",
    "InternalsProjectedAtViewBoundary",
    "NewBackendComputationAtViewBoundary",
    "ModalityLeafNotRecordingAtViewBoundary",
    # Boundary callables (four)
    "enter_view_boundary_with_snapshot",
    "assert_projection_is_reads_only_at_view_boundary",
    "assert_projection_is_internals_free_at_view_boundary",
    "serve_recording_evidence_leaf",
)


# ---------------------------------------------------------------------------
# OWNER-PINNED §13.4 CONSTRAINT POSTURE (owner CP-AIP-9 constraint verbatim
# 2026-02-23 at CP-AIP-8 report-and-continue + §13.4 P219 V122c verbatim).
# ---------------------------------------------------------------------------


NO_BACKEND_COMPUTATION_V1_POSTURE: Final[str] = (
    "§13.4 P219 V122c verbatim (LOAD-BEARING · reads-only · OWNER-PINNED "
    "CONSTRAINT): 'Milestones are records with done-conditions; the platform "
    "already stamps events. No new machinery is built for display. Any surface "
    "element in this section found to require new backend computation beyond "
    "reading existing artifacts is out of specification and must be removed or "
    "re-specified.' · Owner CP-AIP-9 constraint verbatim 2026-02-23 at CP-AIP-8 "
    "report-and-continue: 'CP-AIP-9 (§13: milestones-first, artifacts as "
    "drill-down evidence only, ZERO new backend computation — any surface "
    "element needing computation beyond reading existing artifacts is out of "
    "spec per §13.4 and must be pinned as such).' · This module contains NO "
    "arithmetic, comparison-derived status decisions, aggregation, or any "
    "computation beyond composing sealed reads · §1.2 modality-extension."
)


# ---------------------------------------------------------------------------
# Boundary result carrier (§1.2 · frozen · composes sealed reads only).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CommissionViewBoundaryResult_v1:
    """§13.2 milestones-first Commission-View compose-boundary result.

    Frozen 3-carrier composing sealed CP-M6-9-1/9-2 outputs:
      - `projection`: sealed `CommissionViewProjection` (V120a milestones-first).
      - `snapshot`:   sealed `CommissionViewSnapshot`   (source-of-truth ref).
      - `posture_note`: opaque str carrying the §13.4 owner-pinned constraint
        posture (see `NO_BACKEND_COMPUTATION_V1_POSTURE`).

    Contains NO computed fields · reads-only composition.
    """

    projection: CommissionViewProjection
    snapshot: CommissionViewSnapshot
    posture_note: str


# ---------------------------------------------------------------------------
# Base refusal + five clause-anchored subclasses (§13.1 · §13.2 · §13.3 · §13.4).
# All refusals surface sealed refusals from CP-M6-9-1/9-2 or CP-M6-8-2 by
# family-catch discipline (each subclass ALSO subclasses the sealed refusal
# so a caller can catch either the boundary layer or the sealed layer).
# ---------------------------------------------------------------------------


class CommissionViewBoundaryRefused(Exception):
    """§13 compose-boundary refusal base · family-catch anchor."""


class AgreementMissingAtViewBoundary(
    CommissionViewBoundaryRefused, MilestoneListNotAgreedError
):
    """§13.2 V120b verbatim: 'Commission does not open until it is agreed.'
    Raised by `enter_view_boundary_with_snapshot` when the source snapshot
    carries an unagreed MilestoneList (defence-in-depth against a caller
    bypassing the CP-M6-9-1 factory).  Composes sealed
    `MilestoneListNotAgreedError` <: `CommissionOpenBeforeAgreementError`."""


class StatusValueRefusedAtViewBoundary(CommissionViewBoundaryRefused):
    """§13.2 V120c verbatim: 'status in plain terms — done, on track, behind,
    missed.'  The sealed CP-M6-9-1 `MilestoneStatusEntry.__post_init__`
    raises `MilestoneStatusInvalidError` on out-of-set status values; this
    boundary symbol exists so callers can family-catch at the CP-AIP-9 layer."""


class InternalsProjectedAtViewBoundary(
    CommissionViewBoundaryRefused, InternalsProjectedError
):
    """§13.1 V119c verbatim: 'no surface is a rendering of backend internals.'
    Raised by `assert_projection_is_internals_free_at_view_boundary` when
    the projection carries a forbidden-name field (composes sealed
    `assert_no_internals_projected`)."""


class NewBackendComputationAtViewBoundary(
    CommissionViewBoundaryRefused, NewBackendComputationError
):
    """§13.4 V122c verbatim (LOAD-BEARING · OWNER-PINNED): 'No new machinery
    is built for display.'  Raised by
    `assert_projection_is_reads_only_at_view_boundary` when the projection
    carrier type is outside the sealed reads-only allow-list (composes
    sealed `assert_no_new_backend_computation`)."""


class ModalityLeafNotRecordingAtViewBoundary(
    CommissionViewBoundaryRefused, RecordingEvidenceKindMismatchError
):
    """§13.3 V121a verbatim: 'Modality appears at exactly one leaf: evidence
    inspection.'  Raised by `serve_recording_evidence_leaf` when the wrapped
    EvidenceRef.kind is not 'recording' (composes sealed
    `RecordingEvidenceLeaf.__post_init__` refusal)."""


# ---------------------------------------------------------------------------
# Four boundary callables · reads-only composition · no computation.
# ---------------------------------------------------------------------------


def enter_view_boundary_with_snapshot(
    *,
    snapshot: CommissionViewSnapshot,
) -> CommissionViewBoundaryResult_v1:
    """§13.2 V120b compose-boundary entry point.

    Reads the sealed `CommissionViewSnapshot` (already constructed via the
    sealed CP-M6-9-1 factory or bypass-constructed by a defence-in-depth
    caller) · invokes sealed `assert_commission_open_only_after_agreement`
    on the wrapped MilestoneList · then invokes sealed
    `render_commission_view` to produce the sealed `CommissionViewProjection`.

    Refuses `AgreementMissingAtViewBoundary` (which is <:
    `MilestoneListNotAgreedError` <: `CommissionOpenBeforeAgreementError`
    for full family-catch chain) if the milestone list is not agreed.

    Reads-only: does not derive any status · does not compute totals.
    """
    # V120b + V114c defence-in-depth via sealed refusal composition.
    try:
        assert_commission_open_only_after_agreement(
            milestone_list=snapshot.milestone_list
        )
    except CommissionOpenBeforeAgreementError as sealed_refusal:
        # Family-catch: surface as boundary refusal that still subclasses
        # the sealed refusal so downstream callers catching the sealed
        # type still see it (§13.2 V120b verbatim).
        raise AgreementMissingAtViewBoundary(str(sealed_refusal)) from sealed_refusal

    # Sealed render (also refuses on unagreed lists · defence-in-depth · no
    # computation beyond sealed reads).
    try:
        projection = render_commission_view(snapshot=snapshot)
    except MilestoneListNotAgreedError as sealed_render_refusal:
        raise AgreementMissingAtViewBoundary(
            str(sealed_render_refusal)
        ) from sealed_render_refusal

    return CommissionViewBoundaryResult_v1(
        projection=projection,
        snapshot=snapshot,
        posture_note=NO_BACKEND_COMPUTATION_V1_POSTURE,
    )


def assert_projection_is_reads_only_at_view_boundary(
    *,
    projection,
    snapshot: CommissionViewSnapshot,
) -> None:
    """§13.4 V122c verbatim (OWNER-PINNED): reads-only allow-list defence at
    the compose-boundary.  Composes sealed `assert_no_new_backend_computation`
    and re-raises as `NewBackendComputationAtViewBoundary` (family-catch
    preserved via multiple inheritance).

    NO computation performed here beyond forwarding to the sealed check.
    """
    try:
        assert_no_new_backend_computation(projection=projection, snapshot=snapshot)
    except NewBackendComputationError as sealed_refusal:
        raise NewBackendComputationAtViewBoundary(
            str(sealed_refusal)
        ) from sealed_refusal


def assert_projection_is_internals_free_at_view_boundary(
    *,
    projection,
) -> None:
    """§13.1 V119c verbatim: 'no surface is a rendering of backend internals.'
    Composes sealed `assert_no_internals_projected` and re-raises as
    `InternalsProjectedAtViewBoundary` (family-catch preserved via multiple
    inheritance).

    NO computation performed here beyond forwarding to the sealed check.
    """
    try:
        assert_no_internals_projected(projection=projection)
    except InternalsProjectedError as sealed_refusal:
        raise InternalsProjectedAtViewBoundary(
            str(sealed_refusal)
        ) from sealed_refusal


def serve_recording_evidence_leaf(
    *,
    evidence_ref: EvidenceRef,
    plays_at_timestamp: str,
    recording_provenance_ref: str,
) -> RecordingEvidenceLeaf:
    """§13.3 V121a + V121b verbatim: modality leaf is exactly evidence-inspection
    on a recording; the source plays at its timestamp.

    Composes sealed `RecordingEvidenceLeaf.__post_init__` (which refuses
    non-'recording' EvidenceRef.kind).  Returns the sealed carrier
    unchanged on the happy path · re-raises as
    `ModalityLeafNotRecordingAtViewBoundary` on refusal (family-catch
    preserved via multiple inheritance).

    NO computation performed here beyond composing sealed construction.
    §3.1 P038 tokens-not-waveforms preserved (no audio bytes cross the seam).
    """
    try:
        return RecordingEvidenceLeaf(
            evidence_ref=evidence_ref,
            plays_at_timestamp=plays_at_timestamp,
            recording_provenance_ref=recording_provenance_ref,
        )
    except RecordingEvidenceKindMismatchError as sealed_refusal:
        raise ModalityLeafNotRecordingAtViewBoundary(
            str(sealed_refusal)
        ) from sealed_refusal
