"""services.watch.route_recheck_failure — CA1-011 enforcement half (W9).

Owner Ruling 2026-08-25T23:15Z (CA1-011 SPLIT): W7 landed the re-check
state + surfacing (`services/model_recheck/status.py`); W9 lands the
Watch-routed enforcement here at the NAMED SEAM.

Behavior:
  1. Read `status_for(model_id)`.
  2. If state == 'overdue', mint a Macho verdict + Mkono action pair
     atomically (Canon 8 §32.5).
  3. Return {fired, state, verdict_id?, action_id?}.

Idempotency: a second call for the same overdue model_id returns the
existing verdict/action pair; no double-mint (Canon 8 §32.5 atomic).

Verdict shape:
  * sensor      = 'macho.recheck_watcher'
  * signal_class= 'recheck_overdue'
  * severity    = 'attention'
  * subject_kind= 'artifact'
  * subject_ref = f'model:{model_id}'
  * evidence_note names the model_id + the overdue due_date.

Action shape:
  * action_class= 'mark_minted'
  * responder   = 'mkono.recheck_responder'
  * acted_on_ref= f'model:{model_id}'
  * outcome_note names the mark reason.
"""
from __future__ import annotations

from typing import Any, Dict

from services.model_recheck.status import status_for
from services.watch.macho import mint_verdict, load_verdicts
from services.watch.mkono import act_on_verdict, load_actions


def _existing_pair(model_id: str) -> Dict[str, Any]:
    subject_ref = f"model:{model_id}"
    for v in load_verdicts():
        if (
            v.signal_class == "recheck_overdue"
            and v.subject_ref == subject_ref
        ):
            for a in load_actions():
                if a.verdict_id == v.verdict_id:
                    return {
                        "fired": True,
                        "state": "overdue",
                        "verdict_id": v.verdict_id,
                        "action_id": a.action_id,
                    }
            return {
                "fired": True,
                "state": "overdue",
                "verdict_id": v.verdict_id,
                "action_id": None,
            }
    return {}


def route_recheck_failure(model_id: str) -> Dict[str, Any]:
    """CA1-011 enforcement half. See module docstring."""
    st = status_for(model_id)
    state = st.get("state")
    if state != "overdue":
        return {"fired": False, "state": state, "note": st.get("honest_note")}

    existing = _existing_pair(model_id)
    if existing:
        return existing

    due_at = st.get("re_check_due_at", "?")
    verdict_id = f"vd_recheck_{model_id.replace('.', '_').replace('-', '_')}"
    action_id = f"ax_recheck_{model_id.replace('.', '_').replace('-', '_')}"
    now_iso = st.get("observed_at", "1970-01-01T00:00:00Z")

    v = mint_verdict({
        "verdict_id": verdict_id,
        "at_iso": now_iso,
        "sensor": "macho.recheck_watcher",
        "signal_class": "recheck_overdue",
        "severity": "attention",
        "subject_kind": "artifact",
        "subject_ref": f"model:{model_id}",
        "evidence_note": (
            f"Model {model_id!r} re-check overdue: due at {due_at!r}, "
            f"observed at {now_iso!r}. CA1-011 Doc 13 §23."
        ),
    })
    a = act_on_verdict({
        "action_id": action_id,
        "at_iso": now_iso,
        "verdict_id": v.verdict_id,
        "action_class": "mark_minted",
        "responder": "mkono.recheck_responder",
        "acted_on_ref": f"model:{model_id}",
        "outcome_note": (
            f"Attention mark minted on model {model_id!r} for CA1-011 "
            f"re-check overdue. Standing decrement until re-check clears."
        ),
    })
    return {
        "fired": True,
        "state": "overdue",
        "verdict_id": v.verdict_id,
        "action_id": a.action_id,
    }
