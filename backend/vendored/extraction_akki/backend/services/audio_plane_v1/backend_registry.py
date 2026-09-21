"""M6 · Audio-Plane v1.0 · CP-M6-6-4 · Ratified-vs-INFERRED backend registry surface.

Discharge anchor (verbatim on single un-wrapped line):

- Rec-3-M6SW6 (owner ruling 2026-09-15T~21:25Z verbatim):
      "add a fourth CP to sub-wave 6 that lands a read-only registry surface enumerating every pluggable seam (LID, code-switch, channel-condition, synthesis-attributes, clustering, and any codec/backends registered) with status ∈ {RATIFIED, INFERRED-pending-ratification}, closed-set refusal on unknown status, deterministic output — the M6-seal-story 'what is truly live' table."

- D10 pluggable-seam discipline:
      Each pluggable seam registers backends with a ratification_state that is either 'ratified' (owner-ratified for live invocation) or 'inferred_pending_ratification' (placeholder registered by canon but not yet owner-ratified for live invocation). Live-invocation paths refuse on any 'inferred_pending_ratification' backend.

Wave-honest limits (§E.5 sub-wave 6 grounding brief):
  - Registry is METADATA-ONLY.  It does not call backends; it records
    their ratification state.  Live-invocation paths remain untouched
    (each seam already refuses on invocation of an unratified backend
    per D10 discipline).  The registry adds a QUERY surface, not an
    enforcement path.
  - Case-agnostic; no coupling to any specific seam class.
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Deterministic output: insertion order preserved on read
    (Rec-3-M6SW6 verbatim 'deterministic output').
  - §3.1 P038 tokens-not-waveforms discipline preserved.

Contract:

    BACKEND_RATIFICATION_STATES = frozenset({
        "ratified", "inferred_pending_ratification",
    }).

    RegisteredBackendEntry — frozen 5-carrier:
        seam_name · backend_name · ratification_state · canon_anchor ·
        ratified_at_utc (Optional[str] · ISO-8601 when ratified,
        None when inferred_pending_ratification).

    BackendRegistrySurface — frozen 1-carrier:
        entries: Tuple[RegisteredBackendEntry, ...].

    register_backend(*, registry, seam_name, backend_name,
                     ratification_state, canon_anchor,
                     ratified_at_utc=None) -> BackendRegistrySurface
        Appends an entry.  Returns a new BackendRegistrySurface
        (immutability preserved).  Refuses:
        - BackendRatificationStateInvalidError on state ∉
          BACKEND_RATIFICATION_STATES.
        - BackendRatifiedButMissingRatifiedAtError when
          ratification_state == 'ratified' and ratified_at_utc is None.

    list_ratified_backends(*, registry) ->
        Tuple[RegisteredBackendEntry, ...]
        Returns only entries with ratification_state == 'ratified',
        in insertion order.  Provenance for M6-seal-story
        'what is truly live' table.

    list_inferred_backends(*, registry) ->
        Tuple[RegisteredBackendEntry, ...]
        Returns only entries with ratification_state ==
        'inferred_pending_ratification', in insertion order.
        Provenance for M6-seal-story 'pending owner ratification'
        table.

    assert_seam_has_ratified_backend(*, registry, seam_name) -> None
        Refuses SeamHasNoRatifiedBackendError when no ratified
        backend is registered under seam_name.  Load-bearing gate
        for future live-invocation paths.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


BACKEND_RATIFICATION_STATES = frozenset({
    "ratified", "inferred_pending_ratification",
})


class BackendRatificationStateInvalidError(ValueError):
    """`ratification_state` not in the closed set
    BACKEND_RATIFICATION_STATES.  Rec-3-M6SW6 verbatim:
    'closed-set refusal on unknown status'."""


class BackendRatifiedButMissingRatifiedAtError(ValueError):
    """`ratification_state='ratified'` requires an ISO-8601
    `ratified_at_utc` timestamp evidencing when ratification landed
    (§P036 receipt-before-result: no ratification claim without a
    dated receipt)."""


class SeamHasNoRatifiedBackendError(LookupError):
    """`assert_seam_has_ratified_backend` refusal: no backend under
    the given seam_name is in state 'ratified'.  Load-bearing gate
    for live-invocation paths."""


@dataclass(frozen=True)
class RegisteredBackendEntry:
    seam_name: str
    backend_name: str
    ratification_state: str
    canon_anchor: str
    ratified_at_utc: Optional[str]


@dataclass(frozen=True)
class BackendRegistrySurface:
    entries: Tuple[RegisteredBackendEntry, ...]


def register_backend(
    *,
    registry: BackendRegistrySurface,
    seam_name: str,
    backend_name: str,
    ratification_state: str,
    canon_anchor: str,
    ratified_at_utc: Optional[str] = None,
) -> BackendRegistrySurface:
    if ratification_state not in BACKEND_RATIFICATION_STATES:
        raise BackendRatificationStateInvalidError(
            f"ratification_state={ratification_state!r} not in "
            f"closed set {sorted(BACKEND_RATIFICATION_STATES)!r}"
        )
    if ratification_state == "ratified" and ratified_at_utc is None:
        raise BackendRatifiedButMissingRatifiedAtError(
            "ratified state requires a ratified_at_utc timestamp "
            "(§P036 receipt-before-result)"
        )
    new_entry = RegisteredBackendEntry(
        seam_name=seam_name,
        backend_name=backend_name,
        ratification_state=ratification_state,
        canon_anchor=canon_anchor,
        ratified_at_utc=ratified_at_utc,
    )
    return BackendRegistrySurface(
        entries=registry.entries + (new_entry,),
    )


def list_ratified_backends(
    *, registry: BackendRegistrySurface,
) -> Tuple[RegisteredBackendEntry, ...]:
    return tuple(
        e for e in registry.entries
        if e.ratification_state == "ratified"
    )


def list_inferred_backends(
    *, registry: BackendRegistrySurface,
) -> Tuple[RegisteredBackendEntry, ...]:
    return tuple(
        e for e in registry.entries
        if e.ratification_state == "inferred_pending_ratification"
    )


def assert_seam_has_ratified_backend(
    *, registry: BackendRegistrySurface, seam_name: str,
) -> None:
    for e in registry.entries:
        if e.seam_name == seam_name and e.ratification_state == "ratified":
            return None
    raise SeamHasNoRatifiedBackendError(
        f"seam_name={seam_name!r} has no ratified backend registered"
    )
