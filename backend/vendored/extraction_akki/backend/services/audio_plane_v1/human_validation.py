"""M6 · Audio-Plane v1.0 · CP-M6-5-2 · Sampled human validation loop mechanism.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §5.3 P089 (V59 · human validation clause):
      "Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."

- Audio-Plane §16.2 P249 (V157 · commissioning channel):
      "Cluster naming validation: commissioned internally or delegated to an external evaluation partner where one exists (§5.3)."

- M6 Sub-wave 5 grounding brief §C · CP-M6-5-2 (verbatim):
      "Sampled human validation loop mechanism. Build the MECHANISM (deterministic sampling · frozen validation record · verdict binding) provable with synthetic fixtures. Actual human validators binding real samples is post-unblock owner activity — owner ruling 2026-09-15T~20:37Z."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Mechanism provable with synthetic fixtures.
  - §5.3 clause 2 preserved in-flight: `named_by_human` stays None
    until owner unblocks real human validators binding real samples.

Contract:

    COMMISSIONING_CHANNELS = frozenset({"internal", "external_partner"})
      # §16.2 P249 verbatim two-set.

    VALIDATION_VERDICTS = frozenset({
        "variant_confirmed", "variant_refused", "ambiguous",
    })

    sample_stratum_for_human_validation(
        *, stratum, sample_size, rng_seed,
    ) -> Tuple[str, ...]
      Deterministic sampler.  Same (stratum, sample_size, rng_seed) →
      byte-identical output.

    HumanValidationTask — frozen 5-carrier dataclass:
      task_id · stratum_id · sample_attribute_names ·
      quoted_cost_reference · commissioning_channel.  Refuses invalid
      channel at __post_init__.

    HumanValidationVerdict — frozen 4-carrier dataclass:
      task_id · verdict · named_by_human · commissioning_receipt_ref.
      Refuses invalid verdict at __post_init__.  named_by_human stays
      None until owner-unblocked real human binding.

    ValidatedStratum — frozen 3-carrier dataclass:
      candidate_stratum · verdict · bound_at_utc.

    derive_task_id(*, stratum) -> str
      Deterministic task-id derivation from stratum.stratum_id.

    bind_verdict_to_stratum(*, stratum, verdict) -> ValidatedStratum
      Refuses `VerdictTaskIdMismatchError` on task_id mismatch;
      otherwise composes a `ValidatedStratum`.

Refusals:
    SampleSizeInvalidError · SampleSizeExceedsStratumError ·
    RngSeedInvalidError · CommissioningChannelInvalidError ·
    VerdictClosedSetViolationError · VerdictTaskIdMismatchError.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import FrozenSet, Optional, Tuple

from services.audio_plane_v1.clustering import CandidateStratum


COMMISSIONING_CHANNELS: FrozenSet[str] = frozenset({
    "internal", "external_partner",
})
"""§16.2 P249 verbatim: 'commissioned internally or delegated to an
external evaluation partner where one exists'."""

VALIDATION_VERDICTS: FrozenSet[str] = frozenset({
    "variant_confirmed", "variant_refused", "ambiguous",
})
"""Closed refusal grammar for the human validation loop."""


class SampleSizeInvalidError(Exception):
    """Raised when `sample_size` is not a positive integer."""


class SampleSizeExceedsStratumError(Exception):
    """Raised when `sample_size` exceeds the stratum's member count."""


class RngSeedInvalidError(Exception):
    """Raised when `rng_seed` is not an integer (deterministic sampling
    requires an integer seed)."""


class CommissioningChannelInvalidError(Exception):
    """Raised when a `HumanValidationTask.commissioning_channel` is
    outside `COMMISSIONING_CHANNELS`.  §16.2 P249 verbatim vocabulary
    discipline."""


class VerdictClosedSetViolationError(Exception):
    """Raised when a `HumanValidationVerdict.verdict` is outside
    `VALIDATION_VERDICTS`."""


class VerdictTaskIdMismatchError(Exception):
    """Raised by `bind_verdict_to_stratum` when the verdict's task_id
    does not match the task_id derived from the stratum."""


def derive_task_id(*, stratum: CandidateStratum) -> str:
    """Deterministically derive a task_id from a candidate stratum.

    Depends solely on `stratum.stratum_id` so the same stratum always
    yields the same task_id — the pivot the bind gate uses to detect
    cross-binding attempts.
    """
    return f"validation-task-{stratum.stratum_id}"


def sample_stratum_for_human_validation(
    *,
    stratum: CandidateStratum,
    sample_size: int,
    rng_seed: int,
) -> Tuple[str, ...]:
    """Deterministic sample of a stratum's members for human validation.

    Same `(stratum, sample_size, rng_seed)` → byte-identical output.

    Refusals:
      - `SampleSizeInvalidError` on `sample_size ≤ 0`.
      - `SampleSizeExceedsStratumError` on `sample_size > len(members)`.
      - `RngSeedInvalidError` on non-integer seed.
    """
    if not isinstance(rng_seed, int) or isinstance(rng_seed, bool):
        raise RngSeedInvalidError(
            f"rng_seed must be int, got {type(rng_seed).__name__}"
        )
    if sample_size <= 0:
        raise SampleSizeInvalidError(
            f"sample_size must be positive, got {sample_size}"
        )
    members = list(stratum.member_attribute_names)
    if sample_size > len(members):
        raise SampleSizeExceedsStratumError(
            f"sample_size {sample_size} exceeds stratum member count "
            f"{len(members)}"
        )
    rng = random.Random(rng_seed)
    return tuple(rng.sample(members, sample_size))


@dataclass(frozen=True)
class HumanValidationTask:
    """A commissioned human-validation task per §5.3 clause 3 verbatim.

    Five carriers:
      - `task_id` — opaque; deterministically derivable from
        `stratum_id` via `derive_task_id`.
      - `stratum_id` — the candidate stratum this task validates.
      - `sample_attribute_names` — the sampled members for human
        inspection (immutable tuple).
      - `quoted_cost_reference` — §5.3 clause 3 verbatim
        "commissioned like any other qualified work with quoted cost";
        this points to the quote entry.
      - `commissioning_channel` — closed-set per §16.2 P249 verbatim:
        one of `COMMISSIONING_CHANNELS`.
    """

    task_id: str
    stratum_id: str
    sample_attribute_names: Tuple[str, ...]
    quoted_cost_reference: str
    commissioning_channel: str

    def __post_init__(self) -> None:
        if self.commissioning_channel not in COMMISSIONING_CHANNELS:
            raise CommissioningChannelInvalidError(
                f"commissioning_channel {self.commissioning_channel!r} "
                f"outside §16.2 P249 verbatim vocabulary "
                f"{sorted(COMMISSIONING_CHANNELS)!r}"
            )


@dataclass(frozen=True)
class HumanValidationVerdict:
    """A human validation verdict on a commissioned task.

    Four carriers:
      - `task_id` — matches the `HumanValidationTask.task_id` the
        verdict responds to.
      - `verdict` — closed-set per `VALIDATION_VERDICTS`.
      - `named_by_human` — Optional[str].  §5.3 clause 2 verbatim
        preserved in-flight: 'not what it is called' — None is the
        canonical value until a real human validator supplies a name
        (post-unblock owner activity per owner ruling 2026-09-15T
        ~20:37Z).
      - `commissioning_receipt_ref` — pointer to the commissioning
        receipt closing the quoted-cost cycle.
    """

    task_id: str
    verdict: str
    named_by_human: Optional[str]
    commissioning_receipt_ref: str

    def __post_init__(self) -> None:
        if self.verdict not in VALIDATION_VERDICTS:
            raise VerdictClosedSetViolationError(
                f"verdict {self.verdict!r} outside verbatim closed-set "
                f"{sorted(VALIDATION_VERDICTS)!r}"
            )


@dataclass(frozen=True)
class ValidatedStratum:
    """A candidate stratum with an attached human validation verdict.

    Three carriers:
      - `candidate_stratum` — the original CP-M6-5-1
        `CandidateStratum` (frozen · immutability preserved).
      - `verdict` — the attached `HumanValidationVerdict`.
      - `bound_at_utc` — ISO-8601 UTC timestamp of the bind operation.
    """

    candidate_stratum: CandidateStratum
    verdict: HumanValidationVerdict
    bound_at_utc: str


def bind_verdict_to_stratum(
    *,
    stratum: CandidateStratum,
    verdict: HumanValidationVerdict,
) -> ValidatedStratum:
    """Bind a `HumanValidationVerdict` to its `CandidateStratum`.

    Refuses `VerdictTaskIdMismatchError` when the verdict's task_id
    does not match the deterministically-derived task_id for the
    stratum.

    Preserves the original `CandidateStratum` (frozen · immutable)
    reference via `ValidatedStratum.candidate_stratum`.
    """
    expected_task_id = derive_task_id(stratum=stratum)
    if verdict.task_id != expected_task_id:
        raise VerdictTaskIdMismatchError(
            f"verdict.task_id {verdict.task_id!r} does not match "
            f"expected {expected_task_id!r} for stratum "
            f"{stratum.stratum_id!r}"
        )
    return ValidatedStratum(
        candidate_stratum=stratum,
        verdict=verdict,
        bound_at_utc=datetime.now(timezone.utc).isoformat(),
    )
