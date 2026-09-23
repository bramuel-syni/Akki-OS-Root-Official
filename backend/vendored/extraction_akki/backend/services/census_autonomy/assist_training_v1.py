"""CP-AIP-ASSIST-TRAINING · assist_training_v1 · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md Item 5.11.g
CP-AIP-ASSIST-TRAINING and nothing else. Additive-only per SO §3.8.
Sealed CP-AIP-ASSIST-CENSUS (Item 5.11.f) + CP-TRACK-4-AUTONOMY-WIRING
(Item 5.11.e) + CP-AIP-10-TRAINING-RUNS + all prior sealed carriers
UNCHANGED. Terminal pytest only. RED-first mechanical.

Owner directive verbatim (SO §6.9 amendment + owner drop 2026-02-23
`STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md`):

Six binding conditions verbatim — applied to training-run dialogue:
    (1) No path to any decision (negative-scan import isolation)
    (2) Confirmed turns only banked (A5.16 receipted provenance)
    (3) Training assistant read-only against Registry (B5.1 byte-identical
        training-run commission with/without assistant)
    (4) MOAC criteria owner-set only at commission time (frozen at
        owner confirmation)
    (5) Content generated · chat surface · anchored · gated
        (R-32/A5.15/CON-6)
    (6) No learning from dialogue (L-4/L-5 only admission path)

Placement OUTSIDE the TCB. Every user-facing string is a Content
Registry entry.

Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: E1 wires the seam INTO
Census Autonomy Service; pod is never data path. Training compute +
model weights + labelled corpus NEVER leave Akki's boundary.

§1.2 modality-extension composing sealed CP-AIP-ASSIST-CENSUS
(assist_census_v1) by identity — never redeclare sealed symbols.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Final, Optional, Tuple

# §1.2 modality-extension: compose sealed CP-AIP-ASSIST-CENSUS symbols by identity.
# Import them so downstream users can access without redeclaration.
from backend.services.census_autonomy.assist_census_v1 import (
    AssistCensusBoundaryRefused as _AssistCensusBoundaryRefused,
    ContentRegistryEntry_v1 as _ContentRegistryEntry_v1,
    render_content_registry_entry as _render_content_registry_entry,
)


# ---------------------------------------------------------------------------
# Refusal hierarchy — extends sealed CP-AIP-ASSIST-CENSUS base by identity
# ---------------------------------------------------------------------------


class UnconfirmedTrainingTurnBankRefused(_AssistCensusBoundaryRefused):
    """Binding condition (2): unconfirmed training-assistant turn refused."""


class UngatedTrainingContentRefused(_AssistCensusBoundaryRefused):
    """Binding condition (5): training-content without A5.15+CON-6 refused."""


class FrozenMoacEditRefused(_AssistCensusBoundaryRefused):
    """Binding condition (4): editing MOAC after owner-confirmation freeze refused."""


class LearningWriteFromDialogueRefused(_AssistCensusBoundaryRefused):
    """Binding condition (6): dialogue-fed learning refused."""


class PodIsNeverDataPathAtAssistTrainingError(_AssistCensusBoundaryRefused):
    """Ruling (b) verbatim: pod is never data path — refuses pod://* / /app/* refs
    at training-assistant boundary callables."""


# ---------------------------------------------------------------------------
# Posture markers (Final str · owner verbatim)
# ---------------------------------------------------------------------------


ASSIST_TRAINING_READONLY_POSTURE: Final[str] = (
    "CP-AIP-ASSIST-TRAINING binding condition (3) verbatim: 'Training "
    "assistant read-only against Registry (B5.1 byte-identical training-"
    "run commission with/without assistant).' The training assistant "
    "MUST NOT write to the Registry. B5.1 byte-identity: a training-run "
    "commission derived WITH assistant activation is byte-identical to a "
    "commission derived WITHOUT assistant activation, given identical "
    "Registry state."
)


MOAC_OWNER_SET_ONLY_AT_COMMISSION_POSTURE_TRAINING: Final[str] = (
    "CP-AIP-ASSIST-TRAINING binding condition (4) verbatim: 'MOAC "
    "criteria owner-set only at commission time (frozen at owner "
    "confirmation).' The training assistant proposes; the owner confirms; "
    "on confirmation MOAC becomes owner-set only and the commission "
    "FREEZES. Subsequent turns propose a NEW commission superseding the "
    "prior; the frozen carrier is NEVER edited in place."
)


NO_LEARNING_FROM_DIALOGUE_POSTURE_TRAINING: Final[str] = (
    "CP-AIP-ASSIST-TRAINING binding condition (6) verbatim: 'No learning "
    "from dialogue (L-4/L-5 only admission path).' Training-assistant "
    "dialogue MUST NEVER feed training material. L-4/L-5 is the only "
    "admission path for training material. The training-assistant module "
    "exposes ZERO learning-write callables + ZERO weight-export callables."
)


PLACEMENT_OUTSIDE_TCB_POSTURE_TRAINING: Final[str] = (
    "CP-AIP-ASSIST-TRAINING placement verbatim: 'Placement OUTSIDE the "
    "TCB.' The training-assistant module is not part of the Trusted "
    "Computing Base; every user-facing string it renders is a Content "
    "Registry entry with an A5.15 anchor and CON-6 gate; the assistant "
    "cannot cross into any decision boundary of the TCB (binding "
    "condition 1 negative-scan import isolation enforces this)."
)


WEIGHTS_CORPUS_NEVER_LEAVE_AKKI_POSTURE: Final[str] = (
    "CP-AIP-ASSIST-TRAINING Ruling (b) verbatim 2026-02-23: 'Training "
    "compute, model weights, and the labelled corpus never leave Akki's "
    "boundary; no third-party export.' The training-assistant module "
    "MUST NOT expose any callable returning weight bytes, corpus payload, "
    "or model internals. E1 wires the seam INTO Census Autonomy Service; "
    "pod is never data path."
)


SIX_BINDING_CONDITIONS_POSTURE_TRAINING: Final[Tuple[str, str, str, str, str, str]] = (
    "(1) No path to any decision (negative-scan import isolation).",
    "(2) Confirmed turns only banked (A5.16 receipted provenance).",
    "(3) Training assistant read-only against Registry (B5.1 byte-"
    "identical training-run commission with/without assistant).",
    "(4) MOAC criteria owner-set only at commission time (frozen at "
    "owner confirmation).",
    "(5) Content generated · chat surface · anchored · gated (R-32/A5.15/CON-6) "
    "with §6.9 markers over refusal where a marker makes the state honest.",
    "(6) No learning from dialogue (L-4/L-5 only admission path).",
)


# ---------------------------------------------------------------------------
# Frozen carriers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TrainingAssistantConfirmedTurn_v1:
    """A single confirmed training-assistant/owner turn — banked with A5.16
    provenance + reference to the proposed training commission.
    """
    session_id: str
    tenant_id: str
    role: str  # "assistant" | "owner"
    content_registry_ref: str
    confirmed_by_owner: bool
    confirmed_at_utc: str
    a5_16_receipt_ref: str
    proposed_training_commission_ref: str


@dataclass(frozen=True)
class TrainingCommissionProposal_v1:
    """A proposed training commission — model + data slice + calibration +
    cost/CI + MOAC freeze state. Frozen dataclass; freeze semantics via
    `freeze_training_commission_on_owner_confirm` producing a NEW instance.
    """
    model_choice_ref: str
    data_slice_ref: str
    calibration_stage_ref: str
    cost_ci_quote_ref: str
    moac_frozen: bool
    frozen_at_utc: str


# ---------------------------------------------------------------------------
# Boundary callables
# ---------------------------------------------------------------------------


def bank_confirmed_training_turn(
    *,
    session_id: str,
    tenant_id: str,
    role: str,
    content_registry_ref: str,
    confirmed_by_owner: bool,
    confirmed_at_utc: Optional[str],
    a5_16_receipt_ref: str,
    proposed_training_commission_ref: str,
) -> TrainingAssistantConfirmedTurn_v1:
    """Bank a confirmed training-assistant/owner turn with A5.16 provenance.

    Refuses:
    - `confirmed_by_owner is False` → `UnconfirmedTrainingTurnBankRefused`.
    - `a5_16_receipt_ref` empty/malformed → `UnconfirmedTrainingTurnBankRefused`.
    - `proposed_training_commission_ref` empty → `UnconfirmedTrainingTurnBankRefused`.
    - session_id/tenant_id/content_registry_ref starting with `pod://` or `/app/`
      → `PodIsNeverDataPathAtAssistTrainingError` (Ruling (b) verbatim).
    """
    for ref, name in (
        (session_id, "session_id"),
        (tenant_id, "tenant_id"),
        (content_registry_ref, "content_registry_ref"),
        (proposed_training_commission_ref, "proposed_training_commission_ref"),
    ):
        if isinstance(ref, str) and (ref.startswith("pod://") or ref.startswith("/app/")):
            raise PodIsNeverDataPathAtAssistTrainingError(
                f"Ruling (b) verbatim: pod is never data path. "
                f"{name}={ref!r} refused at training-assistant boundary."
            )
    if not confirmed_by_owner:
        raise UnconfirmedTrainingTurnBankRefused(
            "Binding condition (2) verbatim: 'Confirmed turns only banked.' "
            "Unconfirmed training-assistant turn refused at boundary."
        )
    if not a5_16_receipt_ref or not a5_16_receipt_ref.startswith("a5_16://"):
        raise UnconfirmedTrainingTurnBankRefused(
            "Binding condition (2) verbatim: 'A5.16 receipted provenance.' "
            f"a5_16_receipt_ref={a5_16_receipt_ref!r} refused."
        )
    if not proposed_training_commission_ref:
        raise UnconfirmedTrainingTurnBankRefused(
            "Training-turn bank refused: proposed_training_commission_ref "
            "empty; every training turn references a commission proposal."
        )
    return TrainingAssistantConfirmedTurn_v1(
        session_id=session_id,
        tenant_id=tenant_id,
        role=role,
        content_registry_ref=content_registry_ref,
        confirmed_by_owner=True,
        confirmed_at_utc=confirmed_at_utc or "",
        a5_16_receipt_ref=a5_16_receipt_ref,
        proposed_training_commission_ref=proposed_training_commission_ref,
    )


def render_training_content_registry_entry(
    *,
    content_registry_ref: str,
    a5_15_anchor_ref: str,
    con_6_gate_ref: str,
    honest_marker: Optional[str],
) -> _ContentRegistryEntry_v1:
    """Render a training-scope user-facing content-registry entry.

    Composes sealed CP-AIP-ASSIST-CENSUS `render_content_registry_entry` by
    identity + retags refusal class to `UngatedTrainingContentRefused` for
    training-scope discrimination.

    Refuses:
    - missing/empty `a5_15_anchor_ref` → `UngatedTrainingContentRefused`.
    - missing/empty `con_6_gate_ref` → `UngatedTrainingContentRefused`.
    """
    if not a5_15_anchor_ref or not a5_15_anchor_ref.startswith("a5_15://"):
        raise UngatedTrainingContentRefused(
            "Binding condition (5) verbatim: 'Content generated · chat "
            "surface · anchored · gated (R-32/A5.15/CON-6).' Missing "
            f"a5_15_anchor_ref={a5_15_anchor_ref!r}."
        )
    if not con_6_gate_ref or not con_6_gate_ref.startswith("con_6://"):
        raise UngatedTrainingContentRefused(
            "Binding condition (5) verbatim: 'CON-6 gated content.' "
            f"Missing con_6_gate_ref={con_6_gate_ref!r}."
        )
    # Compose sealed 5.11.f callable by identity for the actual construction
    return _render_content_registry_entry(
        content_registry_ref=content_registry_ref,
        a5_15_anchor_ref=a5_15_anchor_ref,
        con_6_gate_ref=con_6_gate_ref,
        honest_marker=honest_marker,
    )


def freeze_training_commission_on_owner_confirm(
    *,
    proposal: TrainingCommissionProposal_v1,
    owner_confirmation_ref: str,
    frozen_at_utc: str,
) -> TrainingCommissionProposal_v1:
    """Freeze a proposed training commission on owner confirmation.

    Returns a NEW frozen instance with `moac_frozen=True` +
    `frozen_at_utc` set. The input proposal (frozen dataclass) is not
    mutated. Subsequent freeze calls on the returned carrier are refused
    with `FrozenMoacEditRefused`.

    Refuses:
    - proposal already `moac_frozen=True` → `FrozenMoacEditRefused`.
    - missing/malformed `owner_confirmation_ref` → `UnconfirmedTrainingTurnBankRefused`.
    """
    if proposal.moac_frozen:
        raise FrozenMoacEditRefused(
            "Binding condition (4) verbatim: 'MOAC criteria owner-set only "
            "at commission time.' Frozen commission already frozen at "
            f"{proposal.frozen_at_utc}; edit refused."
        )
    if not owner_confirmation_ref or not owner_confirmation_ref.startswith("a5_16://"):
        raise UnconfirmedTrainingTurnBankRefused(
            "freeze_training_commission_on_owner_confirm: "
            f"owner_confirmation_ref={owner_confirmation_ref!r} refused."
        )
    return replace(proposal, moac_frozen=True, frozen_at_utc=frozen_at_utc)
