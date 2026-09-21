"""M6 · Audio-Plane v1.0 · CP-M6-9-1 + CP-M6-9-2 · §13 Commission View · schema + reads-only discipline + milestones-first render + modality leaf.

Verbatim canon anchors (single-line for gating-test docstring parity):

- §13.1 P216 (V119): "This surface adjustment applies to all commissioned work on the platform — extraction, census, and training commissions alike, across every extraction type. No modality receives its own UI, and no surface is a rendering of backend internals: rendering internals quietly commits the backend to building displayable versions of its own machinery."

- §13.2 P217 (V120 · LOAD-BEARING): "The surface is milestones. The artifacts are evidence behind them. At Sampling & Reflection, the proposed milestone list is presented to the objective owner for agreement. Commission does not open until it is agreed. The Commission View reports against the agreed checklist: each milestone with its done-condition and owner; status in plain terms — done, on track, behind, missed. Missed is shown as plainly as done. Spend against quote is shown at the same plain level. Technical material — calibration results, strata coverage, Collection Schema state — is drill-down evidence for whoever asks why a milestone reads as it does. It is never the front page."

- §13.3 P218 (V121): "Modality appears at exactly one leaf: evidence inspection. Where provenance resolves to a recording, the source plays at its timestamp rather than rendering as a page region — the existing trust-receipt pattern (\"a disputed number is answered by playing the tape\"), unchanged."

- §13.4 P219 (V122 · LOAD-BEARING · reads-only): "Milestones are records with done-conditions; the platform already stamps events. No new machinery is built for display. Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified."

CP-M6-9-1 (Part-A) lands the Commission View SCHEMA + reads-only discipline:
closed four-status enum (V120c) + status entries (V120c) + spend-against-quote
carrier (V120e reading CP-M6-7-3 CostQuoteWithCI · V122b reads existing
stamps) + evidence-ref subordinate carrier (V120f · never the front page) +
CommissionViewSnapshot 4-carrier composition + factory that gates on
V120b agreement (composes CP-M6-8-2 V114c).

CP-M6-9-2 (Part-B · append-only · CLOSES SUB-WAVE 9) lands the milestones-first
render (V120a) + modality leaf (V121) + internals-projection refusal (V119c) +
reads-only allow-list defence (V122c).

Wave-honest limits (per M6 SW9 grounding brief §D):

- Synthetic-fixture-safe.  No real estate data.
- V121b recording-modality is a REF-carrier only (opaque timestamp + provenance ref).  No audio bytes cross the seam.
- V119c internals-projection refusal is redacted-field-name based (not total defence).
- V122c reads-only defence is an allow-list of carrier types authored this sub-wave.
- No LLM / HTTP / filesystem / network.  Case-agnostic.
- §3.1 P038 tokens-not-waveforms preserved.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Tuple

from services.audio_plane_v1.milestones import (
    CommissionOpenBeforeAgreementError,
    MilestoneList,
)

__all__ = (
    "MILESTONE_STATUS_VALUES",
    "MilestoneStatusEntry",
    "SpendAgainstQuote",
    "EvidenceRef",
    "CommissionViewSnapshot",
    "construct_commission_view_snapshot",
    "MilestoneStatusInvalidError",
    "MilestoneListNotAgreedError",
    "StatusEntryCountMismatchError",
    "EvidenceKindInvalidError",
    # ---- Part-B (CP-M6-9-2 · §13.2 render + §13.3 modality + V119c + V122c) ----
    "CommissionViewProjection",
    "MilestoneRow",
    "render_commission_view",
    "RecordingEvidenceLeaf",
    "assert_no_internals_projected",
    "assert_no_new_backend_computation",
    "RecordingEvidenceKindMismatchError",
    "InternalsProjectedError",
    "NewBackendComputationError",
)


# ---------------------------------------------------------------------------
# Closed-set discipline (V120c · V120f)
# ---------------------------------------------------------------------------


MILESTONE_STATUS_VALUES: frozenset = frozenset({
    "done",
    "on_track",
    "behind",
    "missed",
})
"""§13.2 V120c verbatim: 'status in plain terms — done, on track, behind, missed.'

Closed four-token enum.  Any expansion is a §13.2 amendment · not a silent
addition (per M6 SW9 grounding brief §D wave-honest limit 4).
"""


_EVIDENCE_KIND_VALUES: frozenset = frozenset({
    "calibration",
    "strata_coverage",
    "collection_schema",
    "recording",
})


# ---------------------------------------------------------------------------
# Refusals (V120c · V120b · V120e · V120f)
# ---------------------------------------------------------------------------


class MilestoneStatusInvalidError(Exception):
    """§13.2 V120c: 'status in plain terms — done, on track, behind, missed.'
    Raised at MilestoneStatusEntry.__post_init__ when status is not one of
    the four canonical tokens."""


class MilestoneListNotAgreedError(CommissionOpenBeforeAgreementError):
    """§13.2 V120b: 'Commission does not open until it is agreed.'  Composes
    CP-M6-8-2 V114c: subclass of CommissionOpenBeforeAgreementError so that
    a family-catch on the CP-M6-8-2 refusal captures this refusal too."""


class StatusEntryCountMismatchError(Exception):
    """§13.2 V120c parity: exactly one status entry per milestone.  Raised
    at construct_commission_view_snapshot when len(statuses) !=
    len(milestone_list.milestones)."""


class StatusEntryOrderingMismatchError(Exception):
    """§13.2 V120a + §11.3 V114a: milestones-first + ordering-load-bearing.
    Raised at construct_commission_view_snapshot when statuses'
    milestone_ref sequence does not align with milestone_list's
    milestones[i].milestone_id sequence in order."""


class SpendAgainstQuoteRefMissingError(Exception):
    """§13.2 V120e + §13.4 V122b: SpendAgainstQuote reads existing event
    stamps · caller supplies the aggregate + the ref to the CP-M6-7-3
    CostQuoteWithCI.  Raised at SpendAgainstQuote.__post_init__ when
    cost_quote_ref is empty."""


class EvidenceKindInvalidError(Exception):
    """§13.2 V120f: 'Technical material — calibration results, strata
    coverage, Collection Schema state — is drill-down evidence.'  Raised
    at EvidenceRef.__post_init__ when kind is not one of the four canonical
    drill-down kinds."""


# ---------------------------------------------------------------------------
# Carriers (V120c · V120e · V120f · V122a)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MilestoneStatusEntry:
    """§13.2 V120c: 'each milestone with its done-condition and owner; status
    in plain terms — done, on track, behind, missed.'

    Frozen 2-carrier: milestone_ref (FK by milestone_id) + status (must be
    in MILESTONE_STATUS_VALUES).
    """

    milestone_ref: str
    status: str

    def __post_init__(self) -> None:
        if self.status not in MILESTONE_STATUS_VALUES:
            raise MilestoneStatusInvalidError(
                f"status={self.status!r} not in canonical four-set "
                f"{sorted(MILESTONE_STATUS_VALUES)!r} "
                "(V120c · P217 'status in plain terms — done, on track, "
                "behind, missed')."
            )


@dataclass(frozen=True)
class SpendAgainstQuote:
    """§13.2 V120e + §13.4 V122b: 'Spend against quote is shown at the same
    plain level' + 'the platform already stamps events'.

    Frozen 2-carrier: actual (aggregate provided by caller · not computed
    here per V122c) + cost_quote_ref (opaque ref to a CP-M6-7-3
    CostQuoteWithCI · reads existing carrier).
    """

    actual: float
    cost_quote_ref: str

    def __post_init__(self) -> None:
        if not self.cost_quote_ref:
            raise SpendAgainstQuoteRefMissingError(
                "SpendAgainstQuote.cost_quote_ref must be a non-empty "
                "opaque ref to a CP-M6-7-3 CostQuoteWithCI "
                "(V120e · V122b · reads existing carrier)."
            )


@dataclass(frozen=True)
class EvidenceRef:
    """§13.2 V120f: 'Technical material — calibration results, strata
    coverage, Collection Schema state — is drill-down evidence for whoever
    asks why a milestone reads as it does. It is never the front page.'

    Frozen 2-carrier: kind (closed four-set) + ref (opaque).
    """

    kind: str
    ref: str

    def __post_init__(self) -> None:
        if self.kind not in _EVIDENCE_KIND_VALUES:
            raise EvidenceKindInvalidError(
                f"evidence kind={self.kind!r} not in canonical four-set "
                f"{sorted(_EVIDENCE_KIND_VALUES)!r} "
                "(V120f · P217 'drill-down evidence for whoever asks why "
                "a milestone reads as it does')."
            )


@dataclass(frozen=True)
class CommissionViewSnapshot:
    """§13 Commission View snapshot · V120a milestones-first · V122a
    milestones-are-records-with-done-conditions (imports CP-M6-8-2
    MilestoneList verbatim; no new milestone shape carrier).

    Frozen 4-carrier: milestone_list (CP-M6-8-2) + statuses + spend +
    evidence_refs.  Constructed via construct_commission_view_snapshot,
    which enforces V120b agreement gate + V120c parity + V120a/V114a
    ordering-alignment.
    """

    milestone_list: MilestoneList
    statuses: Tuple[MilestoneStatusEntry, ...]
    spend: SpendAgainstQuote
    evidence_refs: Tuple[EvidenceRef, ...]


# ---------------------------------------------------------------------------
# Factory + agreement gate (V120b · V120c parity · V120a/V114a ordering)
# ---------------------------------------------------------------------------


def construct_commission_view_snapshot(
    *,
    milestone_list: MilestoneList,
    statuses: Tuple[MilestoneStatusEntry, ...],
    spend: SpendAgainstQuote,
    evidence_refs: Tuple[EvidenceRef, ...],
) -> CommissionViewSnapshot:
    """Factory · composes CP-M6-8-2 MilestoneList + this-module carriers.

    Refusals:
      - MilestoneListNotAgreedError (V120b · composes CP-M6-8-2 V114c ·
        subclass of CommissionOpenBeforeAgreementError · family-catch
        preserved).
      - StatusEntryCountMismatchError (V120c · exactly one status per
        milestone).
      - StatusEntryOrderingMismatchError (V120a milestones-first + V114a
        ordering-load-bearing).
    """
    # V120b: Commission does not open until it is agreed.
    if milestone_list.commission_agreement_ref is None:
        raise MilestoneListNotAgreedError(
            "milestone list is not agreed; the Commission View may not be "
            "constructed until the objective owner reviews and agrees "
            "(V120b · P217 'Commission does not open until it is agreed' · "
            "composes CP-M6-8-2 V114c)."
        )
    # V120c parity: exactly one status per milestone.
    if len(statuses) != len(milestone_list.milestones):
        raise StatusEntryCountMismatchError(
            f"statuses count={len(statuses)} does not match milestones "
            f"count={len(milestone_list.milestones)} "
            "(V120c · P217 'each milestone with its done-condition and "
            "owner; status in plain terms')."
        )
    # V120a/V114a: ordering-load-bearing.
    for i, (m, s) in enumerate(zip(milestone_list.milestones, statuses)):
        if s.milestone_ref != m.milestone_id:
            raise StatusEntryOrderingMismatchError(
                f"status[{i}].milestone_ref={s.milestone_ref!r} does not "
                f"align with milestones[{i}].milestone_id={m.milestone_id!r} "
                "(V120a milestones-first + V114a 'a proposed milestone "
                "list — the checklist of what must be done, in what order')."
            )
    return CommissionViewSnapshot(
        milestone_list=milestone_list,
        statuses=statuses,
        spend=spend,
        evidence_refs=evidence_refs,
    )


# ---------------------------------------------------------------------------
# Part-B · CP-M6-9-2 · §13.2 render + §13.3 modality + V119c + V122c
# (append-only extension · CLOSES SUB-WAVE 9)
# ---------------------------------------------------------------------------


# Refusals (V121b · V119c · V122c)


class RecordingEvidenceKindMismatchError(Exception):
    """§13.3 V121a: 'Modality appears at exactly one leaf: evidence
    inspection.'  RecordingEvidenceLeaf accepts ONLY kind=='recording'.
    Raised at RecordingEvidenceLeaf.__post_init__ when the wrapped
    EvidenceRef.kind is not 'recording'."""


class InternalsProjectedError(Exception):
    """§13.1 V119c: 'no surface is a rendering of backend internals'.
    Raised by assert_no_internals_projected when the projection carries
    any field whose name matches the forbidden-name closed-set."""


class NewBackendComputationError(Exception):
    """§13.4 V122c: 'No new machinery is built for display. Any surface
    element in this section found to require new backend computation
    beyond reading existing artifacts is out of specification'.  Raised
    by assert_no_new_backend_computation when the projection carries
    a carrier type outside the allow-list authored this sub-wave."""


# Carriers (V120a · V121b)


@dataclass(frozen=True)
class MilestoneRow:
    """§13.2 V120a milestones-first head row.  Reads Milestone +
    MilestoneStatusEntry.  No new fields · no evidence content.

    Frozen 4-carrier: milestone_id + done_condition + owner + status.
    """

    milestone_id: str
    done_condition: str
    owner: str
    status: str


@dataclass(frozen=True)
class RecordingEvidenceLeaf:
    """§13.3 V121b: 'Where provenance resolves to a recording, the source
    plays at its timestamp rather than rendering as a page region'.

    Frozen 3-carrier: evidence_ref (must be kind=='recording') +
    plays_at_timestamp (opaque ISO-8601-shaped string) +
    recording_provenance_ref (opaque · no audio bytes cross the seam ·
    §3.1 P038 preserved).
    """

    evidence_ref: "EvidenceRef"
    plays_at_timestamp: str
    recording_provenance_ref: str

    def __post_init__(self) -> None:
        if self.evidence_ref.kind != "recording":
            raise RecordingEvidenceKindMismatchError(
                f"RecordingEvidenceLeaf requires EvidenceRef.kind == "
                f"'recording'; got {self.evidence_ref.kind!r} "
                "(V121a · P218 'Modality appears at exactly one leaf: "
                "evidence inspection')."
            )


@dataclass(frozen=True)
class CommissionViewProjection:
    """§13.2 V120a milestones-first projection.

    Frozen 4-carrier:
      - milestones_head: ordered tuple of MilestoneRow (front page · V120a).
      - spend_head: SpendAgainstQuote (V120e "same plain level").
      - evidence_leaves: ordered tuple of EvidenceRef (V120f · body · never
        the front page).
      - snapshot_ref: opaque ref back to the source snapshot.
    """

    milestones_head: Tuple[MilestoneRow, ...]
    spend_head: SpendAgainstQuote
    evidence_leaves: Tuple["EvidenceRef", ...]
    snapshot_ref: str


# Render (V120a milestones-first · V120b defence-in-depth)


def render_commission_view(
    *,
    snapshot: CommissionViewSnapshot,
) -> CommissionViewProjection:
    """§13.2 V120a milestones-first render.  Deterministic projection
    from a CommissionViewSnapshot: iterates milestones in order (V114a
    ordering-load-bearing), zips with statuses (V120c parity), assembles
    MilestoneRow head list.  Spend at the same plain level (V120e).
    Evidence at the leaf (V120f · never the front page).

    Defence-in-depth: even if a caller bypasses the CP-M6-9-1 factory
    (e.g. constructs a CommissionViewSnapshot directly with an unagreed
    milestone list), this render refuses via MilestoneListNotAgreedError
    (family-catch preserved: MilestoneListNotAgreedError <:
    CommissionOpenBeforeAgreementError).
    """
    if snapshot.milestone_list.commission_agreement_ref is None:
        raise MilestoneListNotAgreedError(
            "cannot render Commission View for an unagreed milestone "
            "list (V120b · P217 'Commission does not open until it is "
            "agreed' · defence-in-depth)."
        )
    rows = tuple(
        MilestoneRow(
            milestone_id=m.milestone_id,
            done_condition=m.done_condition,
            owner=m.owner,
            status=s.status,
        )
        for m, s in zip(snapshot.milestone_list.milestones, snapshot.statuses)
    )
    return CommissionViewProjection(
        milestones_head=rows,
        spend_head=snapshot.spend,
        evidence_leaves=snapshot.evidence_refs,
        snapshot_ref=snapshot.milestone_list.commission_id,
    )


# V119c internals-projection refusal


_INTERNALS_FORBIDDEN_FIELD_NAMES: frozenset = frozenset({
    "ratchet",
    "invariant",
    "seam",
    "pytest_stripped_sha256",
    "mongodb_",
    "redis_",
    "http_",
    "grpc_",
    "backend_",
})


def assert_no_internals_projected(*, projection) -> None:
    """§13.1 V119c refusal: 'no surface is a rendering of backend
    internals: rendering internals quietly commits the backend to
    building displayable versions of its own machinery'.

    Walks dataclasses.fields(projection) field names.  Refuses if any
    field name matches (equals or is prefixed by) an entry in the
    forbidden-name closed-set.  Wave-honest limit: this is a
    name-scan defence · not a total defence against internals leakage.
    """
    for f in dataclasses.fields(projection):
        for forbidden in _INTERNALS_FORBIDDEN_FIELD_NAMES:
            if f.name == forbidden or f.name.startswith(forbidden):
                raise InternalsProjectedError(
                    f"projection field {f.name!r} matches forbidden "
                    f"internals-name entry {forbidden!r} "
                    "(V119c · P216 'no surface is a rendering of backend "
                    "internals')."
                )


# V122c reads-only allow-list defence


_READS_ONLY_ALLOWLIST_CARRIER_TYPE_NAMES: frozenset = frozenset({
    "CommissionViewProjection",
    "MilestoneRow",
    "SpendAgainstQuote",
    "EvidenceRef",
    "RecordingEvidenceLeaf",
})


def assert_no_new_backend_computation(
    *,
    projection,
    snapshot: CommissionViewSnapshot,
) -> None:
    """§13.4 V122c refusal: 'No new machinery is built for display. Any
    surface element in this section found to require new backend
    computation beyond reading existing artifacts is out of specification
    and must be removed or re-specified'.

    Checks:
      1. type(projection).__name__ must be in the allow-list of carrier
         types authored this sub-wave.
      2. Each entry in projection.evidence_leaves (if any) must be an
         instance of EvidenceRef or a subclass whose type name is in the
         allow-list.

    Wave-honest limit: this is an authoring-boundary allow-list defence.
    A carrier legitimately named CommissionViewProjection that computed
    new totals internally is not caught by name-scan alone · caller-side
    integration tests carry the total discipline.
    """
    proj_type = type(projection).__name__
    if proj_type not in _READS_ONLY_ALLOWLIST_CARRIER_TYPE_NAMES:
        raise NewBackendComputationError(
            f"projection carrier type {proj_type!r} is not in the "
            f"reads-only allow-list "
            f"{sorted(_READS_ONLY_ALLOWLIST_CARRIER_TYPE_NAMES)!r} "
            "(V122c · P219 'No new machinery is built for display')."
        )
    leaves = getattr(projection, "evidence_leaves", ())
    for leaf in leaves:
        leaf_type = type(leaf).__name__
        if leaf_type not in _READS_ONLY_ALLOWLIST_CARRIER_TYPE_NAMES:
            raise NewBackendComputationError(
                f"projection.evidence_leaves carrier type "
                f"{leaf_type!r} is not in the reads-only allow-list "
                f"{sorted(_READS_ONLY_ALLOWLIST_CARRIER_TYPE_NAMES)!r} "
                "(V122c · P219 'No new machinery is built for display')."
            )
    # snapshot is a caller-supplied ref; V122c reads-only defence at
    # authoring surface does not walk snapshot internals (already gated
    # by CP-M6-9-1 factory).  The parameter is preserved for future
    # cross-reference checks.
    _ = snapshot
