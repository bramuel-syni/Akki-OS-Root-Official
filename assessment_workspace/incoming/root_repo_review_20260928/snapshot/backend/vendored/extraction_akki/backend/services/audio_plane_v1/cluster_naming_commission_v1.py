"""CP-AIP-5-CLUSTERING · cluster naming commission wrapper · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-5-CLUSTERING and nothing else.

Spec anchor: AIP v1.0 §5.3 clause 2 verbatim: "Naming and validation are
human work applied to a sample, commissioned like any other qualified
work with quoted cost."

§1.2 modality-extension: this module COMPOSES sealed carriers:
  - CP-M6-5-2 HumanValidationVerdict + ValidatedStratum + bind_verdict_to_stratum
    (human_validation.py).
  - CP-M6-5-1 CandidateStratum (clustering.py).

Sealed carriers are IMPORTED, NEVER REDECLARED. The bind path uses
sealed bind_verdict_to_stratum verbatim; this module DOES NOT
reimplement the bind parallel-fashion.

§1.4 measure-don't-assert: quoted-cost commissioning discipline
requires a non-empty commissioning_receipt_ref (fail-fast on empty per
§1.5 unrepresentable-not-policed).
"""
from __future__ import annotations

from typing import Final

from backend.services.audio_plane_v1.clustering import (
    CandidateStratum,
)
from backend.services.audio_plane_v1.human_validation import (
    HumanValidationVerdict,
    ValidatedStratum,
    bind_verdict_to_stratum,
    derive_task_id,
)


HONEST_GAP_V1_POSTURE: Final[str] = (
    "AIP v1.0 §5.3 clause 2 verbatim: naming and validation are human "
    "work applied to a sample, commissioned like any other qualified "
    "work with quoted cost. This module wraps sealed CP-M6-5-2 "
    "bind_verdict_to_stratum verbatim; it does not infer a name."
)


class NamingCommissionReceiptMissing(Exception):
    """Raised by commission_cluster_naming when the commissioning
    receipt reference is empty / None / whitespace-only. §5.3 clause 2
    verbatim requires the commissioning receipt to be present;
    §1.4 measure-don't-assert forbids proceeding without it.
    """


def commission_cluster_naming(
    *,
    stratum: CandidateStratum,
    proposed_name: str,
    commissioning_receipt_ref: str,
    verdict_type: str = "accept",
) -> ValidatedStratum:
    """Commission a human naming ceremony over a candidate stratum via
    sealed CP-M6-5-2 bind_verdict_to_stratum.

    Refusals:
      - `NamingCommissionReceiptMissing` when `commissioning_receipt_ref`
        is empty / whitespace-only / falsy (§5.3 clause 2 verbatim +
        §1.4 measure-don't-assert).
      - `VerdictClosedSetViolationError` from sealed CP-M6-5-2 when
        `verdict_type` is outside the closed verdict set.
      - `VerdictTaskIdMismatchError` from sealed CP-M6-5-2 when the
        derived task_id does not match (structural boundary).

    Returns a frozen `ValidatedStratum` from sealed CP-M6-5-2
    bind_verdict_to_stratum (§1.2 modality-extension - not
    reimplemented).
    """
    if not commissioning_receipt_ref or not commissioning_receipt_ref.strip():
        raise NamingCommissionReceiptMissing(
            f"CP-AIP-5: commissioning_receipt_ref="
            f"{commissioning_receipt_ref!r} is empty/whitespace-only; "
            f"§5.3 clause 2 verbatim requires quoted-cost commissioning "
            f"receipt for cluster naming ceremony. Refusing to commission "
            f"naming for stratum {stratum.stratum_id!r}."
        )

    task_id = derive_task_id(stratum=stratum)
    verdict = HumanValidationVerdict(
        task_id=task_id,
        verdict=verdict_type,
        named_by_human=proposed_name,
        commissioning_receipt_ref=commissioning_receipt_ref,
    )

    # §1.2 modality-extension: invoke sealed CP-M6-5-2 verbatim.
    return bind_verdict_to_stratum(stratum=stratum, verdict=verdict)
