"""services.watch.mkono · Doc 8 §Line 28 verbatim — the hand.

'Mkono, the hand, which acts and holds no judgement — a deterministic
mapping from verdict properties to actions.'
                                                    — Canon 8 §Line 28

Two capabilities live on this module:

1. `map_verdict_to_action(v, action_id, issued_at)`. Deterministic
   mapping from a MachoVerdict to a WatchActionV0. No randomness,
   no I/O, no policy interpretation. §Line 30 verbatim governs the
   externally-steerable cap (annotate/shape/contain — never sever).
   §Line 31 + the closed six-signal registry govern the sever unlock.
   §Line 99 governs the four-class ladder (destroy does not exist).

2. `persist_action(a)`. Seam law enforcement (§Line 6): the action's
   `verdict_ref` MUST already be on record before Mkono may write.
   Write-once JSONL append via services.watch.persistence.

Legacy `act_on_verdict(payload)` for the W10 CP8 WatchActionRecord_v0
grammar is retained so state rollups continue to render.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts.watch_action import WatchActionRecord_v0
from contracts.watch_action_v0 import WatchActionV0
from services.watch.macho import MachoVerdict, load_verdicts


# ---------------- W10 CP8 legacy Mkono ---------------- #


_DEFAULT_DIR = "/app/assessment_workspace/phase0/watch_actions"


def _dir() -> Path:
    return Path(os.environ.get("WATCH_ACTIONS_DIR", _DEFAULT_DIR))


def _find_verdict(verdict_id: str):
    for v in load_verdicts():
        if v.verdict_id == verdict_id:
            return v
    return None


def _find_action_for_verdict(verdict_id: str) -> Optional[WatchActionRecord_v0]:
    for a in load_actions():
        if a.verdict_id == verdict_id:
            return a
    return None


def act_on_verdict(payload: Dict[str, Any]) -> WatchActionRecord_v0:
    """Legacy Mkono path (W10 CP8) — WatchActionRecord_v0."""
    a = WatchActionRecord_v0(**payload)
    if _find_verdict(a.verdict_id) is None:
        raise ValueError(
            f"verdict {a.verdict_id!r} not on record. Canon 8 §6 seam law: "
            f"Macho mints the verdict before Mkono acts."
        )
    if _find_action_for_verdict(a.verdict_id) is not None:
        raise ValueError(
            f"verdict {a.verdict_id!r} already has an action on record. "
            f"Canon 8 §32.5: one atomic act-and-attest per verdict."
        )
    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{a.action_id}.json").write_text(
        json.dumps(a.model_dump(), indent=2, ensure_ascii=False)
    )
    return a


def load_actions() -> List[WatchActionRecord_v0]:
    d = _dir()
    if not d.is_dir():
        return []
    return sorted(
        (WatchActionRecord_v0(**json.loads(p.read_text()))
         for p in d.glob("ax_*.json")),
        key=lambda a: (a.at_iso, a.action_id),
    )


# ---------------- W11 C CP-C2 · deterministic mapper ---------------- #


# §Line 30 verbatim: externally-steerable severity → action class.
# The mapping is a code-time discipline, not a runtime knob (Line 31
# verbatim: 'no parameter through which a detector's confidence can
# enter').
_STEERABLE_INTENSITY_TO_ACTION_CLASS = {
    "noted":    "annotate",   # §Line 99: 'annotate (mark the record, change nothing)'
    "elevated": "shape",      # §Line 99: 'shape (friction: throttle, stricter masking, ...)'
    "severe":   "contain",    # §Line 30: 'caps at reversible containment, whatever its score'
}


def _contain_ttl_seconds() -> int:
    """Default TTL for contain actions · owner-ceremonial value per
    §Line 221 ('the tightest ceiling ... the shortest retention').
    Runtime-tunable via WATCH_CONTAIN_DEFAULT_TTL_SECONDS."""
    raw = os.environ.get("WATCH_CONTAIN_DEFAULT_TTL_SECONDS", "3600")
    try:
        n = int(raw)
    except ValueError:
        n = 3600
    return n if n > 0 else 3600


def map_verdict_to_action(
    v: MachoVerdict,
    action_id: str,
    issued_at: str,
) -> WatchActionV0:
    """Deterministic mapping · Doc 8 §Line 28 verbatim:
        'Mkono, the hand, which acts and holds no judgement — a
         deterministic mapping from verdict properties to actions.'

    §Line 30 verbatim: 'Everything externally steerable caps at
    reversible containment, whatever its score.' — externally-steerable
    verdicts map to annotate/shape/contain (never sever).

    §Line 31 verbatim: the closed six-signal registry is 'the whole of
    what may unlock the Watch's maximum autonomous force.' — sever
    action is emitted only when the verdict rests on structural_certainty.

    §Line 99 verbatim: four classes and only four — 'There is no fifth
    class: destroy does not exist in the Watch, per W3.'
    """
    if v.verdict_class == "structural_certainty":
        # Grammar guarantees sever_certainty_signal_id is set here.
        # WatchActionV0's own model_validator re-enforces (defence in depth).
        return WatchActionV0(
            action_id=action_id,
            action_class="sever",  # §Line 99 sever
            subject_ref=v.subject_ref,
            verdict_ref=v.verdict_id,
            sever_certainty_signal_id=v.sever_certainty_signal_id,
            reversible=False,      # §Line 99: sever 'holds rather than expires'
            issued_at=issued_at,
        )

    # externally_steerable: cap at reversible containment.
    action_class = _STEERABLE_INTENSITY_TO_ACTION_CLASS[v.intensity]
    if action_class == "contain":
        return WatchActionV0(
            action_id=action_id,
            action_class="contain",
            subject_ref=v.subject_ref,
            verdict_ref=v.verdict_id,
            ttl_seconds=_contain_ttl_seconds(),
            reversible=True,
            issued_at=issued_at,
        )
    return WatchActionV0(
        action_id=action_id,
        action_class=action_class,   # 'annotate' or 'shape'
        subject_ref=v.subject_ref,
        verdict_ref=v.verdict_id,
        reversible=True,
        issued_at=issued_at,
    )


def persist_action(a: WatchActionV0) -> WatchActionV0:
    """Land the action on the shared record. Doc 8 §Line 6 verbatim
    (seam law): the verdict_ref MUST already be on record before
    Mkono may write.

    Raises:
      ValueError · when verdict_ref is not on the MachoVerdict store.
      WriteOnceViolation · via persistence layer on duplicate action_id.
    """
    from services.watch.persistence import get_verdict, append_action

    if get_verdict(a.verdict_ref) is None:
        raise ValueError(
            f"verdict {a.verdict_ref!r} not on record. Doc 8 §Line 6 "
            "verbatim (seam law): Macho mints the verdict before "
            "Mkono acts."
        )
    return append_action(a)
