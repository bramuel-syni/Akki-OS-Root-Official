"""services.watch.mirage — Canon 8 §15-§16 Grey Mirror mirage fabric.

Writers:
  * plant_mirage(payload) — writes Mirage_v0. Proactive; no verdict
    required (Macho does not sense to plant; Mkono plants preemptively
    per §15 discipline).
  * record_touch(payload) — writes MirageTouch_v0. Requires mirage on
    record (chokepoint · no side doors).
  * engage_mirage(touch_id, verdict_id) — atomic act-and-attest per
    §32.5. On 'guilty_use' touch: mints Mkono action with
    action_class='severance_executed' + writes Severance_v0 record.
    On 'innocent_read' touch: mints Mkono action with
    action_class='noted_no_action' (no severance).

Seam law (§6): engage requires the verdict on record. §32.4 keeps
mirage construction hidden throughout.

Records:
  * phase0/mirages/mr_*.json                    (Mirage_v0)
  * phase0/mirage_touches/mt_*.json             (MirageTouch_v0)
  * phase0/severances/sv_*.json                 (Severance_v0)
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts.mirage import Mirage_v0, MirageTouch_v0, Severance_v0
from services.watch.macho import load_verdicts
from services.watch.mkono import act_on_verdict, load_actions


_DEFAULT_M_DIR = "/app/assessment_workspace/phase0/mirages"
_DEFAULT_T_DIR = "/app/assessment_workspace/phase0/mirage_touches"
_DEFAULT_S_DIR = "/app/assessment_workspace/phase0/severances"


def _m_dir() -> Path:
    return Path(os.environ.get("MIRAGES_DIR", _DEFAULT_M_DIR))


def _t_dir() -> Path:
    return Path(os.environ.get("MIRAGE_TOUCHES_DIR", _DEFAULT_T_DIR))


def _s_dir() -> Path:
    return Path(os.environ.get("SEVERANCES_DIR", _DEFAULT_S_DIR))


# ---------- loaders ----------

def load_mirages() -> List[Mirage_v0]:
    d = _m_dir()
    if not d.is_dir():
        return []
    return sorted(
        (Mirage_v0(**json.loads(p.read_text())) for p in d.glob("mr_*.json")),
        key=lambda m: (m.planted_at, m.mirage_id),
    )


def load_touches() -> List[MirageTouch_v0]:
    d = _t_dir()
    if not d.is_dir():
        return []
    return sorted(
        (MirageTouch_v0(**json.loads(p.read_text()))
         for p in d.glob("mt_*.json")),
        key=lambda t: (t.touched_at, t.touch_id),
    )


def load_severances() -> List[Severance_v0]:
    d = _s_dir()
    if not d.is_dir():
        return []
    return sorted(
        (Severance_v0(**json.loads(p.read_text()))
         for p in d.glob("sv_*.json")),
        key=lambda s: (s.severed_at, s.severance_id),
    )


def _find_mirage(mirage_id: str) -> Optional[Mirage_v0]:
    for m in load_mirages():
        if m.mirage_id == mirage_id:
            return m
    return None


def _find_touch(touch_id: str) -> Optional[MirageTouch_v0]:
    for t in load_touches():
        if t.touch_id == touch_id:
            return t
    return None


def _touch_already_engaged(touch_id: str) -> bool:
    for a in load_actions():
        # engagement writes an action with an outcome_note that
        # references the touch_id.
        if touch_id in a.outcome_note:
            return True
    return False


# ---------- writers ----------

def plant_mirage(payload: Dict[str, Any]) -> Mirage_v0:
    """Plant a mirage (Canon 8 §15 · proactive). Refuses overwrite
    (§43)."""
    m = Mirage_v0(**payload)
    d = _m_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{m.mirage_id}.json"
    if path.exists():
        raise ValueError(
            f"mirage {m.mirage_id!r} already on record. Canon 8 §43: "
            f"correction is by new entry only."
        )
    path.write_text(json.dumps(m.model_dump(), indent=2, ensure_ascii=False))
    return m


def record_touch(payload: Dict[str, Any]) -> MirageTouch_v0:
    """Record a mirage touch. Refuses if the mirage is not on record
    (chokepoint · no side doors) OR if the touch already recorded."""
    t = MirageTouch_v0(**payload)
    if _find_mirage(t.mirage_id) is None:
        raise ValueError(
            f"mirage {t.mirage_id!r} not on record. Touches only exist "
            f"against planted mirages (chokepoint · no side doors)."
        )
    d = _t_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{t.touch_id}.json"
    if path.exists():
        raise ValueError(
            f"touch {t.touch_id!r} already on record. Canon 8 §43: "
            f"correction is by new entry only."
        )
    path.write_text(json.dumps(t.model_dump(), indent=2, ensure_ascii=False))
    return t


def engage_mirage(touch_id: str, verdict_id: str) -> Dict[str, Any]:
    """Engage a mirage on a recorded touch (Canon 8 §15 aftermath flow).

    guilty_use  → mint action 'severance_executed' + write Severance_v0.
    innocent_read → mint action 'noted_no_action' (no severance).

    Refuses:
      - touch not on record.
      - verdict not on record (seam law).
      - touch already engaged (idempotency · §43).
    """
    t = _find_touch(touch_id)
    if t is None:
        raise ValueError(
            f"touch {touch_id!r} not on record. Record the touch before "
            f"engaging."
        )
    if not any(v.verdict_id == verdict_id for v in load_verdicts()):
        raise ValueError(
            f"verdict {verdict_id!r} not on record. Canon 8 §6 seam law: "
            f"Macho mints the verdict before Mkono engages the mirage."
        )
    if _touch_already_engaged(touch_id):
        raise ValueError(
            f"touch {touch_id!r} already engaged. Canon 8 §43: correction "
            f"is by new entry only."
        )

    if t.touch_kind == "guilty_use":
        action_class = "severance_executed"
        outcome_note = (
            f"Severance executed on Mkono authority for guilty_use touch "
            f"{touch_id!r}. Canon 8 §15 aftermath — decision panel "
            f"receives aftermath, not request."
        )
    else:  # innocent_read
        action_class = "noted_no_action"
        outcome_note = (
            f"Innocent_read touch {touch_id!r} noted; ordinary work "
            f"continues under scope. Canon 8 §15/§22 restraint."
        )

    action = act_on_verdict({
        "action_id": f"ax_engage_{touch_id}",
        "at_iso": t.touched_at,
        "verdict_id": verdict_id,
        "action_class": action_class,
        "responder": "mkono.severance_manager"
                     if action_class == "severance_executed"
                     else "mkono.restraint_writer",
        "acted_on_ref": t.actor_ref,
        "outcome_note": outcome_note,
    })

    severance_id: Optional[str] = None
    if t.touch_kind == "guilty_use":
        severance_id = f"sv_{touch_id}"
        severance = Severance_v0(**{
            "severance_id": severance_id,
            "touch_id": touch_id,
            "severed_at": t.touched_at,
            "severed_by": "mkono.severance_manager",
            "aftermath_note": (
                f"Access severed on Mkono authority following guilty_use "
                f"touch {touch_id!r}. Canon 8 §15: decision panel "
                f"receives aftermath, not request."
            ),
        })
        d = _s_dir()
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{severance_id}.json").write_text(
            json.dumps(severance.model_dump(), indent=2, ensure_ascii=False)
        )

    return {
        "action_class": action_class,
        "action_id": action.action_id,
        "severance_id": severance_id,
    }
