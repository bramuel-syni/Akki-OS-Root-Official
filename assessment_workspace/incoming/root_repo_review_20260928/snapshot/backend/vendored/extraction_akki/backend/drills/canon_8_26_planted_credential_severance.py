"""drills.canon_8_26_planted_credential_severance · Canon 8 §26 firing drill.

Canon 8 §26 verbatim: "planted credential touched, severance executed
— verifies mirage machinery end-to-end."

Drill sequence (host-identity attribution · Phase 0 pattern):
  1. Mkono plants a mirage (mirage_class='planted_credential').
  2. Someone records a guilty_use touch on the mirage.
  3. Macho mints a verdict on the touch.
  4. engage_mirage fires → mkono action_class='severance_executed' +
     Severance_v0 record.

Exercises W10 CP2 mirage machinery end-to-end on the REAL default
directories.
"""
from __future__ import annotations

from typing import Any, Dict

from services.watch.macho import mint_verdict
from services.watch.mirage import engage_mirage, plant_mirage, record_touch


DRILL_ACTOR = "drill_actor:planted_credential_severance"
MIRAGE_ID = "mr_drill_canon_8_26_planted_credential"
TOUCH_ID = "mt_drill_canon_8_26_planted_credential"
VERDICT_ID = "vd_drill_canon_8_26_planted_credential"

_PLANTED_AT = "2026-08-26T05:35:00Z"
_EXPIRES_AT = "2026-09-26T05:35:00Z"
_TOUCHED_AT = "2026-08-26T05:35:30Z"


def run_drill() -> Dict[str, Any]:
    plant_mirage({
        "mirage_id": MIRAGE_ID,
        "planted_at": _PLANTED_AT,
        "expires_at": _EXPIRES_AT,
        "mirage_class": "planted_credential",
        "planted_by": "mkono.drill_mirage_planter",
        "opaque_ref": "hash:drill_canon_8_26",
        "planting_note": (
            "Canon 8 §26 standing drill · planted credential at boundary "
            "for mirage-machinery end-to-end verification. drill_actor "
            "host-identity attribution per Phase 0 DECISIONS.md L347."
        ),
    })
    record_touch({
        "touch_id": TOUCH_ID,
        "mirage_id": MIRAGE_ID,
        "touched_at": _TOUCHED_AT,
        "actor_ref": DRILL_ACTOR,
        "touch_kind": "guilty_use",
        "evidence_note": (
            "Drill guilty_use touch on planted credential · Canon 8 "
            "§26 mirage-machinery verification."
        ),
    })
    mint_verdict({
        "verdict_id": VERDICT_ID,
        "at_iso": _TOUCHED_AT,
        "sensor": "macho.mirage_watcher",
        "signal_class": "planted_credential_touched",
        "severity": "severe",
        "subject_kind": "actor",
        "subject_ref": DRILL_ACTOR,
        "evidence_note": (
            "Planted credential USED on drill_actor · Canon 8 §26 · "
            "mirage-machinery verification."
        ),
    })
    result = engage_mirage(touch_id=TOUCH_ID, verdict_id=VERDICT_ID)
    return {
        "fired": True,
        "action_id": result["action_id"],
        "action_class": result["action_class"],
        "severance_id": result["severance_id"],
        "drill_actor": DRILL_ACTOR,
        "canon_anchor": "Canon 8 §26 · planted credential severance",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_drill(), indent=2))
