"""CP-AIP-4-CODEC-SERVICE · AIP v1.0 §3.2 P049 codec pretraining commissioned-job contract seat.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else.

Spec anchor (AIP v1.0):
- §3.2 P049 verbatim: 'The codec pretrains unsupervised on unlabelled
  estate audio, under the standard commissioned-job contract.'
- §1.4 measure-don't-assert: costs are measured before heavy pretraining
  runs; no asserted throughput / cost figures.
- §16.2 codec-choice DEFERRED per owner ('Sampling & Reflection §11.2
  answers it once built').

Owner directive verbatim (2026-02-23 CP-AIP-4 GO):
    'Build the service seam + contract + pins against whichever codec
    path is cheapest to stand up honestly (HF online fetch is permitted
    per lifted hold; offline cache remains fallback). If neither is
    viable in-pod, the fail-closed refusal path with stated reason IS
    the honest v1 behavior - do not mock a codec and call it real; mark
    any stub explicitly as honest-gap. Codec pretraining (§3.2) is a
    commissioned-job contract item - card it, do not run heavy
    pretraining in-pod without a measured cost receipt first.'

Design:
- `CodecPretrainingContract_v1` frozen dataclass carries the
  commissioned-job contract shape.
- `PretrainingCostReceiptMissing` raised on any attempt to launch
  pretraining without a measured cost receipt.
- `assert_pretraining_can_run_in_pod` is the boundary that refuses
  heavy pretraining without cost evidence (§1.4).
- `HONEST_GAP_V1_POSTURE` Final constant names the current v1
  fail-closed refusal posture (owner directive verbatim - honest-gap
  marker so downstream reviewers cannot mistake the seat for a real
  pretraining harness).

Sealed carriers UNCHANGED per SO §3.8:
- backend/services/perception/audio_codec/service.py (CP-M6-4-1 ·
  pretraining_contract carrier already sealed on AudioCodecServiceDescriptor).

Wave-honest limits:
- No LLM invocation. No HTTP call. No filesystem write.
- Case-agnostic; no executive-domain tokens.
"""
from __future__ import annotations

import dataclasses
from typing import Final, Literal, Optional


# Honest-gap marker (owner directive verbatim 2026-02-23 CP-AIP-4 GO):
#   'if neither is viable in-pod, the fail-closed refusal path with
#    stated reason IS the honest v1 behavior - do not mock a codec and
#    call it real; mark any stub explicitly as honest-gap.'
HONEST_GAP_V1_POSTURE: Final[str] = (
    "CP-AIP-4-v1-HONEST-GAP · codec pretraining not yet stood up "
    "in-pod. Fail-closed refusal (PretrainingCostReceiptMissing / "
    "UnsupportedCodecConditionRefused / MissingFidelityMeasurementError) "
    "IS the honest v1 behavior. No mock-and-call-it-real. §16.2 codec-"
    "choice DEFERRED to Sampling & Reflection §11.2."
)


class PretrainingCostReceiptMissing(Exception):
    """§1.4 measure-don't-assert refusal · pretraining requires a
    MEASURED cost receipt path before launching a heavy run in-pod.
    Owner directive verbatim: 'do not run heavy pretraining in-pod
    without a measured cost receipt first.'"""


@dataclasses.dataclass(frozen=True)
class CodecPretrainingContract_v1:
    """§3.2 P049 commissioned-job contract carrier.

    Three carriers:
      - `contract_type` — Literal["commissioned_job"] per §3.2 P049
        verbatim ('under the standard commissioned-job contract').
      - `data_scope` — description of the training-data scope
        (§3.2 P049 verbatim: 'unlabelled estate audio').
      - `cost_measurement_receipt_path` — Optional path (str) to the
        MEASURED cost receipt bank. Must be non-empty at launch time
        (see `assert_pretraining_can_run_in_pod`).
    """

    contract_type: Literal["commissioned_job"]
    data_scope: str
    cost_measurement_receipt_path: Optional[str] = None


def assert_pretraining_can_run_in_pod(
    *,
    contract: CodecPretrainingContract_v1,
) -> None:
    """§1.4 measure-don't-assert + owner directive verbatim: refuses
    to launch heavy pretraining in-pod without a measured cost
    receipt path on the contract.

    Refuses `PretrainingCostReceiptMissing` when the contract's
    `cost_measurement_receipt_path` is None or empty. Returns None
    on acceptance (contract satisfies the cost-receipt precondition).
    """
    if contract.contract_type != "commissioned_job":
        raise PretrainingCostReceiptMissing(
            f"§3.2 P049 verbatim: 'under the standard commissioned-job "
            f"contract'. Contract type {contract.contract_type!r} is not "
            f"admissible for in-pod pretraining."
        )
    if not contract.cost_measurement_receipt_path:
        raise PretrainingCostReceiptMissing(
            f"§1.4 measure-don't-assert + owner directive verbatim "
            f"(2026-02-23 CP-AIP-4 GO): 'do not run heavy pretraining "
            f"in-pod without a measured cost receipt first.' Contract "
            f"data_scope={contract.data_scope!r} has no "
            f"cost_measurement_receipt_path on file. Fail-closed per "
            f"§3.1 P037. Honest-gap posture: {HONEST_GAP_V1_POSTURE}"
        )
    return None
