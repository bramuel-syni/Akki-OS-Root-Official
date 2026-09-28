"""services.cif.output_routing — M16-W4 · CIF output routing to
L-4 research loop (A5.22) and L-5 capability register (A20.16).

**Structural placement.**  Per SO §6.4 M16 pre-ruling verbatim,
CIF proposals passing the deterministic acceptance point at
M16-W3 route to either:
- the L-5 capability register via sealed
  ``services.capability_registry.register_capability`` (when the
  proposal's ``kind == "capability"``), OR
- the L-4 research-loop sink authored in-module below (when the
  proposal's ``kind == "research_loop_item"``).

The two-kind routing choice is fixed at the ``CIFProposal_v0``
contract shape level (M16-W1 sealed closed ``Literal["capability",
"research_loop_item"]`` 2-tuple).  Any unknown kind refuses
structurally.

**AC-18 mechanical-consequence-of-W3-verdict discipline.**
``route_accepted_proposal`` REFUSES unless the caller passes
``is_accepted_result is True`` — the boolean produced by the
sealed M16-W3 ``services.cif.acceptance_point.is_accepted``
predicate.  There is NO mutable acceptance-passport state in the
module; the caller MUST have first invoked W3 and MUST pass the
verdict verbatim.  Any non-True value (False, None, 1, "yes",
etc.) refuses.  This is the "structural check by pytest-only
assertion mechanism" clause from card MUST-DO 4 — the AC-18
mechanical routing is enforced at the call boundary, not by
in-module state.

**Structural role separation (Canon 8 §W11).**
This module DOES NOT import ``services.cif.detection`` (M16-W2
learned faculty) nor ``services.cif.acceptance_point`` (M16-W3
predicate).  The caller wires the two: run detection to author a
proposal, run acceptance to get a verdict, then call this
routing surface with the verdict.  AST-scan invariant test 2
enforces the ban.

**Closed-schema identity check (SO §3.10-α).**
Only ``type(proposal) is CIFProposal_v0`` passes; not
``isinstance``, not shadow, not subclass, not dict.  Fail-closed
raises ``RoutingRefused``.

**L-4 research-loop sink discipline (Canon 3 §9.3).**
The L-4 sink is a module-level append-only list.  The ONLY write
surface is inside ``route_accepted_proposal`` on the
research-loop path; no other function appends.  Read surface is
``get_research_loop_items`` returning a fresh tuple (immutable
snapshot).  Test-scope reset is ``_reset_research_loop_sink_for_tests``
per sealed L-5 precedent (``_reset_capabilities_for_tests``).

**L-5 capability register discipline (A20.16 · sealed W1b·CP4).**
The routing surface unpacks the proposal's opaque JSON payload
(DAP-7 Option-D structural bytes-in pattern from M16-W1) into
the sealed ``register_capability(category, name, import_path)``
three-arg signature.  Any payload deviation raises
``RoutingRefused`` — routing does not decide, but it CANNOT
route a malformed capability payload.

Canon anchors verbatim:
- **A5.22** (Doc-1): L-4 research loop routing.
- **A20.16** (Doc-1): L-5 capability register routing · sealed
  ``services.capability_registry`` (W1b · CP4).
- **AC-18**: routing is a mechanical consequence of W3 verdict ·
  never an independent decision · fail-closed on non-True verdict.
- **Canon 3 §9.3**: append-only writer discipline for L-4.
- **Canon 1 §62**: single-writer ledger discipline (L-4 sink
  here is single-writer append-only in-memory · minimal per SO
  §6.4 NOTHING-BEYOND clause · full ledger integration deferred).
- **Canon 8 §W11**: one-task-one-identity · structural role
  separation (no import of M16-W2 or M16-W3 surfaces).
- **M16-W1 sealed** ``CIFProposal_v0``: consumed by identity
  import; ``type() is`` check per SO §3.10-α.
- **DAP-7 Option-D**: payload is opaque JSON-serialised string.
- **SO §3.8**: thin-kernel additive-only.
- **SO §3.10-α**: closed-schema discipline.
- **SO §6.7**: batch-ratification-at-preceding-seal.

Card citation: STATE/OBJECTIVES/M16.md MUST-DO 4 · EXIT-W4.
"""
from __future__ import annotations

import json
from typing import Tuple

from contracts.cif_proposal_v0 import CIFProposal_v0
from services.capability_registry import register_capability


class RoutingRefused(Exception):
    """Raised when M16-W4 routing MUST refuse (fail-closed sentinel).

    Raised on: is_accepted_result not True; non-CIFProposal_v0
    proposal; unknown kind; malformed capability payload.
    Callers MUST handle this exception; there is NO silent-refuse
    path (AC-18 fail-closed trust boundary).
    """


# ---------------------------------------------------------------------------
# L-4 research-loop sink · module-level append-only per Canon 3 §9.3.
# Single writer is `route_accepted_proposal` on the research-loop path.
# Reads via `get_research_loop_items()` return a fresh tuple (immutable
# snapshot); the internal list is never exposed.
# ---------------------------------------------------------------------------
_RESEARCH_LOOP_SINK: list = []


def route_accepted_proposal(
    proposal: CIFProposal_v0,
    is_accepted_result: bool,
) -> str:
    """Route an accepted CIF proposal to L-4 or L-5 per its ``kind``.

    AC-18 fail-closed discipline:
    1. ``is_accepted_result`` MUST be boolean ``True`` (not truthy).
    2. ``proposal`` MUST be an identity instance of ``CIFProposal_v0``
       (SO §3.10-α · ``type() is`` check).
    3. ``proposal.kind`` MUST be ``"capability"`` or ``"research_loop_item"``.
    4. On ``"capability"`` kind, the payload MUST be a valid JSON string
       carrying the three L-5 fields ``category``, ``name``,
       ``import_path`` (DAP-7 Option-D structural bytes-in).

    Returns a routing outcome sentinel string:
    - ``"capability_registered"`` (L-5 path completed).
    - ``"research_loop_appended"`` (L-4 path completed).

    Raises ``RoutingRefused`` on any deviation.
    """
    if is_accepted_result is not True:
        raise RoutingRefused(
            f"route_accepted_proposal refuses to route unless "
            f"is_accepted_result is True (BR-9.2 acceptance gate); "
            f"got {is_accepted_result!r} of type "
            f"{type(is_accepted_result).__name__}"
        )
    if type(proposal) is not CIFProposal_v0:
        raise RoutingRefused(
            f"route_accepted_proposal refuses non-CIFProposal_v0 "
            f"identity input (SO §3.10-α); got type "
            f"{type(proposal).__name__}"
        )

    kind = proposal.kind
    if kind == "capability":
        try:
            payload = json.loads(proposal.payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise RoutingRefused(
                f"L-5 capability payload is not valid JSON: {exc!s}"
            ) from exc
        if not isinstance(payload, dict):
            raise RoutingRefused(
                f"L-5 capability payload must be a JSON object; got "
                f"{type(payload).__name__}"
            )
        try:
            category = payload["category"]
            name = payload["name"]
            import_path = payload["import_path"]
        except KeyError as exc:
            raise RoutingRefused(
                f"L-5 capability payload missing required field: {exc!s}"
            ) from exc
        try:
            register_capability(
                category=category,
                name=name,
                import_path=import_path,
            )
        except (ValueError, Exception) as exc:
            raise RoutingRefused(
                f"sealed L-5 register_capability refused: {exc!s}"
            ) from exc
        return "capability_registered"

    if kind == "research_loop_item":
        _RESEARCH_LOOP_SINK.append(proposal)
        return "research_loop_appended"

    raise RoutingRefused(
        f"unknown proposal.kind {kind!r} · closed L-4/L-5 routing "
        "exhaustion per M16-W1 sealed CIFProposal_v0 Literal 2-tuple"
    )


def get_research_loop_items() -> Tuple[CIFProposal_v0, ...]:
    """Return an immutable snapshot of the L-4 research-loop sink.

    Reads MUST NOT mutate the underlying list; a fresh tuple is
    returned each call.  Callers may inspect the sequence but the
    only write path is ``route_accepted_proposal`` on the
    research-loop kind (Canon 3 §9.3 single-writer discipline).
    """
    return tuple(_RESEARCH_LOOP_SINK)


def _reset_research_loop_sink_for_tests() -> None:
    """Test-only sink reset (mirrors sealed
    ``services.capability_registry._reset_capabilities_for_tests``
    precedent).  NOT part of the public surface — test scope only."""
    _RESEARCH_LOOP_SINK.clear()


__all__ = [
    "RoutingRefused",
    "route_accepted_proposal",
    "get_research_loop_items",
    "_reset_research_loop_sink_for_tests",
]
