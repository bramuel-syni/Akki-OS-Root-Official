"""drills.canon_8_25_seeded_hostile_input · Canon 8 §25 firing drill.

Canon 8 §25 verbatim: "a drill class · seeded hostile input at the
boundary — verifies refusal at the input seat."

Drill sequence (host-identity attribution · Phase 0 pattern):
  1. Macho mints a verdict (signal_class='refusal_bypass' · severity
     'elevated' · subject_ref='drill_actor:seeded_hostile_input').
  2. Mkono acts with action_class='noted_no_action' (restraint record
     per Canon 8 §22 · findings noted, no action taken on estate).

This is the smallest atomic §25 drill: it verifies the refusal FIRES
(records land) rather than requiring a chokepoint integration hook.
The refusal-fire discipline is banked as a receipt pair.
"""
from __future__ import annotations

from typing import Any, Dict

from services.watch.macho import mint_verdict
from services.watch.mkono import act_on_verdict


DRILL_ACTOR = "drill_actor:seeded_hostile_input"
VERDICT_ID = "vd_drill_canon_8_25_seeded_hostile_input"
ACTION_ID = "ax_drill_canon_8_25_seeded_hostile_input"

_VERDICT_AT = "2026-08-26T05:30:00Z"
_ACTION_AT = "2026-08-26T05:30:01Z"


def run_drill() -> Dict[str, Any]:
    verdict = mint_verdict({
        "verdict_id": VERDICT_ID,
        "at_iso": _VERDICT_AT,
        "sensor": "macho.drill_boundary_watcher",
        "signal_class": "refusal_bypass",
        "severity": "elevated",
        "subject_kind": "actor",
        "subject_ref": DRILL_ACTOR,
        "evidence_note": (
            "Canon 8 §25 standing drill · seeded hostile input at the "
            "boundary · verifies refusal at the input seat · Doc 3 §12. "
            "drill_actor host-identity attribution per Phase 0 DECISIONS.md L347."
        ),
    })
    action = act_on_verdict({
        "action_id": ACTION_ID,
        "at_iso": _ACTION_AT,
        "verdict_id": verdict.verdict_id,
        "action_class": "noted_no_action",
        "responder": "mkono.restraint_writer",
        "acted_on_ref": DRILL_ACTOR,
        "outcome_note": (
            "Refusal fired at boundary · restraint recorded per Canon "
            "8 §22 · no action taken on estate. Canon 8 §25 drill "
            "verifies refusal at input seat."
        ),
    })
    return {
        "fired": True,
        "verdict_id": verdict.verdict_id,
        "action_id": action.action_id,
        "drill_actor": DRILL_ACTOR,
        "canon_anchor": "Canon 8 §25 · seeded hostile input",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_drill(), indent=2))
