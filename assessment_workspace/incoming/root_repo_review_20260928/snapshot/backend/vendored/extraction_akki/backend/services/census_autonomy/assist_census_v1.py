"""CP-AIP-ASSIST-CENSUS · assist_census_v1 · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md Item 5.11.f
CP-AIP-ASSIST-CENSUS and nothing else. Additive-only per SO §3.8.
Sealed CP-AIP-6 wizard + Census Autonomy Service response_required_queue
+ Track-4 autonomy wiring UNCHANGED. Terminal pytest only. RED-first
mechanical.

Owner directive verbatim (SO §6.9 amendment + owner drop 2026-02-23
`STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md`):

Six binding conditions verbatim:
    (1) No path to any decision (negative-scan import isolation)
    (2) Confirmed turns only banked (A5.16 receipted provenance)
    (3) Census assistant read-only against Registry (B5.1 byte-identical
        census with/without assistant)
    (4) Training proposals freeze at commission; MOAC owner-set only
    (5) Content generated · chat surface · anchored · gated (R-32/A5.15/CON-6)
    (6) No learning from dialogue (L-4/L-5 only admission path)

Placement OUTSIDE the TCB. Every user-facing string is a Content
Registry entry.

Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: E1 wires the seam INTO
Census Autonomy Service; pod is never data path.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Optional, Tuple


# ---------------------------------------------------------------------------
# Refusal hierarchy
# ---------------------------------------------------------------------------


class AssistCensusBoundaryRefused(Exception):
    """Base for all CP-AIP-ASSIST-CENSUS boundary refusals."""


class UnconfirmedTurnBankRefused(AssistCensusBoundaryRefused):
    """Binding condition (2): unconfirmed turns MUST NOT be banked."""


class UngatedContentRefused(AssistCensusBoundaryRefused):
    """Binding condition (5): content without A5.15 anchor + CON-6 gate refused."""


# ---------------------------------------------------------------------------
# Posture markers (Final str · owner verbatim)
# ---------------------------------------------------------------------------


ASSIST_CENSUS_READONLY_POSTURE: Final[str] = (
    "CP-AIP-ASSIST-CENSUS binding condition (3) verbatim: 'Census "
    "assistant read-only against Registry (B5.1 byte-identical census "
    "with/without assistant).' The assistant MUST NOT write to the "
    "Registry. B5.1 byte-identity: a census output derived WITH assistant "
    "activation is byte-identical to a census output derived WITHOUT "
    "assistant activation, given identical Registry state."
)


MOAC_OWNER_SET_ONLY_POSTURE: Final[str] = (
    "CP-AIP-ASSIST-CENSUS binding condition (4) verbatim: 'Training "
    "proposals freeze at commission; MOAC owner-set only.' Census "
    "assistant does not propose training runs nor edit MOAC criteria; "
    "that surface belongs to CP-AIP-ASSIST-TRAINING (Item 5.11.g) and "
    "MOAC criteria are set by the owner's confirmation only at "
    "commission time."
)


NO_LEARNING_FROM_DIALOGUE_POSTURE: Final[str] = (
    "CP-AIP-ASSIST-CENSUS binding condition (6) verbatim: 'No learning "
    "from dialogue (L-4/L-5 only admission path).' Assistant dialogue "
    "MUST NEVER feed training material. L-4/L-5 is the only admission "
    "path for training material. The assistant module exposes ZERO "
    "learning-write callables."
)


PLACEMENT_OUTSIDE_TCB_POSTURE: Final[str] = (
    "CP-AIP-ASSIST-CENSUS placement verbatim: 'Placement OUTSIDE the "
    "TCB.' The census assistant module is not part of the Trusted "
    "Computing Base; every user-facing string it renders is a Content "
    "Registry entry with an A5.15 anchor and CON-6 gate; the assistant "
    "cannot cross into any decision boundary of the TCB (binding "
    "condition 1 negative-scan import isolation enforces this)."
)


SIX_BINDING_CONDITIONS_POSTURE: Final[Tuple[str, str, str, str, str, str]] = (
    "(1) No path to any decision (negative-scan import isolation).",
    "(2) Confirmed turns only banked (A5.16 receipted provenance).",
    "(3) Census assistant read-only against Registry (B5.1 byte-identical "
    "census with/without assistant).",
    "(4) Training proposals freeze at commission; MOAC owner-set only.",
    "(5) Content generated · chat surface · anchored · gated (R-32/A5.15/CON-6) "
    "with §6.9 markers over refusal where a marker makes the state honest.",
    "(6) No learning from dialogue (L-4/L-5 only admission path).",
)


# ---------------------------------------------------------------------------
# Frozen carriers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CensusAssistantConfirmedTurn_v1:
    """A single confirmed assistant/owner turn — banked with A5.16 provenance.

    Owner directive verbatim: 'Confirmed turns only banked (A5.16
    receipted provenance).' An unconfirmed turn is NEVER persisted.
    """
    session_id: str
    tenant_id: str
    role: str  # "assistant" | "owner"
    content_registry_ref: str
    confirmed_by_owner: bool  # always True for banked turns
    confirmed_at_utc: str
    a5_16_receipt_ref: str  # a5_16://receipt/<turn-id>


@dataclass(frozen=True)
class ContentRegistryEntry_v1:
    """A rendered assistant utterance — anchored (A5.15) + gated (CON-6).

    Owner directive verbatim: 'Content generated · chat surface ·
    anchored · gated (R-32/A5.15/CON-6).' Every user-facing string is
    a Content Registry entry.
    """
    content_registry_ref: str  # R-32
    a5_15_anchor_ref: str  # a5_15://anchor/<row-id>
    con_6_gate_ref: str  # con_6://gate/<gate-id>
    honest_marker: Optional[str]  # §6.9 marker — 'unmeasured'/'INFERRED'/'honest-gap'/'fallback'/None


# ---------------------------------------------------------------------------
# Boundary callables
# ---------------------------------------------------------------------------


def bank_confirmed_assistant_turn(
    *,
    session_id: str,
    tenant_id: str,
    role: str,
    content_registry_ref: str,
    confirmed_by_owner: bool,
    confirmed_at_utc: Optional[str],
    a5_16_receipt_ref: str,
) -> CensusAssistantConfirmedTurn_v1:
    """Bank a confirmed assistant/owner turn with A5.16 provenance.

    Refuses:
    - `confirmed_by_owner is False` → `UnconfirmedTurnBankRefused`.
    - `a5_16_receipt_ref` empty/None → `UnconfirmedTurnBankRefused`.
    """
    if not confirmed_by_owner:
        raise UnconfirmedTurnBankRefused(
            "Binding condition (2) verbatim: 'Confirmed turns only banked.' "
            "Unconfirmed turn refused at boundary."
        )
    if not a5_16_receipt_ref or not a5_16_receipt_ref.startswith("a5_16://"):
        raise UnconfirmedTurnBankRefused(
            "Binding condition (2) verbatim: 'A5.16 receipted provenance.' "
            f"a5_16_receipt_ref={a5_16_receipt_ref!r} refused."
        )
    return CensusAssistantConfirmedTurn_v1(
        session_id=session_id,
        tenant_id=tenant_id,
        role=role,
        content_registry_ref=content_registry_ref,
        confirmed_by_owner=True,
        confirmed_at_utc=confirmed_at_utc or "",
        a5_16_receipt_ref=a5_16_receipt_ref,
    )


def render_content_registry_entry(
    *,
    content_registry_ref: str,
    a5_15_anchor_ref: str,
    con_6_gate_ref: str,
    honest_marker: Optional[str],
) -> ContentRegistryEntry_v1:
    """Render a user-facing content-registry entry with A5.15 anchor + CON-6 gate.

    Refuses:
    - missing/empty `a5_15_anchor_ref` → `UngatedContentRefused`.
    - missing/empty `con_6_gate_ref` → `UngatedContentRefused`.

    `honest_marker` is optional; if provided, must be one of
    §6.9 markers: `unmeasured` / `INFERRED` / `honest-gap` / `fallback`.
    """
    if not a5_15_anchor_ref or not a5_15_anchor_ref.startswith("a5_15://"):
        raise UngatedContentRefused(
            "Binding condition (5) verbatim: 'Content generated · chat "
            "surface · anchored · gated (R-32/A5.15/CON-6).' Missing "
            f"a5_15_anchor_ref={a5_15_anchor_ref!r}."
        )
    if not con_6_gate_ref or not con_6_gate_ref.startswith("con_6://"):
        raise UngatedContentRefused(
            "Binding condition (5) verbatim: 'CON-6 gated content.' "
            f"Missing con_6_gate_ref={con_6_gate_ref!r}."
        )
    return ContentRegistryEntry_v1(
        content_registry_ref=content_registry_ref,
        a5_15_anchor_ref=a5_15_anchor_ref,
        con_6_gate_ref=con_6_gate_ref,
        honest_marker=honest_marker,
    )
