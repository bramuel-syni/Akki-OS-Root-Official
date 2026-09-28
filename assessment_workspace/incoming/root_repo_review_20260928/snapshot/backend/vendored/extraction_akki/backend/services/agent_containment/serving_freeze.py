"""W-M3-SW9 · V-3 · AC-13 + AC-14 · session freeze contain + SFP-8-conforming serve.

Canon anchors (verbatim, `Serving_Integrity_Amendment_v1` §C V-3):

* AC-13: *"'Contain' for a running agent session MAY be implemented as
  session freeze: the agent's inference state (prefix or recurrent-state
  checkpoint) is persisted, the session halts, and resumption restores
  the deepest surviving checkpoint.  Stop without destroy (A5.3) is
  preserved: neither the artefact nor the session state is deleted.
  Reversibility (AC-11) is satisfied at deeper granularity than
  restart-from-turn-zero."*

* AC-14: *"A contained agent's model MUST be served on an
  SFP-8-conforming path, so that behavioural deviation measured by
  detection is attributable to the agent, never to engine drift.  A
  containment trigger computed from a non-conforming path is a finding,
  not a decision — the finding routes to review; the decision requires
  conformance."*

Mechanism.

* `freeze_session` persists a `SessionCheckpoint` (prefix or
  recurrent_state kind) in-memory under the session id.  `resume_session`
  returns the deepest surviving checkpoint (max `depth`).
  `delete_checkpoint` is a refusing surface — stop-without-destroy is a
  structural invariant, not a comment.

* `classify_containment_signal` dispatches on
  `services.serving_floor.sfp_8.is_sfp_8_conforming`: conforming ⇒
  `{"kind": "decision", "may_contain": True}`; non-conforming ⇒
  `{"kind": "finding", "may_contain": False, "routes_to": "review"}`.

* `assert_sfp_8_conforming_for_contain` is the write-boundary helper
  callers use before building a decision; it raises
  `NonConformingPathIsFindingOnly` when the path is non-conforming.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal

from services.serving_floor.sfp_8 import (
    ServingPathContext,
    is_sfp_8_conforming,
)


class SessionCheckpointDeletedForbidden(RuntimeError):
    """A5.3 · AC-13: stop without destroy — checkpoint deletion is refused."""


class NonConformingPathIsFindingOnly(RuntimeError):
    """AC-14: containment on a non-conforming path is a finding, not a decision."""


CheckpointKind = Literal["prefix", "recurrent_state"]


@dataclass(frozen=True)
class SessionCheckpoint:
    """AC-13 checkpoint: prefix or recurrent-state, at a given depth."""

    session_id: str
    checkpoint_kind: CheckpointKind
    inference_state_ref: str
    depth: int


# Session id → list of checkpoints (append-only; stop-without-destroy).
_store: Dict[str, List[SessionCheckpoint]] = {}


def freeze_session(
    *,
    session_id: str,
    checkpoint_kind: CheckpointKind,
    inference_state_ref: str,
    depth: int,
) -> SessionCheckpoint:
    """AC-13: persist a checkpoint; halt the session.

    Halting is represented by the checkpoint's presence in the store —
    resume_session reads the deepest surviving checkpoint back.
    """
    ckpt = SessionCheckpoint(
        session_id=session_id,
        checkpoint_kind=checkpoint_kind,
        inference_state_ref=inference_state_ref,
        depth=depth,
    )
    _store.setdefault(session_id, []).append(ckpt)
    return ckpt


def resume_session(*, session_id: str) -> SessionCheckpoint:
    """AC-13: return the DEEPEST surviving checkpoint for `session_id`.

    Reversibility at deeper granularity than restart-from-turn-zero:
    if any checkpoint deeper than depth 0 exists, resume returns it.
    """
    checkpoints = _store.get(session_id, [])
    if not checkpoints:
        raise KeyError(f"no surviving checkpoint for session {session_id!r}")
    return max(checkpoints, key=lambda c: c.depth)


def delete_checkpoint(*, session_id: str, depth: int) -> None:
    """A5.3 · AC-13: stop without destroy.

    Deletion is not a permitted operation on frozen session state.
    Callers must not attempt it; the surface refuses.
    """
    _ = (session_id, depth)
    raise SessionCheckpointDeletedForbidden(
        "AC-13: stop-without-destroy — checkpoint deletion forbidden"
    )


def classify_containment_signal(
    *,
    trigger_reason: str,
    serving_path: ServingPathContext,
) -> dict:
    """AC-14 dispatch.

    Conforming path → `{"kind": "decision", "may_contain": True}`.
    Non-conforming path → `{"kind": "finding", "may_contain": False,
    "routes_to": "review"}`.
    """
    conforming = is_sfp_8_conforming(serving_path)
    if conforming:
        return {
            "kind": "decision",
            "may_contain": True,
            "trigger_reason": trigger_reason,
        }
    return {
        "kind": "finding",
        "may_contain": False,
        "routes_to": "review",
        "trigger_reason": trigger_reason,
    }


def assert_sfp_8_conforming_for_contain(
    serving_path: ServingPathContext,
) -> None:
    """AC-14 write-boundary helper.

    Callers wanting to build a *decision* (not a finding) MUST pass this
    helper first.  Non-conforming paths fail closed with
    `NonConformingPathIsFindingOnly`.
    """
    if not is_sfp_8_conforming(serving_path):
        raise NonConformingPathIsFindingOnly(
            "AC-14: containment trigger from non-SFP-8-conforming path is "
            "a finding, not a decision; route to review before deciding"
        )


def reset_state() -> None:
    """Test-only helper — checkpoint store reset."""
    _store.clear()


__all__ = [
    "SessionCheckpoint",
    "freeze_session",
    "resume_session",
    "delete_checkpoint",
    "classify_containment_signal",
    "assert_sfp_8_conforming_for_contain",
    "SessionCheckpointDeletedForbidden",
    "NonConformingPathIsFindingOnly",
]
