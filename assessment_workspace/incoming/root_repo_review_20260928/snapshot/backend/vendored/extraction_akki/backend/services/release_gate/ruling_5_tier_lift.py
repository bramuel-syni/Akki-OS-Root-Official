"""CP-M7-W8-LIFT-1 · Ruling #5 tier-lift admissibility carrier.

Owner ruling banked verbatim 2026-09-16T~17:43Z (§A · master a04c65a8):

    "Ruling #5: kdpa = compliant-under-pilot, named-persons = tokenized,
     transfer-basis = derivative-only"

Under Ruling #5, the three tiers previously refused-by-default at
`services.audio_poc.release_gate.TRANSCRIPT_TIERS_REFUSED_BY_DEFAULT`
(`biometric_embedding`, `named_identity`, `speaker_labeled_audio`) are
LIFTED to ADMISSIBLE when a caller invokes
`assert_admissible_under_ruling_5(...)` with the exact triple of
verdict values banked by the ruling.

Case-agnostic doctrine:
- All identifier discriminators (tier · verdict value strings) are
  OPEN str. Values are frozen at owner-ratified constants; the
  refusal-wrapper compares equality against those constants.
- Zero closed enums.
- Zero imports of `services.audio_poc.release_gate` (case-agnostic
  decoupling · composition surface only · caller-side composition
  binds this admissibility check with the existing release-gate
  refusal-by-default surface).

Preventive-charter pattern (matches CP-M8-CTCC-1 + CP-M7-W9-CONTRACT-1
+ CP-M7-W2-CONTRACT-1):
- Runtime enforcement fires only when caller invokes
  `assert_admissible_under_ruling_5`. No global gate.
- The lift admits under Ruling #5 conditions; downstream composition
  with `admit_transcript_release_pilot_open` is caller-side.

Standing lines held:
- No estate-audio training (SW-10 deferred; this module is
  admissibility only, not training).
- No biometric material (this module compares string verdict values;
  synthetic-fixture invariants exercise the refusal semantics; no
  actual biometric material touches the mechanism).
- No enforcement hard-gate (preventive-charter · caller invokes).
- No speculative shapes (4-carrier check + 4 refusal classes bind
  1:1 to Ruling #5 verbatim triple + non-lifted-tier refusal).
"""
from __future__ import annotations

import dataclasses


# Owner ruling #5 verbatim (banked 2026-09-16T~17:43Z · §A master a04c65a8):
# Ratified verdict-value normalizations (owner-verbatim lower-case with
# hyphens is the case-agnostic canonical form):
KDPA_VERDICT_COMPLIANT_UNDER_PILOT: str = "compliant-under-pilot"
NAMED_PERSONS_VERDICT_TOKENIZED: str = "tokenized"
TRANSFER_BASIS_DERIVATIVE_ONLY: str = "derivative-only"


# Ruling #5 verbatim anchor · required-verbatim phrase for gating invariant.
RULING_5_VERBATIM_ANCHOR: str = (
    "Owner ruling #5 verbatim (2026-09-16T~17:43Z): "
    "'Ruling #5: kdpa = compliant-under-pilot, "
    "named-persons = tokenized, transfer-basis = derivative-only'"
)


# Three tiers lifted by Ruling #5 (previously refused-by-default at
# `services.audio_poc.release_gate.TRANSCRIPT_TIERS_REFUSED_BY_DEFAULT`):
TIERS_LIFTED_UNDER_RULING_5: tuple = (
    "biometric_embedding",
    "named_identity",
    "speaker_labeled_audio",
)


class Ruling5TierLiftRefused(Exception):
    """Root refusal class for Ruling #5 tier-lift admissibility check."""


class TierNotLiftedUnderRuling5Error(Ruling5TierLiftRefused):
    """Refusal raised when the tier is not in the three tiers lifted by
    Ruling #5. Callers using this admissibility check on the
    always-safe `transcript_text_only` tier or any other tier should
    route through the existing `admit_transcript_release` path."""


class KdpaVerdictNotCompliantUnderPilotError(Ruling5TierLiftRefused):
    """Refusal raised when kdpa_verdict is not exactly
    'compliant-under-pilot' per Ruling #5 verbatim."""


class NamedPersonsVerdictNotTokenizedError(Ruling5TierLiftRefused):
    """Refusal raised when named_persons_verdict is not exactly
    'tokenized' per Ruling #5 verbatim (consistent with R-15(a))."""


class TransferBasisNotDerivativeOnlyError(Ruling5TierLiftRefused):
    """Refusal raised when transfer_basis is not exactly
    'derivative-only' per Ruling #5 verbatim (consistent with
    R-16(a))."""


@dataclasses.dataclass(frozen=True)
class Ruling5AdmissionCheck:
    """Ruling #5 admissibility check carrier.

    Exact-order 4 carriers. Frozen.

    - `tier` (str) — the tier to check; must be in
      `TIERS_LIFTED_UNDER_RULING_5` for admission.
    - `kdpa_verdict` (str) — must equal `KDPA_VERDICT_COMPLIANT_UNDER_PILOT`.
    - `named_persons_verdict` (str) — must equal
      `NAMED_PERSONS_VERDICT_TOKENIZED`.
    - `transfer_basis` (str) — must equal `TRANSFER_BASIS_DERIVATIVE_ONLY`.
    """
    tier: str
    kdpa_verdict: str
    named_persons_verdict: str
    transfer_basis: str


def assert_admissible_under_ruling_5(*, check: Ruling5AdmissionCheck) -> None:
    """Preventive-charter refusal wrapper.

    Fires only when caller invokes. Refuses (in order):
    - `TierNotLiftedUnderRuling5Error` if `check.tier` not in
      `TIERS_LIFTED_UNDER_RULING_5`.
    - `KdpaVerdictNotCompliantUnderPilotError` if
      `check.kdpa_verdict != KDPA_VERDICT_COMPLIANT_UNDER_PILOT`.
    - `NamedPersonsVerdictNotTokenizedError` if
      `check.named_persons_verdict != NAMED_PERSONS_VERDICT_TOKENIZED`.
    - `TransferBasisNotDerivativeOnlyError` if
      `check.transfer_basis != TRANSFER_BASIS_DERIVATIVE_ONLY`.

    Returns None on success. Does not mutate check.

    Caller-side composition: after this refusal-wrapper returns None,
    the caller MAY proceed with downstream release-gate composition
    (e.g. `admit_transcript_release_pilot_open` with the appropriate
    tokenized-named-persons and derivative-only-via-pull-seam
    normalizations of the verdict values into the existing closed sets
    at `services.audio_poc.release_gate`).
    """
    if check.tier not in TIERS_LIFTED_UNDER_RULING_5:
        raise TierNotLiftedUnderRuling5Error(
            f"tier {check.tier!r} is not lifted by Ruling #5; "
            f"lifted tiers are {TIERS_LIFTED_UNDER_RULING_5!r}."
        )
    if check.kdpa_verdict != KDPA_VERDICT_COMPLIANT_UNDER_PILOT:
        raise KdpaVerdictNotCompliantUnderPilotError(
            f"kdpa_verdict {check.kdpa_verdict!r} does not match "
            f"Ruling #5 verbatim value "
            f"{KDPA_VERDICT_COMPLIANT_UNDER_PILOT!r}."
        )
    if check.named_persons_verdict != NAMED_PERSONS_VERDICT_TOKENIZED:
        raise NamedPersonsVerdictNotTokenizedError(
            f"named_persons_verdict {check.named_persons_verdict!r} "
            f"does not match Ruling #5 verbatim value "
            f"{NAMED_PERSONS_VERDICT_TOKENIZED!r}."
        )
    if check.transfer_basis != TRANSFER_BASIS_DERIVATIVE_ONLY:
        raise TransferBasisNotDerivativeOnlyError(
            f"transfer_basis {check.transfer_basis!r} does not match "
            f"Ruling #5 verbatim value "
            f"{TRANSFER_BASIS_DERIVATIVE_ONLY!r}."
        )


__all__ = [
    "KDPA_VERDICT_COMPLIANT_UNDER_PILOT",
    "NAMED_PERSONS_VERDICT_TOKENIZED",
    "TRANSFER_BASIS_DERIVATIVE_ONLY",
    "RULING_5_VERBATIM_ANCHOR",
    "TIERS_LIFTED_UNDER_RULING_5",
    "Ruling5AdmissionCheck",
    "Ruling5TierLiftRefused",
    "TierNotLiftedUnderRuling5Error",
    "KdpaVerdictNotCompliantUnderPilotError",
    "NamedPersonsVerdictNotTokenizedError",
    "TransferBasisNotDerivativeOnlyError",
    "assert_admissible_under_ruling_5",
]
