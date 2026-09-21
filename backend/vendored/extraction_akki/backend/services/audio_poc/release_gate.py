"""W-AUDIO-POC · CP-A1 · Release gate for transcript artefacts.

Refuses any transcript release unless FOUR verdicts are all non-`PENDING`:
`kdpa_verdict`, `named_persons_verdict`, `transfer_basis`, `licence_class`.
Refuses tiers `biometric_embedding`, `named_identity`,
`speaker_labeled_audio` by default (regardless of verdicts).

The SAFE tier is `transcript_text_only` — text-only transcript payloads.
With `licence_class:owner_full_rights` (per owner Ruling #2, DECISIONS
2026-09-12T~12:00Z) AND all three other verdicts non-PENDING, this tier
admits.

Wave-scope note: at wave open, the three other verdicts (KDPA · named-
persons · transfer-basis) are all PENDING per owner still-blocked list.
This means the release gate CURRENTLY refuses ALL transcript releases.
CP-A5's writer will observe the refusal and HALT-with-blocker-note per
grounding brief §G — that is the CORRECT posture until owner rulings
land on R-7 / R-15 / R-16 / R-17.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contracts.release_budget import ReleaseBudgetState, ReleaseLedgerDebit


TRANSCRIPT_TIERS_REFUSED_BY_DEFAULT: frozenset = frozenset({
    "biometric_embedding",
    "named_identity",
    "speaker_labeled_audio",
})

SAFE_TRANSCRIPT_TIER: str = "transcript_text_only"

# Verdict state that fails the gate regardless of tier.
_PENDING_STATE: str = "PENDING"


# W-RELEASE-GATE-PILOT-LIFT · CP-RG3 · closed-set discipline on verdicts.
# Acceptable values for named_persons_verdict.
# - PENDING · pre-ratification default (refuses via TranscriptVerdictPending).
# - DPO-APPROVED · owner-authorized non-tokenized admission (existing pattern).
# - TOKENIZED · R-15(a) admission (DECISIONS 2026-09-15T~03:55Z Effect 2:
#   "named_persons_verdict resolves to TOKENIZED for release purposes").
TRANSCRIPT_NAMED_PERSONS_VERDICTS_ACCEPTABLE: frozenset = frozenset({
    "PENDING",
    "RATIFIED",
    "DPO-APPROVED",
    "TOKENIZED",
})

# Acceptable values for transfer_basis.
# - PENDING · pre-ratification default (refuses via TranscriptVerdictPending).
# - DPO-APPROVED · owner-authorized non-derivative admission (existing pattern).
# - DERIVATIVE_ONLY_VIA_PULL_SEAM · R-16(a) admission (DECISIONS
#   2026-09-15T~03:55Z Effect 3: "Set transfer_basis:
#   DERIVATIVE_ONLY_VIA_PULL_SEAM for the transcript-text-only tier — the
#   Pull Seam is the model-facing seam; source data does not cross; only
#   derivatives (tokenized transcripts) cross").
TRANSCRIPT_TRANSFER_BASIS_ACCEPTABLE: frozenset = frozenset({
    "PENDING",
    "RATIFIED",
    "DPO-APPROVED",
    "DERIVATIVE_ONLY_VIA_PULL_SEAM",
})


class TranscriptTierRefused(Exception):
    """Raised when the artefact's tier is in
    `TRANSCRIPT_TIERS_REFUSED_BY_DEFAULT`.
    """


class TranscriptVerdictPending(Exception):
    """Raised when any of the four verdicts is `PENDING`."""


class TranscriptVerdictUnknown(Exception):
    """W-RELEASE-GATE-PILOT-LIFT · CP-RG3 · Raised when a verdict value is
    outside its closed-set of acceptable values.

    Applies to:
      - `named_persons_verdict` outside `TRANSCRIPT_NAMED_PERSONS_VERDICTS_ACCEPTABLE`
      - `transfer_basis` outside `TRANSCRIPT_TRANSFER_BASIS_ACCEPTABLE`

    Closed-set discipline: extending an acceptable set is an owner-ratified
    snapshot-parity event (see R-15(a)/R-16(a) DECISIONS 2026-09-15T~03:55Z
    Effects 2+3 for the current admission set).
    """


@dataclass(frozen=True)
class TranscriptArtefact:
    """Release-gate carrier for a transcript artefact.

    Frozen: mutation after construction raises `FrozenInstanceError`.
    Field order is fixed; adding fields is a snapshot-parity event.
    """

    tier: str
    kdpa_verdict: str
    named_persons_verdict: str
    transfer_basis: str
    licence_class: str


def admit_transcript_release(artefact: TranscriptArtefact) -> None:
    """Refuse the release unless every gate passes.

    Order of checks:
      1. Tier check (`TranscriptTierRefused`).
      2. Four-verdict PENDING check (`TranscriptVerdictPending`).

    Returns None on admit.  The caller then knows the artefact is
    clear to leave the estate (PutObject to OBS, etc.).
    """
    if artefact.tier in TRANSCRIPT_TIERS_REFUSED_BY_DEFAULT:
        raise TranscriptTierRefused(
            f"transcript tier refused by default: {artefact.tier!r}"
        )
    pending_fields = [
        f
        for f in (
            "kdpa_verdict",
            "named_persons_verdict",
            "transfer_basis",
            "licence_class",
        )
        if getattr(artefact, f) == _PENDING_STATE
    ]
    if pending_fields:
        raise TranscriptVerdictPending(
            f"transcript release refused: verdict(s) PENDING: {pending_fields}"
        )

    # W-RELEASE-GATE-PILOT-LIFT · CP-RG3 · Closed-set discipline on verdicts.
    # R-15(a) admits TOKENIZED; R-16(a) admits DERIVATIVE_ONLY_VIA_PULL_SEAM;
    # every other value outside the acceptable set MUST refuse (this closes
    # the previously-open string-typed carriers to a canonical value set).
    if artefact.named_persons_verdict not in TRANSCRIPT_NAMED_PERSONS_VERDICTS_ACCEPTABLE:
        raise TranscriptVerdictUnknown(
            f"named_persons_verdict outside closed acceptable set: "
            f"{artefact.named_persons_verdict!r}"
        )
    if artefact.transfer_basis not in TRANSCRIPT_TRANSFER_BASIS_ACCEPTABLE:
        raise TranscriptVerdictUnknown(
            f"transfer_basis outside closed acceptable set: "
            f"{artefact.transfer_basis!r}"
        )
    return None


def admit_transcript_release_pilot_open(
    artefact: TranscriptArtefact,
    *,
    release_receipt_id: str,
    release_budget_state: "ReleaseBudgetState",
    usage_quantity: int,
    usage_unit: str,
    debited_by_party: str,
) -> "ReleaseLedgerDebit":
    """W-RELEASE-GATE-PILOT-LIFT · CP-RG4 · End-to-end admit + debit compose.

    Composes CP-RG3 `admit_transcript_release` (artefact validation) with
    CP-RG1 `record_debit` (P036 receipt-before-result + R-7 PILOT_OPEN
    receipt+debit invariant).

    Order:
      1. Validate the artefact via `admit_transcript_release` — raises
         `TranscriptTierRefused` / `TranscriptVerdictPending` /
         `TranscriptVerdictUnknown` on failure. On failure, NO debit is
         written (P036 receipt-before-result ordering: the receipt refers
         to a completed operation; a refused operation has no debit).
      2. Record the debit via `record_debit` — raises
         `ReceiptMissingRefused` on empty `release_receipt_id` (P036 anchor)
         or `BudgetStateRefused` on `DEFAULT_PENDING_OVERRIDE` (R-7 anchor).

    Returns the recorded `ReleaseLedgerDebit`.

    Canon anchors:
      - R-7 · DECISIONS 2026-09-15T~03:55Z · Effect 1: PILOT_OPEN admission
        with mandatory receipt+debit.
      - R-15(a) · Effect 2: named_persons_verdict = TOKENIZED admits.
      - R-16(a) · Effect 3: transfer_basis = DERIVATIVE_ONLY_VIA_PULL_SEAM admits.
      - R-17(a) hardening deferred (owner: "stays open · non-blocking").
      - Pull Seam §2 P7 P036: receipt-before-result invariant.
    """
    # Lazy import to avoid circular reference at module load.
    from services.release_gate.release_ledger import record_debit
    # Step 1: artefact validation (may raise; no debit-write on refusal).
    admit_transcript_release(artefact)
    # Step 2: record debit (P036 receipt-before-result · R-7 budget-state gate).
    return record_debit(
        receipt_id=release_receipt_id,
        budget_state=release_budget_state,
        usage_quantity=usage_quantity,
        usage_unit=usage_unit,
        debited_by_party=debited_by_party,
    )
