"""CP-AIP-LANGUAGE-COGNITION · language_cognition_corpus_seam_v1 · additive
corpus-assembly seam composing sealed CP-AIP-ASSIST-CENSUS by identity.

Ledger check - this seal implements Item 5.12 of EXECUTION_ORDER.md
CP-AIP-LANGUAGE-COGNITION (SPEC ENHANCEMENT · owner order 2026-02-23T~16:07Z
verbatim · SO §6.8 standing authority) and nothing else. Additive-only per
SO §3.8. Sealed CP-AIP-ASSIST-CENSUS UNCHANGED. Terminal pytest only.
RED-first mechanical.

Owner directive verbatim (owner drop 2026-02-23 §Sequence · §coupling):
'Corpus assembly runs UNDER THE CENSUS ASSISTANT'S DIALOGUE — this is
Item 5.11.f (CP-AIP-ASSIST-CENSUS)'s first real objective. The assistant
PROPOSES corpus slices; the owner/tenant CONFIRMS; gates DECIDE.'

Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: E1 wires the seam INTO
Census Autonomy Service; pod is never data path.

§1.2 modality-extension composing sealed CP-AIP-ASSIST-CENSUS by identity
— never redeclare sealed symbols.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Tuple

# §1.2 modality-extension: compose sealed CP-AIP-ASSIST-CENSUS by identity.
from backend.services.census_autonomy.assist_census_v1 import (
    bank_confirmed_assistant_turn as _bank_confirmed_assistant_turn,
    render_content_registry_entry as _render_content_registry_entry,
)


# ---------------------------------------------------------------------------
# Sealed callables composed by identity (§1.2 no-redeclaration)
# ---------------------------------------------------------------------------


BANK_CONFIRMED_ASSISTANT_TURN_COMPOSED_BY_IDENTITY = _bank_confirmed_assistant_turn
RENDER_CONTENT_REGISTRY_ENTRY_COMPOSED_BY_IDENTITY = _render_content_registry_entry


# ---------------------------------------------------------------------------
# Target languages Final 5-tuple (owner verbatim)
# ---------------------------------------------------------------------------


LANGUAGE_COGNITION_TARGET_LANGUAGES: Final[Tuple[str, str, str, str, str]] = (
    "Kikuyu",
    "Luo",
    "Sheng",
    "Swahili",
    "English",
)


# ---------------------------------------------------------------------------
# Honest-gap carrier — DQ-17 family (Weego/NAS credential rotations)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CorpusChannelUnreachableHonestGap_v1:
    """Owner drop §Long-pole verbatim: 'Corpus assembly needs NAS channels
    reachable (Weego/NAS credential rotations DQ-17 family) as ONLY gate
    recorded as FACT not policy hold.' This carrier declares the honest-
    gap explicitly — the gate is a FACT about the pod's current channel
    reachability, not a policy hold introduced by the seal.
    """
    blocked_on_ref: str
    is_fact_not_policy_hold: bool
    remediation_ref: str


CORPUS_CHANNEL_UNREACHABLE_HONEST_GAP: Final[CorpusChannelUnreachableHonestGap_v1] = (
    CorpusChannelUnreachableHonestGap_v1(
        blocked_on_ref="DQ-17 · Weego/NAS credential rotations · STATE/DESK_QUEUE.md",
        is_fact_not_policy_hold=True,
        remediation_ref=(
            "Owner action: unlock Weego/NAS channels via credential rotation. "
            "Once channels are reachable, sealed assist_census_v1."
            "bank_confirmed_assistant_turn + render_content_registry_entry "
            "compose the corpus-slice propose/confirm/gate/decide workflow. "
            "Training compute + labelled corpus NEVER leave Akki's boundary."
        ),
    )
)


# ---------------------------------------------------------------------------
# Posture markers (Final str · owner verbatim)
# ---------------------------------------------------------------------------


CORPUS_ASSEMBLY_UNDER_ASSISTANT_DIALOGUE_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-DO §10 owner verbatim (owner drop "
    "§Sequence · §coupling): 'Corpus assembly runs UNDER THE CENSUS "
    "ASSISTANT'S DIALOGUE. The assistant PROPOSES corpus slices; the "
    "owner/tenant CONFIRMS; gates DECIDE.' Composes sealed CP-AIP-ASSIST-"
    "CENSUS bank_confirmed_assistant_turn + render_content_registry_entry "
    "by identity via BANK_CONFIRMED_ASSISTANT_TURN_COMPOSED_BY_IDENTITY "
    "+ RENDER_CONTENT_REGISTRY_ENTRY_COMPOSED_BY_IDENTITY. §1.2 "
    "no-redeclaration."
)


DQ_17_ONLY_GATE_FACT_NOT_POLICY_HOLD_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION Long-pole owner verbatim: 'Corpus assembly "
    "needs NAS channels reachable (Weego/NAS credential rotations DQ-17 "
    "family) as ONLY gate recorded as FACT not policy hold.' The gate is "
    "structural reachability of the tenant's Weego/NAS channels — not a "
    "policy check the seal introduces."
)


COMMISSIONED_JOB_HONEST_GAP_NOT_MOCK_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-NOT §9 owner verbatim (owner drop "
    "§Execution-reach): 'If in-pod compute cannot honestly run even a "
    "small LoRA pass, the commissioned-job contract carries an honest-gap "
    "on execution — never a mock or a stub.' The commissioned Track-4 "
    "training-runs job kind carries the honest-gap as a receipt line, "
    "never a fabricated pass."
)
