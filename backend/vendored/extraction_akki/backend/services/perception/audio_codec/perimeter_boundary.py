"""M6 · Audio-Plane v1.0 · CP-M6-4-4 · in-perimeter-on-tenant-compute invariant.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §3.2 P045 (V33 · service path · N4 anchor · in-perimeter clause):
      "perception/audio_codec/ — registered like any other perception model; census-visible; runs in-perimeter on tenant compute."

- M6 grounding brief §Sub-wave 4 CP breakdown (verbatim):
      "CP-M6-4-4 · in-perimeter-on-tenant-compute invariant — TESTS-FIRST · codec service refuses cross-perimeter dispatch."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Pure carrier + predicate + refusal.  No coupling to a specific
    dispatcher implementation (case-agnostic).
  - §3.1 P038 tokens-not-waveforms discipline preserved.

Contract:

    IN_PERIMETER: str = "in-perimeter"
    OUT_OF_PERIMETER: str = "out-of-perimeter"
    TENANT_COMPUTE: str = "tenant"

    PerimeterProfile — frozen 2-carrier dataclass:
      perimeter · compute_kind.

    is_in_perimeter_on_tenant_compute(*, perimeter_profile) -> bool
      Pure predicate.  True iff perimeter == IN_PERIMETER AND
      compute_kind == TENANT_COMPUTE (conjunctive per §3.2 P045
      verbatim).

    assert_runs_in_perimeter_on_tenant_compute(*, perimeter_profile) -> None
      Refuses with PerimeterViolationError on any violation, naming
      the specific violated clause (perimeter or compute).

    PerimeterViolationError — subclass of PerceptionRegistrationError
    (from CP-M6-4-1 service.py · family cohesion).

Refusals:
    PerimeterViolationError
"""

from __future__ import annotations

from dataclasses import dataclass

from services.perception.audio_codec.service import (
    PerceptionRegistrationError,
)


IN_PERIMETER: str = "in-perimeter"
OUT_OF_PERIMETER: str = "out-of-perimeter"
TENANT_COMPUTE: str = "tenant"


class PerimeterViolationError(PerceptionRegistrationError):
    """Raised when a `PerimeterProfile` does not satisfy the §3.2 P045
    verbatim 'runs in-perimeter on tenant compute' conjunctive clause.

    Subclass of `PerceptionRegistrationError` (CP-M6-4-1) so the
    perception-registration refusal family remains single-catch."""


@dataclass(frozen=True)
class PerimeterProfile:
    """The declared execution profile for the audio_codec service.

    Two carriers:
      - `perimeter` — must be `IN_PERIMETER` for the §3.2 P045
        verbatim 'runs in-perimeter' clause.
      - `compute_kind` — must be `TENANT_COMPUTE` for the §3.2 P045
        verbatim 'on tenant compute' clause.

    Pull-seam / §3.1 P038 discipline: no `audio_bytes` / `waveform` /
    `samples` / `raw_audio` carriers.
    """

    perimeter: str
    compute_kind: str


def is_in_perimeter_on_tenant_compute(
    *,
    perimeter_profile: PerimeterProfile,
) -> bool:
    """Return True iff the profile declares both `IN_PERIMETER` and
    `TENANT_COMPUTE`.  Pure predicate.  Case-agnostic."""
    return (
        perimeter_profile.perimeter == IN_PERIMETER
        and perimeter_profile.compute_kind == TENANT_COMPUTE
    )


def assert_runs_in_perimeter_on_tenant_compute(
    *,
    perimeter_profile: PerimeterProfile,
) -> None:
    """Assert the §3.2 P045 verbatim 'runs in-perimeter on tenant
    compute' invariant.  Refuses with `PerimeterViolationError` on any
    violation, naming the specific violated clause.

    Conjunctive per canon: an in-perimeter dispatch on non-tenant
    compute is refused; an out-of-perimeter dispatch on tenant compute
    is refused; only the (`IN_PERIMETER`, `TENANT_COMPUTE`) profile
    passes.
    """
    if perimeter_profile.perimeter != IN_PERIMETER:
        raise PerimeterViolationError(
            f"audio_codec: perimeter {perimeter_profile.perimeter!r} "
            f"is not {IN_PERIMETER!r} (§3.2 P045 verbatim: "
            f"'runs in-perimeter on tenant compute')"
        )
    if perimeter_profile.compute_kind != TENANT_COMPUTE:
        raise PerimeterViolationError(
            f"audio_codec: compute_kind {perimeter_profile.compute_kind!r} "
            f"is not {TENANT_COMPUTE!r} (§3.2 P045 verbatim: "
            f"'runs in-perimeter on tenant compute')"
        )
    return None
